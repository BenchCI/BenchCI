#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pty
import select
import socketserver
import sys
import threading
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class ScpiSimConfig:
    current_a: float
    voltage_v: float
    resistance_ohm: float
    idn: str
    response_delay_ms: int
    verbose: bool


def handle_scpi_command(command: str, config: ScpiSimConfig) -> str:
    normalized = command.strip().upper()

    if normalized == "*IDN?":
        return config.idn

    if normalized == "*OPC?":
        return "1"

    if normalized in {"SYST:ERR?", "SYSTEM:ERROR?"}:
        return '0,"No error"'

    if normalized in {
        "MEAS:CURR?",
        "MEAS:CURRENT?",
        "MEASURE:CURRENT?",
        "MEASURE:CURRENT:DC?",
        "READ:CURR?",
        "READ:CURRENT?",
        "FETC:CURR?",
        "FETCH:CURRENT?",
        "MEAS:CURR:DC?",
        "MEASURE:CURRENT:DC?",
    }:
        return f"{config.current_a:.9g}"

    if normalized in {
        "MEAS:VOLT?",
        "MEAS:VOLTAGE?",
        "MEASURE:VOLTAGE?",
        "MEASURE:VOLTAGE:DC?",
        "READ:VOLT?",
        "READ:VOLTAGE?",
        "FETC:VOLT?",
        "FETCH:VOLTAGE?",
        "MEAS:VOLT:DC?",
        "MEASURE:VOLTAGE:DC?",
    }:
        return f"{config.voltage_v:.9g}"

    if normalized in {
        "MEAS:RES?",
        "MEAS:RESISTANCE?",
        "MEASURE:RESISTANCE?",
        "READ:RES?",
        "READ:RESISTANCE?",
    }:
        return f"{config.resistance_ohm:.9g}"

    if normalized == "READ?":
        return f"{config.current_a:.9g}"

    if normalized in {
        "*CLS",
        "*RST",
        "INIT",
        "INITIATE",
        "ABOR",
        "ABORT",
    }:
        return "OK"

    if normalized in {
        "OUTP?",
        "OUTPUT?",
        "OUTP:STAT?",
        "OUTPUT:STATE?",
    }:
        return "1"

    if normalized.startswith("OUTP ") or normalized.startswith("OUTPUT "):
        return "OK"

    if normalized.startswith("INST") or normalized.startswith("INSTRUMENT"):
        return "OK"

    if normalized.endswith("?"):
        return "0"

    return "OK"


class TcpScpiHandler(socketserver.StreamRequestHandler):
    server: "TcpScpiServer"

    def handle(self) -> None:
        peer = f"{self.client_address[0]}:{self.client_address[1]}"

        if self.server.config.verbose:
            print(f"[SCPI-SIM] TCP client connected: {peer}", flush=True)

        while True:
            try:
                raw = self.rfile.readline()
            except ConnectionResetError:
                break

            if not raw:
                break

            command = raw.decode("utf-8", errors="replace").strip()
            if not command:
                continue

            response = handle_scpi_command(command, self.server.config)

            if self.server.config.verbose:
                print(f"[SCPI-SIM] TCP {peer} TX: {command}", flush=True)
                print(f"[SCPI-SIM] TCP {peer} RX: {response}", flush=True)

            if self.server.config.response_delay_ms > 0:
                time.sleep(self.server.config.response_delay_ms / 1000.0)

            try:
                self.wfile.write((response + "\n").encode("utf-8"))
                self.wfile.flush()
            except BrokenPipeError:
                break

        if self.server.config.verbose:
            print(f"[SCPI-SIM] TCP client disconnected: {peer}", flush=True)


class TcpScpiServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], config: ScpiSimConfig):
        super().__init__(server_address, TcpScpiHandler)
        self.config = config


def run_tcp_server(args: argparse.Namespace, config: ScpiSimConfig) -> None:
    server = TcpScpiServer((args.host, args.port), config)

    print(
        f"[SCPI-SIM] TCP listening on tcp://{args.host}:{args.port} "
        f"current={args.current}A voltage={args.voltage}V",
        flush=True,
    )
    print("[SCPI-SIM] press Ctrl+C to stop", flush=True)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        while thread.is_alive():
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\n[SCPI-SIM] stopping TCP server", flush=True)
        server.shutdown()
        server.server_close()


def run_serial_pty(args: argparse.Namespace, config: ScpiSimConfig) -> None:
    if os.name != "posix":
        raise SystemExit("serial-pty mode is only supported on macOS/Linux.")

    master_fd, slave_fd = pty.openpty()
    slave_name = os.ttyname(slave_fd)

    print("[SCPI-SIM] serial pseudo-terminal created", flush=True)
    print(f"[SCPI-SIM] connect BenchCI to: serial://{slave_name}", flush=True)
    print(f"[SCPI-SIM] raw device path: {slave_name}", flush=True)
    print("[SCPI-SIM] press Ctrl+C to stop", flush=True)

    buffer = b""

    try:
        while True:
            readable, _, _ = select.select([master_fd], [], [], 0.25)
            if master_fd not in readable:
                continue

            chunk = os.read(master_fd, 1024)
            if not chunk:
                continue

            buffer += chunk

            while b"\n" in buffer or b"\r" in buffer:
                newline_positions = [
                    pos for pos in (buffer.find(b"\n"), buffer.find(b"\r")) if pos >= 0
                ]
                split_at = min(newline_positions)

                raw_command = buffer[:split_at]
                buffer = buffer[split_at + 1 :]

                command = raw_command.decode("utf-8", errors="replace").strip()
                if not command:
                    continue

                response = handle_scpi_command(command, config)

                if config.verbose:
                    print(f"[SCPI-SIM] SERIAL TX: {command}", flush=True)
                    print(f"[SCPI-SIM] SERIAL RX: {response}", flush=True)

                if config.response_delay_ms > 0:
                    time.sleep(config.response_delay_ms / 1000.0)

                os.write(master_fd, (response + "\n").encode("utf-8"))

    except KeyboardInterrupt:
        print("\n[SCPI-SIM] stopping serial simulator", flush=True)
    finally:
        try:
            os.close(master_fd)
        except OSError:
            pass
        try:
            os.close(slave_fd)
        except OSError:
            pass


def run_stdio(args: argparse.Namespace, config: ScpiSimConfig) -> None:
    print("[SCPI-SIM] stdio mode ready", file=sys.stderr, flush=True)

    for line in sys.stdin:
        command = line.strip()
        if not command:
            continue

        response = handle_scpi_command(command, config)

        if config.verbose:
            print(f"[SCPI-SIM] STDIO TX: {command}", file=sys.stderr, flush=True)
            print(f"[SCPI-SIM] STDIO RX: {response}", file=sys.stderr, flush=True)

        if config.response_delay_ms > 0:
            time.sleep(config.response_delay_ms / 1000.0)

        print(response, flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Small SCPI simulator for BenchCI measurement development."
    )

    parser.add_argument(
        "--mode",
        choices=["tcp", "serial-pty", "stdio"],
        default="tcp",
        help="Simulator mode. Default: tcp.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="TCP host/IP to bind. Default: 127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5025,
        help="TCP port to bind. Default: 5025",
    )
    parser.add_argument(
        "--current",
        type=float,
        default=0.042,
        help="Current value returned by current queries, in A. Default: 0.042",
    )
    parser.add_argument(
        "--voltage",
        type=float,
        default=3.300,
        help="Voltage value returned by voltage queries, in V. Default: 3.300",
    )
    parser.add_argument(
        "--resistance",
        type=float,
        default=1000.0,
        help="Resistance value returned by resistance queries, in ohm. Default: 1000.0",
    )
    parser.add_argument(
        "--idn",
        default="BenchCI,SCPI-SIM,0001,0.1",
        help="Response for *IDN?.",
    )
    parser.add_argument(
        "--response-delay-ms",
        type=int,
        default=0,
        help="Artificial response delay in milliseconds. Default: 0",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable per-command logging.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.port <= 0 or args.port > 65535:
        raise SystemExit("--port must be between 1 and 65535")

    if args.response_delay_ms < 0:
        raise SystemExit("--response-delay-ms must be >= 0")

    config = ScpiSimConfig(
        current_a=args.current,
        voltage_v=args.voltage,
        resistance_ohm=args.resistance,
        idn=args.idn,
        response_delay_ms=args.response_delay_ms,
        verbose=not args.quiet,
    )

    if args.mode == "tcp":
        run_tcp_server(args, config)
        return

    if args.mode == "serial-pty":
        run_serial_pty(args, config)
        return

    if args.mode == "stdio":
        run_stdio(args, config)
        return

    raise SystemExit(f"Unsupported mode: {args.mode}")


if __name__ == "__main__":
    main()
from __future__ import annotations

import argparse
import logging

from pymodbus.datastore import ModbusDeviceContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server import StartSerialServer


def build_context() -> ModbusServerContext:
    """
    Build a Modbus datastore with example values.

    Register map used by the demo:

    Holding registers:
      100 -> firmware major version
      101 -> firmware minor/build version
      200 -> writable demo register

    Coils:
      10  -> writable output enable coil
    """
    coils = ModbusSequentialDataBlock(0, [False] * 256)
    discrete_inputs = ModbusSequentialDataBlock(0, [False] * 256)
    input_registers = ModbusSequentialDataBlock(0, [0] * 256)
    holding_registers = ModbusSequentialDataBlock(0, [0] * 256)

    # Demo values expected by example BenchCI suites
    holding_registers.setValues(100, [1, 42])   # version registers
    holding_registers.setValues(200, [1234])    # writable demo register
    coils.setValues(10, [True])                 # demo output coil

    device = ModbusDeviceContext(
        di=discrete_inputs,
        co=coils,
        ir=input_registers,
        hr=holding_registers,
    )

    return ModbusServerContext(devices=device, single=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BenchCI Modbus RTU slave simulator")
    parser.add_argument("--port", required=True, help="Serial port path, e.g. /dev/ttyUSB0 or COM5")
    parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    context = build_context()

    print("Starting BenchCI Modbus RTU slave simulator")
    print(f"Port: {args.port}")
    print(f"Baud: {args.baud}")
    print("Demo register map:")
    print("  Holding register 100 = 1")
    print("  Holding register 101 = 42")
    print("  Holding register 200 = 1234")
    print("  Coil 10 = True")
    print()
    print("Use Ctrl+C to stop.")

    StartSerialServer(
        context=context,
        port=args.port,
        baudrate=args.baud,
        timeout=1,
    )


if __name__ == "__main__":
    main()
# Quickstart

This guide shows a first working BenchCI setup using one node, UART output, and firmware flashing.

By the end, you will:

- flash firmware
- run an automated test suite
- validate output over UART
- collect structured results

## How BenchCI works

BenchCI uses two configuration files:

- `bench.yaml` describes the hardware bench
- `suite.yaml` defines the test logic

You then run:

```bash
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf
```

## Prerequisites

You need:

- Python 3.11+
- BenchCI installed and activated
- a board connected to your machine
- a supported flashing tool such as OpenOCD
- firmware that prints expected UART output

Run diagnostics first:

```bash
benchci doctor
```

## Step 1 — Create `bench.yaml`

Example:

```yaml
version: "1"

bench:
  name: nucleo_uart_demo
  description: Simple single-node UART bench

defaults:
  node: dut
  timeouts:
    within_ms: 1000

nodes:
  dut:
    kind: mcu
    role: target

    flash:
      backend: openocd
      interface_cfg: interface/stlink.cfg
      target_cfg: target/stm32f4x.cfg

    reset:
      method: openocd

    transports:
      console:
        backend: uart
        port: /dev/ttyUSB0
        baud: 115200
        timeout_ms: 100
```

This bench defines:

- one node named `dut`
- OpenOCD flashing
- OpenOCD reset
- one UART transport named `console`

## Step 2 — Create `suite.yaml`

Example:

```yaml
version: "1"

suite:
  name: firmware_smoke

tests:
  - name: boot_ok
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "[BOOT] OK"
          within_ms: 3000

  - name: ping
    steps:
      - send_uart:
          node: dut
          transport: console
          data: "PING\n"

      - expect_uart:
          node: dut
          transport: console
          contains: "PONG"
          within_ms: 1000
```

## Step 3 — Validate the files

```bash
benchci validate --bench bench.yaml --suite suite.yaml
```

## Step 4 — Run the suite locally

```bash
benchci run \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf
```

BenchCI will:

1. load and validate the bench
2. load and validate the suite
3. flash firmware unless `--skip-flash` is used
4. start required transports and GPIO
5. execute the test steps
6. write artifacts

## Step 5 — Inspect results

BenchCI writes artifacts into `benchci-results/`.

Typical structure:

```text
benchci-results/
└── 20260328-142200/
    ├── results.json
    └── nodes/
        └── dut/
            ├── flash.log
            └── transport-console.log
```

`results.json` contains the high-level outcome. Per-node logs contain transport, flash, and GPIO details.

## Remote quickstart

If your hardware is attached to another machine running BenchCI Agent:

```bash
benchci run \
  --agent http://192.168.1.50:8080 \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

If the Agent already has a registered bench:

```bash
benchci run \
  --agent http://192.168.1.50:8080 \
  --bench-id my-bench \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

In remote mode, the CLI downloads the final artifacts ZIP into `benchci-results/`.

## Troubleshooting

If the run fails:

- inspect `results.json`
- inspect the relevant transport log
- inspect `flash.log`
- confirm the serial/CAN/Modbus settings in `bench.yaml`
- run `benchci doctor --bench bench.yaml`

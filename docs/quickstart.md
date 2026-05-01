# Quickstart

Run your first real hardware test with BenchCI.

This guide uses the simplest useful path:

```text
firmware artifact
        ↓
benchci run
        ↓
flash board
        ↓
read UART output
        ↓
write structured results
```

By the end, you will have a local BenchCI run that flashes firmware, validates UART output, and stores logs under `benchci-results/`.

---

## What you need

- Python 3.11+
- BenchCI installed
- a board connected to your machine, for example an STM32 NUCLEO
- a supported flashing tool, for example OpenOCD
- firmware that prints expected UART output
- a serial connection to the board

Install BenchCI first:

```bash
pip install benchci
```

Log in:

```bash
benchci login
```

Check your active account and workspace:

```bash
benchci whoami
```

---

## Before writing YAML: inspect your machine

Run doctor first so you know which ports, USB devices, tools, and GPIO chips BenchCI can see:

```bash
benchci doctor
benchci doctor --ports
benchci doctor --usb
benchci doctor --tools
```

After creating `bench.yaml`, cross-check it against the current machine:

```bash
benchci doctor --bench bench.yaml
```

This is especially useful for finding the correct UART port, checking whether OpenOCD/J-Link/esptool is installed, and confirming GPIO device paths such as `/dev/gpiochip0`.

## Step 1 — Create `bench.yaml`

`bench.yaml` describes the physical hardware.

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

artifacts:
  root_dir: benchci-results
  per_node_dirs: true
```

This defines:

- one node named `dut`
- OpenOCD flashing
- OpenOCD reset
- one UART transport named `console`
- artifact output under `benchci-results/`

Adjust these fields for your board:

- `target_cfg`
- UART `port`
- UART `baud`
- optional probe serials or extra flash arguments

---

## Step 2 — Create `suite.yaml`

`suite.yaml` defines the test logic.

Example:

```yaml
version: "1"

suite:
  name: firmware_smoke
  description: Flash firmware and validate boot logs

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

This suite checks that:

- the firmware prints `[BOOT] OK`
- the device responds to `PING` with `PONG`

---

## Optional: add traceability

For a first run, a simple suite is enough. When you want evidence reports to show requirement or risk coverage, add optional traceability fields:

```yaml
suite:
  name: firmware_smoke
  description: Flash firmware and validate boot logs
  requirement_ids:
    - REQ-BOOT-001
  risk_ids:
    - RISK-BOOT-001
  tags:
    - smoke

tests:
  - name: boot_ok
    test_case_id: TC-BOOT-001
    requirement_ids:
      - REQ-BOOT-001
    risk_ids:
      - RISK-BOOT-001
    tags:
      - boot
      - uart
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "[BOOT] OK"
          within_ms: 3000
```

Traceability fields are optional. Use them when you want the run to support release, QA, or compliance evidence workflows.

## Step 3 — Validate configuration

Validate without touching hardware:

```bash
benchci validate --bench bench.yaml --suite suite.yaml
```

If validation fails, fix the config before running on the device.

---

## Step 4 — Run locally

```bash
benchci run \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --verbose
```

BenchCI will:

1. load and validate `bench.yaml`
2. load and validate `suite.yaml`
3. flash the artifact unless `--skip-flash` is used
4. start only the required transports and GPIO resources
5. execute the suite steps
6. write logs and structured results

---

## Step 5 — Inspect results

BenchCI writes artifacts into `benchci-results/`.

Typical structure:

```text
benchci-results/
└── 20260328-142200/
    ├── results.json
    ├── evidence.json
    ├── evidence.html
    ├── metadata.json
    ├── inputs/
    │   ├── bench.yaml
    │   └── suite.yaml
    └── nodes/
        └── dut/
            ├── flash.log
            └── transport-console.log
```

`results.json` contains the high-level outcome.

Per-node logs contain flash, transport, GPIO, power, or protocol logs depending on the bench and suite.

---

## Common first-run problems

### UART port is wrong

Check available ports:

```bash
ls /dev/ttyUSB* /dev/ttyACM*
```

Update `bench.yaml`.

### Permission denied on serial port

On Linux, add your user to the serial group used by your distribution, often `dialout`:

```bash
sudo usermod -aG dialout $USER
```

Then log out and back in.

### Flash tool not found

Install the required flash tool, for example:

```bash
sudo apt-get install -y openocd
```

### Boot message not found

Increase timeout or verify the firmware really prints the expected text:

```yaml
within_ms: 5000
```

---

## Next step: connect CI

Once local execution works, move to the end-to-end CI flow:

[End-to-End Example](end_to_end_example.md)

## Evidence outputs

BenchCI now writes both machine-readable and human-readable evidence:

- `results.json` — execution summary, test results, structured failures, and per-test traceability
- `evidence.json` — firmware hash, Git/CI metadata, bench/suite hashes, traceability, and artifact list
- `evidence.html` — human-readable evidence report
- `metadata.json` — supporting run metadata
- `inputs/bench.yaml` and `inputs/suite.yaml` — snapshots of the exact inputs used

Open `evidence.html` after the run when you want a report that is easier to share with a teammate, QA reviewer, or release owner.

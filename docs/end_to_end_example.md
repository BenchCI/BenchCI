# End-to-End Example: STM32 + GitHub Actions + BenchCI Cloud

This page shows the full path from firmware build to real hardware validation.

```text
STM32 firmware
    ↓
GitHub Actions build
    ↓
BenchCI Cloud run
    ↓
Cloud-connected Agent
    ↓
real hardware bench
    ↓
results + measurements + evidence in CLI + dashboard
```

---

## Goal

By the end of this example, a CI workflow will:

1. build firmware
2. upload the firmware artifact
3. ask BenchCI to run a hardware test
4. flash the board through a registered Agent
5. collect results and logs
6. show the run, evidence, traceability, and artifacts in the BenchCI dashboard

---

## Prerequisites

You need:

- a BenchCI account and active workspace
- a hardware machine connected to the DUT
- a working `bench.yaml`
- a working `suite.yaml`
- a registered cloud Agent
- a GitHub repository containing your firmware project

Verify the bench is visible:

```bash
benchci benches list
```

Example result:

```text
my-bench    online    idle
```

---

## 1. Verify local hardware execution

On the hardware-connected machine:

```bash
benchci run \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --verbose
```

Do not continue until this works locally.

This prevents CI debugging from hiding basic bench problems such as wrong UART ports, missing flash tools, invalid GPIO lines, or firmware that does not print the expected output.

---

## 2. Start the cloud Agent

On the hardware-connected machine:

```bash
benchci agent cloud \
  --backend https://api.benchci.dev \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --agent-name "STM32 Lab Agent"
```

The Agent makes outbound requests to the BenchCI backend.

Your lab machine does not need a public inbound port.

---

## 3. Add GitHub secrets

In GitHub:

```text
Settings → Secrets and variables → Actions → New repository secret
```

Add:

```text
BENCHCI_EMAIL=engineer@company.com
BENCHCI_PASSWORD=your-password
BENCHCI_API_URL=https://api.benchci.dev
BENCHCI_BENCH_ID=my-bench
```

Use a dedicated CI account when possible.

---

## 4. Add GitHub Actions workflow

Create:

```text
.github/workflows/hardware-ci.yml
```

Example:

```yaml
name: Hardware CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build-firmware:
    runs-on: ubuntu-24.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install ARM toolchain
        run: |
          sudo apt-get update
          sudo apt-get install -y make gcc-arm-none-eabi binutils-arm-none-eabi

      - name: Build firmware
        run: |
          make
          mkdir -p build
          cp path/to/firmware.elf build/firmware.elf

      - name: Upload firmware artifact
        uses: actions/upload-artifact@v4
        with:
          name: firmware
          path: build/firmware.elf

  hardware-test:
    runs-on: ubuntu-24.04
    needs: build-firmware

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download firmware artifact
        uses: actions/download-artifact@v4
        with:
          name: firmware
          path: build

      - name: Install BenchCI
        run: |
          python -m pip install --upgrade pip
          pip install --upgrade benchci

      - name: Login to BenchCI
        run: |
          benchci login \
            --email "$BENCHCI_EMAIL" \
            --password "$BENCHCI_PASSWORD" \
            --api-url "$BENCHCI_API_URL"
        env:
          BENCHCI_EMAIL: ${{ secrets.BENCHCI_EMAIL }}
          BENCHCI_PASSWORD: ${{ secrets.BENCHCI_PASSWORD }}
          BENCHCI_API_URL: ${{ secrets.BENCHCI_API_URL }}

      - name: Run hardware test
        run: |
          benchci run \
            --cloud \
            --bench-id "$BENCHCI_BENCH_ID" \
            --suite suite.yaml \
            --artifact build/firmware.elf \
            --verbose
        env:
          BENCHCI_BENCH_ID: ${{ secrets.BENCHCI_BENCH_ID }}

      - name: Upload BenchCI results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: benchci-results
          path: benchci-results/
```

Update these paths for your project:

```text
path/to/firmware.elf
suite.yaml
```

---

## 5. Push and inspect the run

After pushing:

1. GitHub builds firmware
2. the firmware artifact is passed to the hardware-test job
3. BenchCI logs in
4. BenchCI schedules the run on the selected bench
5. the Agent flashes firmware and executes the suite
6. BenchCI downloads results and evidence into `benchci-results/`
7. GitHub uploads results as workflow artifacts

---

## 6. Inspect in the dashboard

Open:

```text
https://app.benchci.dev
```

Use the dashboard to inspect:

- run status
- bench assignment
- agent assignment
- event timeline
- failure context
- artifacts

---

## Example `suite.yaml`

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

---

## Expected artifacts

BenchCI writes results into:

```text
benchci-results/
```

Typical contents include:

```text
results.json
evidence.json
evidence.html
manifest.json
flash.log
transport-*.log
gpio.log
power.log
```

The exact logs depend on your bench and suite.

---

## Evidence produced by this workflow

The hardware-test job also produces evidence artifacts:

```text
benchci-results/
├── cloud_<run_id>.zip
└── ...
```

Inside the downloaded ZIP you should find files such as:

```text
results.json
evidence.json
evidence.html
manifest.json
evidence.json
evidence.html
metadata.json
inputs/bench.yaml
inputs/suite.yaml
```

`evidence.json` records the firmware hash, Git metadata, CI job URL, bench/suite hashes, and traceability fields from `suite.yaml`. `evidence.html` is the human-readable report.

In the dashboard, open the run detail page to see the Evidence and Traceability sections.

## Why this example matters

This is the workflow BenchCI is designed for:

```text
software CI discipline
        +
real hardware validation
```

A pull request can now build firmware, schedule a real hardware run, flash a device, validate behavior, and return machine-readable results.

# BenchCI

[![Documentation](https://img.shields.io/badge/docs-available-blue)](https://docs.benchci.dev)
[![PyPI](https://img.shields.io/pypi/v/benchci)](https://pypi.org/project/benchci/)
[![Early Access](https://img.shields.io/badge/status-early--access-orange)](mailto:tech@benchci.dev)
![Hardware CI](https://img.shields.io/badge/focus-hardware%20CI-success)
![Embedded](https://img.shields.io/badge/target-embedded%20systems-blueviolet)
[![License](https://img.shields.io/badge/license-commercial-lightgrey)]()

> **Continuous Integration for real embedded hardware.**
>
> Build firmware in CI, flash a real device, run hardware tests, and get logs/results back automatically.

---

## 🎥 Demo

Watch BenchCI run real hardware tests directly from CI:

[![BenchCI Demo](https://img.youtube.com/vi/CdnzI5P9GrI/maxresdefault.jpg)](https://youtu.be/CdnzI5P9GrI)

> STM32 + Raspberry Pi + GitHub Actions  
> No simulation. Real device.

---

## 🧪 What this demo shows

- CI pipeline builds firmware  
- BenchCI schedules a real hardware bench  
- Device is flashed automatically  
- Tests run on actual hardware  
- Results and logs are returned to CI  

👉 No simulation. No mocks. Real hardware in the loop.

---

## Why BenchCI?

Most embedded testing still looks like this:

1. build firmware
2. flash the board manually
3. open a serial terminal
4. send a command
5. read logs by hand
6. repeat after every change

That works for one engineer at one desk.

It breaks when you need repeatable validation, shared benches, CI pipelines, release gates, or remote teams.

BenchCI turns real hardware into a CI-executable test target.

---

## Quickstart

```bash
pip install benchci
benchci login
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

BenchCI will:

- flash firmware
- execute your test suite on real hardware
- validate device behavior
- generate structured results and logs

Create or access your workspace from:

```text
https://app.benchci.dev
```

Read the docs:

```text
https://docs.benchci.dev
```

---

## The core idea

BenchCI separates the physical bench from the test logic:

```text
bench.yaml  -> hardware setup
suite.yaml  -> test steps
benchci run -> real hardware execution
```

---

## What BenchCI can automate

BenchCI can:

- flash firmware with OpenOCD, STM32CubeProgrammer, J-Link, or esptool
- talk to devices over UART, Modbus RTU/TCP, and CAN
- control GPIO locally or through a remote Agent
- run local tests on a hardware-connected machine
- run remote tests through a customer-managed Agent
- run cloud-scheduled tests through BenchCI Cloud
- return artifacts, logs, and structured results to CI

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

Run it:

```bash
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

---

## CI example

```bash
benchci run --cloud --bench-id my-bench --suite suite.yaml --artifact build/fw.elf
```

Typical flow:

```text
GitHub Actions / GitLab CI
        ↓
BenchCI CLI
        ↓
BenchCI Cloud
        ↓
Cloud-connected Agent
        ↓
Real hardware
        ↓
Results + artifacts
```

---

## Documentation path

Start here:

1. [Installation](https://docs.benchci.dev/installation.html)
2. [Quickstart](https://docs.benchci.dev/quickstart.html)
3. [End-to-End Example](https://docs.benchci.dev/end_to_end_example.html)
4. [GitHub Actions](https://docs.benchci.dev/github_actions.html)
5. [GitLab CI](https://docs.benchci.dev/gitlab_ci.html)

Then use the reference docs for `bench.yaml`, `suite.yaml`, CLI commands, Agent, Cloud Mode, GPIO, architecture, and security.

---

## Early access

BenchCI is currently in early access.

For onboarding, pilots, or managed hardware demos:

```text
tech@benchci.dev
```

---

## No simulation. Real device.

BenchCI is for teams that want automated validation on the hardware they actually ship.

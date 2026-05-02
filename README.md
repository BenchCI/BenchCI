# BenchCI

[![Documentation](https://img.shields.io/badge/docs-available-blue)](https://docs.benchci.dev)
[![PyPI](https://img.shields.io/pypi/v/benchci)](https://pypi.org/project/benchci/)
[![Early Access](https://img.shields.io/badge/status-early--access-orange)](mailto:tech@benchci.dev)
![Hardware CI](https://img.shields.io/badge/focus-hardware%20CI-success)
![Embedded](https://img.shields.io/badge/target-embedded%20systems-blueviolet)
[![License](https://img.shields.io/badge/license-commercial-lightgrey)]()

> **Continuous Integration for real embedded hardware.**
>
> Build firmware in CI, flash a real device, control bench resources, capture hardware metrics, and get structured logs, failure explanations, and evidence reports back automatically.

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
- Results, logs, metrics, artifacts, and evidence are returned to CI/dashboard

👉 No simulation. No mocks. Real hardware in the loop.

---

## Why BenchCI?

Most embedded testing still looks like this:

1. build firmware
2. flash the board manually
3. open a serial terminal
4. send a command
5. read logs by hand
6. copy results into a ticket or release note
7. repeat after every change

That works for one engineer at one desk.

It breaks when you need repeatable validation, shared benches, CI pipelines, release gates, traceable evidence, or remote teams.

BenchCI turns real hardware into a CI-executable test target.

---

## Quickstart

```bash
pip install benchci
benchci login
benchci doctor
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

BenchCI will:

- flash firmware
- execute your test suite on real hardware
- validate device behavior
- explain common failures with structured context
- generate structured results, logs, metrics, and evidence artifacts

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
suite.yaml  -> test steps and optional traceability
benchci run -> real hardware execution
```

A run produces artifacts such as:

```text
results.json
evidence.json
evidence.html
manifest.json
metadata.json
inputs/bench.yaml
inputs/suite.yaml
flash logs
transport logs
GPIO/power logs
measurement logs
```

`manifest.json` records generated artifacts with hashes so a run can be reviewed later with stronger integrity context.

---

## What BenchCI can automate

BenchCI can:

- flash firmware with OpenOCD, STM32CubeProgrammer, J-Link, or esptool
- talk to devices over UART, Modbus RTU/TCP, and CAN
- control GPIO locally or through a remote Agent
- control relay-backed power workflows through Power v2 resources
- capture measurements and assert metrics through Measurement v1 resources
- run local tests on a hardware-connected machine
- run remote tests through a customer-managed Agent
- run cloud-scheduled tests through BenchCI Cloud
- return artifacts, logs, structured results, and evidence reports to CI
- show run history, failure context, traceability, metrics, artifact integrity, and evidence in the dashboard

---

## Power and measurement resources

BenchCI keeps test intent separate from vendor-specific lab hardware.

In `suite.yaml`, a test can say:

```yaml
- power_cycle:
    resource: dut_power
    outlet: main
    off_ms: 1000
    on_settle_ms: 2000

- measure:
    resource: supply_current
    record_as: sleep_current_a
    unit: A
    expect_less_than: 0.150
```

In `bench.yaml`, the resource defines how that action is performed.

Power resources can be backed by GPIO, HTTP relays, generic serial relay command maps, or mocks.

Measurement resources currently support mock and HTTP-backed providers, which can be connected to custom lab controllers or instrument wrapper services. Direct SCPI instrument support is a planned next backend.

This means the suite can stay stable while the bench implementation changes from a Raspberry Pi GPIO relay to a LAN relay, serial relay, lab controller, or future instrument backend.

---

## Better failure output

BenchCI does not only return “failed.”

When possible, failures include:

```text
category
title
message
explanation
suggested checks
failed step
related artifacts
raw error
```

Example:

```text
UART expectation failed
BenchCI did not observe the expected UART output.

Suggested checks:
- Check the UART port in bench.yaml.
- Check baud rate, TX/RX wiring, and common ground.
- Confirm the firmware prints the expected text.
- Open the transport log artifact.
```

This makes hardware CI failures easier to debug from the CLI, artifacts, and dashboard.

---

## Evidence reports and traceability

Every run can generate structured evidence for QA, release, and audit-friendly workflows.

Evidence includes:

- firmware filename and SHA256
- bench configuration hash
- suite hash
- Git commit, branch, remote, and dirty state
- CI provider and CI job URL when available
- run status and summary
- structured failure details
- captured metrics and measurements
- input snapshots
- artifact list
- artifact manifest with SHA256 hashes

Suites can optionally include traceability metadata:

```yaml
version: "1"

suite:
  name: firmware_smoke
  version: "1.0.0"
  release_id: "fw-0.3.5"
  requirement_ids:
    - REQ-BOOT-001
  risk_ids:
    - RISK-BOOT-001
  tags:
    - smoke
    - hardware

tests:
  - name: boot_ok
    test_case_id: TC-BOOT-001
    requirement_ids:
      - REQ-BOOT-001
    risk_ids:
      - RISK-BOOT-001
    tags:
      - uart
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "[BOOT] OK"
          within_ms: 3000
```

This creates a practical chain:

```text
requirement -> test case -> real hardware run -> evidence artifact
```

BenchCI helps produce structured verification evidence. It does not by itself certify a product or replace your company’s compliance process.

---

## Simple `suite.yaml`

Traceability is optional. A minimal suite can stay simple:

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

## Simple measurement example

Measurement steps can record values into run metrics and assert thresholds.

```yaml
version: "1"

suite:
  name: low_power_smoke

tests:
  - name: sleep_current_limit
    steps:
      - measure:
          resource: supply_current
          record_as: sleep_current_a
          unit: A
          expect_less_than: 0.150

      - assert_metric:
          name: sleep_current_a
          expect_less_than_or_equal: 0.150
```

The measurement resource itself is defined in `bench.yaml`, for example as a mock during development or an HTTP-backed lab controller in a real bench.

---

## Diagnostics

Use `benchci doctor` before running on hardware:

```bash
benchci doctor
benchci doctor --ports
benchci doctor --usb
benchci doctor --tools
benchci doctor --bench bench.yaml
```

Doctor helps identify:

- available serial ports
- USB devices such as ST-Link, USB-UART, USB-RS485, and relays
- GPIO chips on Linux machines
- missing tools such as OpenOCD, J-Link, STM32CubeProgrammer, or esptool
- bench.yaml references that do not match the local machine

This is especially useful when creating or debugging `bench.yaml`.

---

## CI example

```bash
benchci run --cloud --bench-id my-bench --suite suite.yaml --artifact build/fw.elf --verbose
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
Results + logs + evidence
```

Cloud runs can be inspected from:

```text
https://app.benchci.dev
```

The dashboard shows:

- workspace health
- online/offline benches
- queued/running runs
- recent failures
- run timeline
- structured failure context
- evidence summary
- captured metrics and measurements
- requirement/test/risk traceability
- artifact manifest status
- artifact download

---

## Examples

The public examples are designed to be mixed:

- simple examples for learning the basic model
- moderate examples for realistic hardware flows
- traceability examples for evidence-oriented workflows

Current example folders:

```text
examples/
├── 01-esp32-esptool-uart-traceable
├── 02-modbus-rtu-plc-simple
├── 03-modbus-tcp-gateway-traceable
├── 04-gateway-jlink-provisioning-moderate
├── 05-local-gpio-reset-ready-advanced
├── 06-multi-node-uart-simple
├── 07-remote-gpio-power-cycle-moderate
├── 08-can-ecu-handshake-simple
├── 09-stm32wl-boot-validation-traceable
├── 10-generic-serial-power-relay
├── 11-http-power-relay
├── 12-mock-power-control
├── 13-http-measurement
└── 14-http-measurement-mock
```

Each folder contains:

```text
bench.yaml
suite.yaml
```

Use them as templates and replace hardware-specific values such as ports, IP addresses, GPIO lines, probe serials, and firmware paths.

---

## Documentation path

Start here:

1. [Installation](https://docs.benchci.dev/installation.html)
2. [Quickstart](https://docs.benchci.dev/quickstart.html)
3. [End-to-End Example](https://docs.benchci.dev/end_to_end_example.html)
4. [Evidence Reports](https://docs.benchci.dev/evidence_reports.html)
5. [Power Resources](https://docs.benchci.dev/power_resources.html)
6. [Measurement Resources](https://docs.benchci.dev/measurement_resources.html)
7. [GitHub Actions](https://docs.benchci.dev/github_actions.html)
8. [GitLab CI](https://docs.benchci.dev/gitlab_ci.html)

Then use the reference docs for `bench.yaml`, `suite.yaml`, CLI commands, Agent, Cloud Mode, GPIO, architecture, dashboard, examples, and security.

---

## Current direction

BenchCI 0.6.0 focuses on:

- Power v2 resources for cleaner bench-level power control
- Measurement v1 resources for captured metrics and threshold assertions
- stronger evidence artifacts with `manifest.json`
- dashboard visibility for metrics, traceability, and artifact integrity

BenchCI is still intentionally lightweight compared with large HiL platforms. The goal is to make real hardware validation practical inside everyday CI workflows.

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

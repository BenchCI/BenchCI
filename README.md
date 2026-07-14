# BenchCI

[![Documentation](https://img.shields.io/badge/docs-available-blue)](https://docs.benchci.dev)
[![PyPI](https://img.shields.io/pypi/v/benchci)](https://pypi.org/project/benchci/)
[![Stable](https://img.shields.io/badge/status-stable-success)](https://docs.benchci.dev)
![Compliance Evidence](https://img.shields.io/badge/focus-compliance%20evidence-success)
![Hardware CI](https://img.shields.io/badge/plus-hardware%20CI-blue)
![Embedded](https://img.shields.io/badge/target-embedded%20systems-blueviolet)
[![License](https://img.shields.io/badge/license-commercial-lightgrey)]()

> **Compliance evidence and hardware CI for real embedded systems.**
>
> Build firmware in CI, test it on a real device, and return structured results, failure context, measurements, traceability, and release evidence automatically.

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

BenchCI turns real hardware into a CI-executable test target and evidence source. Teams with existing pytest or labgrid automation can keep those workflows and import their results into BenchCI for dashboards, release matrices, and evidence packages.

---

## Quickstart

Local runs are **free and need no account** — this works on your bench, today:

```bash
pip install benchci
benchci doctor
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

For cloud features — shared benches, scheduling, run history, sign-off, and release
evidence workflows — create a workspace and log in. New workspaces start a **30-day trial
of Team features**; plans are published at [benchci.dev/#pricing](https://benchci.dev/#pricing).

```bash
benchci login
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
- talk to devices over UART, Modbus RTU/TCP, classic CAN/CAN FD over Linux SocketCAN, I2C, and SPI
- run bounded fuzz tests against UART, CAN, and Modbus transports
- control GPIO locally or through a remote Agent
- control relay-backed power workflows through Power resources
- capture measurements and assert metrics through Measurement resources
- run local tests on a hardware-connected machine
- run remote tests through a customer-managed Agent
- run cloud-scheduled tests through BenchCI Cloud
- return artifacts, logs, structured results, and evidence reports to CI
- show run history, failure context, traceability, metrics, artifact integrity, and evidence in the dashboard
- export canonical JUnit XML and CTRF
- import existing JUnit/CTRF workflows from pytest, labgrid, Robot Framework, or custom harnesses
- upload LCOV coverage alongside hardware-test evidence
- create release evidence bundles, record review decisions, and download human-readable QA reports
- highlight recent bench reliability and test flakiness patterns without overriding the underlying test result
- trigger existing HIL rigs and simulators through bench-owner-approved commands or HTTP APIs (`run_external`), collecting their reports into the same evidence flow
- run controlled fault-injection steps (experimental) with allow-listed glitches and bounded recovery checks
- verify DUT identity through optional UART self-identification before the first test

Cloud workspaces can also choose how firmware reaches an Agent: brokered upload, deletion after Agent fetch, or a customer-controlled URL with Agent-side SHA256 verification. See [Firmware Handling Assurance](https://docs.benchci.dev/firmware-handling-assurance.html) for the security model and operational tradeoffs.

### Flash artifact support

| Backend | Downloadable file types | Address requirement |
| --- | --- | --- |
| OpenOCD | `.elf`, `.hex`, `.bin` | `.bin` requires `flash.address`. |
| STM32CubeProgrammer | `.elf`, `.hex`, `.bin` | `.bin` requires `flash.address`. |
| J-Link | `.elf`, `.hex`, `.bin` | `.bin` requires `flash.address`. |
| esptool | `.bin` single-image downloads | `.bin` requires `flash.address`. |

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

Measurement resources support mocks, HTTP lab-controller readings, `scpi_measurement`, `scpi_power_supply_measurement`, and simple serial sensors. SCPI resources can use TCP addresses such as `tcp://192.168.1.50:5025`, serial addresses such as `serial:///dev/ttyUSB0`, or VISA/USBTMC resource strings when the optional instrument dependencies are installed. See [docs/examples.md](docs/examples.md) for SCPI examples.

This means the suite can stay stable while the bench implementation changes from a Raspberry Pi GPIO relay to a LAN relay, serial relay, lab controller, SCPI instrument, or future instrument backend.

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

## Release evidence and reliability

Completed cloud runs can be grouped into a release evidence bundle:

```bash
benchci releases create "Firmware v1.2.3" --runs RUN_ID_1,RUN_ID_2
benchci releases download BUNDLE_ID --out release-v1.2.3.zip
benchci releases report BUNDLE_ID --template generic-qa --format pdf
```

Bundles connect selected run evidence, firmware hashes, DUT identity, review history, coverage summaries, and requirement traceability. Report templates include Generic QA, IEC 62304-style, and ISO 26262-style formats. These are review aids—not certifications or substitutes for your organization’s approval process.

`benchci runs show` and `benchci benches show` also surface recent pass, failure, infrastructure-failure, and flaky-test patterns. Reliability warnings help you decide whether to investigate firmware and test logic or the fixture, cabling, adapters, Agent host, and other bench infrastructure.

Already have a test harness? Import its result instead of rewriting it:

```bash
benchci runs create-external \
  --name "hardware nightly" \
  --junit report.xml \
  --artifacts artifacts/ \
  --framework pytest
```

Native BenchCI runs and imported runs can be included in the same release bundle.

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

The measurement resource itself is defined in `bench.yaml`, for example as an HTTP-backed lab controller, SCPI instrument, I2C power monitor, or serial sensor.

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
- LCOV coverage summary when attached
- imported JUnit/CTRF source information
- recent bench reliability and test flakiness context
- artifact manifest status
- artifact download
- release review status and compliance-style report downloads
- customer request intake and triage status

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
├── 12-http-measurement
├── 13-scpi
├── 14-low-power-current
├── 15-protocol-fuzzing
├── 16-i2c-spi-registers
├── 17-station-i2c-spi-smoke
├── 18-traceable-release-smoke
├── 19-boundary-value-threshold
└── 20-state-transition-update-flow
```

Most numbered folders contain:

```text
bench.yaml
suite.yaml
```

Use them as templates and replace hardware-specific values such as ports, IP addresses, GPIO lines, probe serials, and firmware paths.

The Station I2C/SPI templates require you to supply the correct bus, device, register, response, wiring, and electrical-level values for your fixture. Validate those values safely on your own hardware before treating the resulting runs as release evidence.

---

## Documentation path

Start here:

1. [Installation](https://docs.benchci.dev/installation.html)
2. [Quickstart](https://docs.benchci.dev/quickstart.html)
3. [End-to-End Example](https://docs.benchci.dev/end_to_end_example.html)
4. [Evidence Reports](https://docs.benchci.dev/evidence_reports.html)
5. [QA Evidence Workflow](https://docs.benchci.dev/qa_evidence_workflow.html)
6. [BenchCI and the Test Process](https://docs.benchci.dev/test_process.html)
7. [External Test Bridge Workflow](https://docs.benchci.dev/external-test-bridge-workflow.html)
8. [Firmware Handling Assurance](https://docs.benchci.dev/firmware-handling-assurance.html)
9. [Power Resources](https://docs.benchci.dev/power_resources.html)
10. [Measurement Resources](https://docs.benchci.dev/measurement_resources.html)
11. [GitHub Actions](https://docs.benchci.dev/github_actions.html)
12. [GitLab CI](https://docs.benchci.dev/gitlab_ci.html)
13. [JUnit/CTRF Import Guide](https://docs.benchci.dev/junit-ctrf-import-guide.html)
14. [HIL Rig Orchestration](https://docs.benchci.dev/hil-orchestration.html)

Then use the reference docs for `bench.yaml`, `suite.yaml`, CLI commands, Agent, Cloud Mode, GPIO, architecture, dashboard, examples, and security.

---

## Current product surface

BenchCI includes:

- local, Agent, and Cloud execution modes
- UART, Modbus RTU/TCP, classic CAN/CAN FD over Linux SocketCAN, I2C, SPI, GPIO, flash, power, measurement, and bounded fuzzing workflows
- Power resources for bench-level relay and power control
- Measurement resources for captured metrics and threshold assertions
- structured failures, evidence reports, artifact manifests, release bundles, review history, and compliance-style report templates
- external JUnit/CTRF imports, canonical exports, and LCOV coverage summaries
- firmware-handling controls with Agent-side SHA256 verification for customer-controlled URLs
- recent bench reliability and flaky-test investigation aids
- HIL rig orchestration (`run_external`), controlled fault injection (experimental), and verified DUT identity
- authenticator (TOTP) MFA with recovery codes, plus run-failure and release-approval email notifications
- workspace, billing, Agent, bench, run, dashboard, and QA evidence workflows

BenchCI stays intentionally lightweight compared with large HiL platforms. The goal is to make real hardware validation practical inside everyday CI workflows.

For commercial onboarding, pilots, or managed hardware demos:

```text
tech@benchci.dev
```

---

## Support, issues, and contributions

- Bugs and feature requests: [GitHub issues](../../issues/new/choose) — open to everyone, on any plan.
- Support commitments per plan: [SUPPORT.md](SUPPORT.md).
- Docs and example contributions are welcome: [CONTRIBUTING.md](CONTRIBUTING.md).
- Release highlights: [CHANGELOG.md](CHANGELOG.md).
- Everything in `examples/` and `tools/` is MIT-licensed — copy freely into your own projects ([LICENSE](LICENSE)).

---

## No simulation. Real device.

BenchCI is for teams that want automated validation on the hardware they actually ship.

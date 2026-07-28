# BenchCI Documentation

## Hardware CI for embedded systems

BenchCI lets embedded teams flash firmware, run tests on real devices, orchestrate existing HIL rigs from CI, return results to CI, and preserve review-ready verification evidence.

```bash
benchci run --cloud --bench-id my-bench --suite suite.yaml --artifact build/fw.elf
```

No simulation. No manual serial-terminal testing. Real hardware in the loop.

---

## The problem BenchCI solves

Most embedded validation still depends on manual bench work:

- flash firmware by hand
- open a terminal
- send commands manually
- watch logs
- copy results into a ticket or release note

That is fine for early bring-up.

It is not enough for repeatable CI, shared hardware, pull-request validation, release gates, or remote teams.

---

## What BenchCI gives you

BenchCI turns hardware validation into a repeatable CI workflow:

```text
CI builds firmware
        ↓
BenchCI schedules a hardware run
        ↓
Agent flashes and tests a real device
        ↓
Results, logs, artifacts, and evidence return to CI/dashboard
        ↓
Optional release review packages can collect runs, coverage, identity, and sign-off history
```

You can start locally, then move the same test model to a remote Agent or BenchCI Cloud.

---

## Fastest path

If you already have a board connected to your machine:

```bash
pip install benchci
benchci login
benchci init --preset flash-uart
benchci doctor --bench bench.yaml
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf
```

BenchCI will load your hardware configuration, flash the firmware, run the suite, and write results under `benchci-results/`.

If you prefer to start in the browser, the dashboard Config Builder can export starter `bench.yaml` and `suite.yaml` files for the same preset-based flows.

---

## Core mental model

```text
bench.yaml  -> describes the hardware
suite.yaml  -> describes the test logic
benchci run -> executes the suite on real hardware
```

Use `benchci init --list-presets` to see starter configs for UART smoke tests, flash + UART flows, GPIO reset/ready checks, power cycling, measurements, CAN, Modbus, and bounded protocol fuzzing. The generated files are intentionally editable YAML, not a hidden cloud configuration.

<!-- Unreleased hardware builder/docs are intentionally hidden until release. -->

A **bench** is your physical setup: DUT, debugger, UART/CAN/Modbus adapters, GPIO, relays, power controllers, measurement instruments, and related resources.

A **suite** is what should happen: flash, reset, send commands, wait for logs, read registers, check GPIO, validate CAN frames, run bounded fuzzing, cycle power, take measurements, and assert metrics.

An **Agent** is the hardware-connected process that lets CI or remote users run tests without sitting next to the device.

BenchCI **Cloud Mode** adds workspace-aware scheduling, shared/private benches, dashboard visibility, and CI-friendly execution.

---

## Recommended path for new users

1. [Installation](installation.md)
2. [Quickstart](quickstart.md)
3. [End-to-End Example](end_to_end_example.md)
4. [Agent](agent.md)
5. [Cloud Mode](cloud.md)
6. [GitHub Actions](github_actions.md) or [GitLab CI](gitlab_ci.md)

Reference pages are available after the getting-started flow.

---

## What BenchCI supports today

Communication:

- UART
- Modbus RTU
- Modbus TCP
- CAN
- I2C (bus scan, register read/write, expect)
- SPI (full-duplex transfer, expect)
- bounded UART/CAN/Modbus protocol fuzzing
- experimental allow-listed power, GPIO, and malformed-UART-byte fault injection

Flashing:

- OpenOCD
- STM32CubeProgrammer
- SEGGER J-Link
- esptool

Control:

- Linux GPIO
- remote GPIO through Agent
- GPIO-backed power control
- HTTP relay control
- serial relay command maps
- allow-listed external simulator/HIL triggers through wrapper commands or HTTP APIs

Power control is exposed through bench-level resources, so suites use generic steps such as `power_cycle` while `bench.yaml` defines the concrete GPIO, HTTP, or serial relay backend.

Measurements:

- HTTP/lab-controller measurement resources
- SCPI measurement resources over TCP/IP, serial/RS232, and USB/VISA-style instruments
- SCPI power-supply current/voltage readback with conservative presets
- I2C power-monitor measurements
- script and serial measurement resources
- recorded metrics and threshold assertions

Measurement follows the same bench-level resource pattern, so suites use generic `measure` steps while `bench.yaml` defines the concrete measurement backend.

Evidence and traceability:

- `evidence.json` machine-readable run evidence
- `evidence.html` human-readable evidence reports
- input snapshots of `bench.yaml` and `suite.yaml`
- firmware, suite, and bench config hashes
- optional requirement, test case, risk, release, and tag metadata
- structured failure explanations and suggested checks
- artifact `manifest.json` with SHA256 hashes
- captured measurements and metrics
- fuzz campaign summaries, seeds, first failing cases, and JSONL case logs when fuzzing is used
- configured or UART-verified DUT identity
- LCOV summaries attached from unit tests or simulation
- firmware handling mode, SHA256 verification, deletion state, and audit events
- imported JUnit/CTRF results and authenticated external artifacts
- orchestrated external/HIL result evidence through `run_external`
- experimental controlled fault-injection recovery evidence
  - optional release bundles with coverage matrices, review sign-off, and HTML/PDF reports
- recent reliability history, flaky-test warnings, and advisory failure assessments

Execution:

- local runs
- direct Agent runs
- backend-controlled Cloud Mode runs

---

## Documentation

### Getting Started

```{toctree}
:maxdepth: 1
:caption: Getting started

installation.md
quickstart.md
end_to_end_example.md
agent.md
cloud.md
cloud_agent_health.md
github_actions.md
gitlab_ci.md
```

### Core Reference

```{toctree}
:maxdepth: 1
:caption: Core reference

bench_config.md
suite_config.md
fuzzing.md
power_resources.md
measurement_resources.md
i2c-spi-station-wiring.md
dut-self-identification.md
fault-injection.md
evidence_reports.md
evidence-integrity.md
junit-ctrf-import-guide.md
hil-orchestration.md
pytest-on-bench.md
cli.md
diagnostics.md
examples.md
dashboard.md
architecture.md
linux_gpio.md
security.md
faq.md
owner_operations.md
```

### Advanced Assurance Workflows

```{toctree}
:maxdepth: 1
:caption: Advanced assurance workflows

qa_evidence_workflow.md
test_process.md
static_testing.md
test_design_techniques.md
external-test-bridge-workflow.md
firmware-handling-assurance.md
```

# BenchCI Documentation

## Run real hardware tests from CI

BenchCI lets embedded teams flash firmware, run tests on real devices, and return logs/results to CI automatically.

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
Results, logs, artifacts, and evidence reports return to CI/dashboard
```

You can start locally, then move the same test model to a remote Agent or BenchCI Cloud.

---

## Fastest path

If you already have a board connected to your machine:

```bash
pip install benchci
benchci login
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

BenchCI will load your hardware configuration, flash the firmware, run the suite, and write results under `benchci-results/`.

---

## Core mental model

```text
bench.yaml  -> describes the hardware
suite.yaml  -> describes the test logic
benchci run -> executes the suite on real hardware
```

A **bench** is your physical setup: DUT, debugger, UART/CAN/Modbus adapters, GPIO, relays, power controllers, measurement instruments, and related resources.

A **suite** is what should happen: flash, reset, send commands, wait for logs, read registers, check GPIO, validate CAN frames, cycle power, take measurements, and assert metrics.

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

Flashing:

- OpenOCD
- STM32CubeProgrammer
- SEGGER J-Link
- esptool

Control:

- Linux GPIO
- remote GPIO through Agent
- mock GPIO
- generic bench-level power resources
- GPIO-backed power control
- HTTP relay control
- serial relay command maps

Measurements:

- mock measurement resources
- HTTP/lab-controller measurement resources
- suite-level `measure` steps
- recorded metrics and threshold assertions

Evidence and traceability:

- `evidence.json` machine-readable run evidence
- `evidence.html` human-readable evidence reports
- input snapshots of `bench.yaml` and `suite.yaml`
- firmware, suite, and bench config hashes
- optional requirement, test case, risk, release, and tag metadata
- structured failure explanations and suggested checks
- artifact `manifest.json` with SHA256 hashes
- captured measurements and metrics

Execution:

- local runs
- direct Agent runs
- backend-controlled Cloud Mode runs

---

## Documentation

```{toctree}
:maxdepth: 1

installation.md
quickstart.md
end_to_end_example.md
agent.md
cloud.md
github_actions.md
gitlab_ci.md
bench_config.md
suite_config.md
power_resources.md
measurement_resources.md
evidence_reports.md
cli.md
examples.md
dashboard.md
architecture.md
linux_gpio.md
security.md
faq.md
owner_operations.md
```

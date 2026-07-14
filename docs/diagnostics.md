# Validation, Self-Test, and Dry-Run Planning

Use this page before running hardware tests, especially when bringing up a new bench or preparing a CI workflow.

BenchCI now separates three different questions:

```text
benchci validate        -> Is my YAML structurally and logically valid?
benchci benches self-test -> Is my physical bench infrastructure ready?
benchci run --dry-run-plan -> What would this run do before touching hardware?
```

This workflow helps you catch configuration mistakes, missing tools, bad ports, broken GPIO mappings, missing power/measurement resources, and surprising execution plans before a real hardware run starts.

---

## Recommended local readiness workflow

Run these commands on the hardware-connected machine:

```bash
benchci validate --bench bench.yaml --suite suite.yaml

benchci benches self-test   --bench bench.yaml   --open-hardware   --log-dir bench-health

benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/firmware.elf   --dry-run-plan

benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/firmware.elf
```

Use this order when:

- setting up a new bench
- changing `bench.yaml`
- changing `suite.yaml`
- moving from local execution to Agent or Cloud Mode
- debugging why CI runs are queued, blocked, or failing
- collecting bench readiness evidence before a customer/demo run

---

## 1. Validate YAML and cross-file compatibility

```bash
benchci validate --bench bench.yaml --suite suite.yaml
```

`validate` does not touch hardware. It checks whether the files are valid and whether the suite makes sense for the bench.

It can catch issues such as:

- invalid bench or suite schema
- unknown node references
- missing transport references
- wrong transport backend usage
- missing GPIO lines
- GPIO direction mismatches
- flash steps on nodes without flash config
- missing flash artifact warnings
- missing power resources or outlets
- missing measurement resources
- `assert_metric` referencing a metric that was not recorded earlier

You can also validate one file at a time:

```bash
benchci validate --bench bench.yaml
benchci validate --suite suite.yaml
```

### JSON output

Use JSON output in automation:

```bash
benchci validate   --bench bench.yaml   --suite suite.yaml   --json
```

Write validation output to a file:

```bash
benchci validate   --bench bench.yaml   --suite suite.yaml   --output validation.json
```

---

## 2. Run a benches self-test

```bash
benchci benches self-test --bench bench.yaml
```

Self-test checks whether the bench definition and local machine are ready for real hardware execution.

Static self-test checks include:

- bench file loading
- default node validation
- flash backend/tool checks
- reset method/tool checks
- serial/CAN path or interface checks
- GPIO configuration checks
- power resource configuration checks
- measurement resource configuration checks

The command reports a health status:

```text
healthy
degraded
failing
unknown
```

### Non-destructive hardware-open mode

```bash
benchci benches self-test --bench bench.yaml --open-hardware
```

This opens configured interfaces and immediately closes them.

It does **not**:

- flash firmware
- reset the target
- toggle relays
- power-cycle outlets
- drive GPIO outputs
- send UART/CAN/Modbus commands

Use this when you want to catch missing permissions, disconnected USB devices, bad serial ports, unavailable GPIO chips, or unreachable resource drivers before running a real suite.

### Optional read-only deeper checks

```bash
benchci benches self-test   --bench bench.yaml   --open-hardware   --read-inputs

benchci benches self-test   --bench bench.yaml   --open-hardware   --read-measurements
```

Use these only when reading inputs or measurements is safe for your bench.

---

## 3. Save self-test logs

Use `--log-dir` when you want reusable diagnostic evidence:

```bash
benchci benches self-test   --bench bench.yaml   --open-hardware   --log-dir bench-health
```

Typical output:

```text
bench-health/
  self-test.log
  self-test-summary.json
  nodes/
    dut/
      transport-console.log
      gpio.log
  resources/
    dut_power/
      power.log
    supply_current/
      measurement.log
```

These files are useful for:

- bench bring-up notes
- customer onboarding
- lab owner troubleshooting
- CI readiness checks
- before/after comparison when fixing hardware

---

## 4. Preview the execution plan

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/firmware.elf   --dry-run-plan
```

Dry-run planning prints what BenchCI would execute without touching hardware.

It shows:

- bench and suite paths
- validation status
- flash enabled/skipped state
- resolved artifact source
- ordered suite steps
- node/transport/GPIO/power/measurement usage
- timeout resolution
- metrics recorded/asserted
- final resource summary

Use `--skip-flash` to preview a run that intentionally does not flash:

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --skip-flash   --dry-run-plan
```

### JSON plan output

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/firmware.elf   --dry-run-plan   --json
```

Write the plan to a file:

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/firmware.elf   --dry-run-plan   --plan-output plan.json
```

---

## How these commands differ from `doctor`

`benchci doctor` inspects the machine and environment.

Examples:

```bash
benchci doctor
benchci doctor --port /dev/ttyUSB0 --baud 115200
benchci doctor --bench bench.yaml
benchci doctor --agent http://agent-host:8080
benchci doctor --json
benchci doctor --export doctor-report.zip
```

Use `doctor` to discover what the machine can see.

Use `validate`, `benches self-test`, and `dry-run-plan` to check whether a specific BenchCI bench/suite/run is ready.

A useful mental model:

```text
doctor           -> What does this machine have?
validate         -> Are my YAML files valid and compatible?
benches self-test -> Is this configured bench ready?
dry-run plan     -> What will this exact run do?
run              -> Execute the hardware test.
```

---

## Troubleshooting quick guide

| Symptom | First command to run |
|---|---|
| YAML does not load | `benchci validate --bench bench.yaml --suite suite.yaml` |
| Suite references wrong node/transport | `benchci validate --bench bench.yaml --suite suite.yaml` |
| UART path may be wrong | `benchci doctor` or `benchci doctor --port <device>`, then `benchci benches self-test --open-hardware` |
| GPIO line may be wrong | `benchci doctor --bench bench.yaml`, then `benchci benches self-test --open-hardware --read-inputs` |
| Flash tool may be missing | `benchci doctor`, then `benchci benches self-test` |
| Power resource may be missing | `benchci benches self-test --open-hardware --log-dir bench-health` |
| Measurement resource may be wrong | `benchci benches self-test --open-hardware --read-measurements` |
| You are unsure what a run will do | `benchci run --dry-run-plan ...` |

---

## Recommended CI preflight

For a hardware-connected self-hosted runner, add a preflight job before the real hardware test:

```bash
benchci validate --bench bench.yaml --suite suite.yaml
benchci benches self-test --bench bench.yaml --open-hardware --log-dir bench-health
benchci run --bench bench.yaml --suite suite.yaml --artifact build/firmware.elf --dry-run-plan
```

For BenchCI Cloud Mode, run `validate` and `dry-run-plan` locally when possible, and rely on the cloud Agent health status to decide whether the bench is eligible for scheduling.

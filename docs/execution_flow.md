# Execution Flow

This document explains how BenchCI executes tests in **Direct Mode** and **Cloud Mode**, and what commands are typically used at each step.

BenchCI uses the same core execution engine in every mode:

```text
bench.yaml + suite.yaml
        ↓
   benchci run
        ↓
    run_local(...)
        ↓
 real hardware bench
        ↓
 logs + results.json
```

The difference is **where** that execution happens and **how** the CLI reaches the hardware.

---

## Overview

BenchCI always starts from the CLI.

Typical entry points are:

```bash
benchci login
benchci run ...
```

From there, execution follows one of these paths:

- **Direct Mode** → customer-owned hardware accessed locally or through a customer-managed Agent
- **Cloud Mode** → BenchCI backend control plane + BenchCI-managed Agent + BenchCI-managed hardware

---

## Direct Mode

Direct Mode is used when the hardware bench belongs to the customer.

This can be:

- fully local execution on the same machine as the hardware
- remote execution through a customer-managed BenchCI Agent

### Direct Mode — local execution

In local execution, the CLI calls the runner on the same machine that is connected to the hardware.

#### Command

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/fw.elf
```

#### Flow

```text
User / CI
   ↓
BenchCI CLI
   ↓
run_local(...)
   ↓
local hardware
   ↓
results.json + logs
```

### Direct Mode — Agent execution

In Agent execution, the customer runs a BenchCI Agent on the hardware machine and the CLI submits runs to that Agent.

#### Start the Agent

```bash
benchci agent serve
```

Optional authenticated mode:

```bash
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

#### Uploaded-bench run

```bash
benchci run   --agent http://agent-host:8080   --bench bench.yaml   --suite suite.yaml   --artifact build/fw.elf   --token "$BENCHCI_AGENT_TOKEN"
```

#### Registered-bench run

```bash
benchci run   --agent http://agent-host:8080   --bench-id my-bench   --suite suite.yaml   --artifact build/fw.elf   --token "$BENCHCI_AGENT_TOKEN"
```

#### Flow

```text
User / CI
   ↓
BenchCI CLI
   ↓
customer-managed BenchCI Agent
   ↓
customer-owned hardware
   ↓
Agent artifacts ZIP
   ↓
BenchCI CLI downloads ZIP
```

---

## Cloud Mode

Cloud Mode is used when the execution path goes through the BenchCI backend control plane and a BenchCI-managed Agent/bench.

This mode is intended for shared managed benches and remote hardware access through the backend scheduler.

### Typical commands

#### Login to the backend

```bash
benchci login --api-url https://your-backend.example.com
```

#### List available cloud benches

```bash
benchci benches list
```

#### Show one cloud bench

```bash
benchci benches show my-cloud-bench
```

#### Submit a run to a specific cloud bench

```bash
benchci run   --cloud   --bench-id my-cloud-bench   --suite suite.yaml   --artifact build/fw.elf
```

#### Submit a run using scheduler requirements

```bash
benchci run   --cloud   --tag uart   --transport uart   --flash-backend openocd   --suite suite.yaml   --artifact build/fw.elf
```

#### Inspect cloud runs

```bash
benchci runs list
benchci runs show <RUN_ID>
benchci runs events <RUN_ID>
```

### Flow

```text
User / CI
   ↓
BenchCI CLI
   ↓
BenchCI Backend
   ↓
Queue / Scheduler
   ↓
BenchCI-managed Agent
   ↓
BenchCI-managed hardware
   ↓
artifacts uploaded to backend
   ↓
BenchCI CLI downloads ZIP
```

---

## Uploaded bench vs registered bench vs cloud bench

### Uploaded bench

The CLI uploads the full bench definition together with the suite and optional artifact.

Example:

```bash
benchci run   --agent http://agent-host:8080   --bench bench.yaml   --suite suite.yaml   --artifact build/fw.elf
```

Use this when:

- you want quick ad-hoc remote execution
- you do not want to pre-register the bench on the Agent

### Registered bench

The Agent already knows the bench and you refer to it by `bench_id`.

Example:

```bash
benchci run   --agent http://agent-host:8080   --bench-id my-bench   --suite suite.yaml   --artifact build/fw.elf
```

Use this when:

- the bench is stable
- the hardware machine is reused
- you want cleaner CI pipelines

### Cloud bench

The backend knows the bench through the cloud Agent inventory and scheduling model.

Example:

```bash
benchci run   --cloud   --bench-id my-cloud-bench   --suite suite.yaml   --artifact build/fw.elf
```

Use this when:

- benches are managed through the backend
- users should not talk directly to the hardware machine
- you want centralized scheduling and artifact access

---

## Run lifecycle

BenchCI runs typically move through these states:

- `queued`
- `preparing`
- `running`
- `uploading_artifacts`
- `done`
- `failed`

Direct Agent mode and Cloud mode both use this general lifecycle.

---

## Artifacts

BenchCI produces structured artifacts such as:

- `results.json`
- transport logs
- `flash.log`
- `gpio.log`

Local runs write a normal result directory under `benchci-results/`.

Agent and Cloud runs package the result directory into a ZIP and return it to the CLI.

Typical examples:

```text
benchci-results/
benchci-results/agent_<run_id>.zip
benchci-results/cloud_<run_id>.zip
```

---

## Summary

BenchCI can currently be used in these practical ways:

| Mode | Control path | Hardware ownership | Typical command |
|---|---|---|---|
| Local Direct | CLI → runner | customer-owned | `benchci run --bench ...` |
| Remote Direct | CLI → Agent | customer-owned | `benchci run --agent ...` |
| Cloud | CLI → Backend → Agent | BenchCI-managed or backend-managed shared bench | `benchci run --cloud ...` |

The important point is that **the same bench/suite model stays consistent** while the deployment model changes.

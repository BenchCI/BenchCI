# BenchCI Architecture

BenchCI is a hardware validation platform for embedded systems. It combines a local execution engine with an optional remote Agent control plane.

## Main components

### CLI

The CLI is the user-facing entry point. It can:

- validate configs
- authenticate with the BenchCI backend
- run suites locally
- submit suites to a remote Agent
- submit suites through the backend cloud control path
- list cloud benches
- inspect cloud runs
- download remote artifacts
- start an Agent process

### Runner

`run_local(...)` is the core execution engine. It:

- loads `bench.yaml` and `suite.yaml`
- cross-validates the suite against the bench
- discovers required nodes, transports, and GPIO
- starts only the resources required by the suite
- dispatches steps
- writes structured results

### Agent

The Agent adds:

- registered bench inventory
- run queueing
- per-bench locking
- remote execution
- event storage
- artifact serving
- remote GPIO services

### Backend

The BenchCI backend handles:

- license activation
- token refresh
- license/session status
- cloud bench inventory
- cloud run submission
- scheduling and assignment
- agent polling and cloud artifact return

## High-level flow

```text
Developer / CI
      ↓
 BenchCI CLI
      ↓
local runner, Agent, or backend-controlled cloud path
      ↓
 real hardware bench
      ↓
 logs + results
```

## Local execution flow

```text
bench.yaml + suite.yaml
        ↓
   benchci run
        ↓
    run_local(...)
        ↓
 start transports / GPIO
        ↓
 execute steps
        ↓
   results.json + logs
```

## Remote execution flow

```text
Developer / CI
      ↓
 BenchCI CLI
      ↓
 BenchCI Agent API
      ↓
   run queue
      ↓
 per-bench lock
      ↓
  run_local(...)
      ↓
 events + artifacts
      ↓
BenchCI CLI downloads ZIP
```

## Backend cloud flow

```text
Developer / CI
      ↓
 BenchCI CLI
      ↓
 BenchCI Backend
      ↓
 Queue / Scheduler
      ↓
 BenchCI-managed or backend-managed Agent
      ↓
  run_local(...)
      ↓
 events + artifacts
      ↓
BenchCI CLI downloads ZIP
```

## Configuration model

BenchCI separates:

- **bench configuration** in `bench.yaml`
- **suite configuration** in `suite.yaml`

A bench describes the hardware and runtime capabilities. A suite describes the test actions and expectations.

## Bench model

A bench contains:

- metadata
- optional defaults
- named nodes
- optional resources
- artifact settings

Each node may define:

- `kind`
- `role`
- `tags`
- flash configuration
- reset configuration
- transports
- GPIO lines

## Supported transport backends

BenchCI currently supports:

- UART
- Modbus RTU
- Modbus TCP
- CAN

## Supported GPIO backends

BenchCI currently supports:

- `local_gpio`
- `remote_gpio`
- `mock_gpio`

## Supported flash backends

BenchCI currently supports:

- `openocd`
- `cubeprog`
- `jlink`
- `esptool`

## Artifact model

BenchCI produces a single `results.json` plus per-node logs. Typical output looks like this:

```text
benchci-results/
└── 20260328-142200/
    ├── results.json
    └── nodes/
        ├── dut/
        │   ├── flash.log
        │   ├── gpio.log
        │   ├── transport-console.log
        │   └── transport-bus.log
        └── helper/
            └── transport-uplink.log
```

Remote Agent runs expose the same results through an artifact ZIP.

## Why the Agent matters

The Agent turns BenchCI from a single-machine runner into shared hardware infrastructure. Teams can host multiple benches behind one Agent, register them once, and reuse them from CI or developer machines without copying `bench.yaml` into every remote execution environment.

## Execution modes (Direct vs Cloud)

BenchCI can currently be used in three practical ways:

### Direct local mode

- CLI calls `run_local(...)` directly
- hardware is attached to the same machine
- simplest development workflow

### Direct remote Agent mode

- CLI submits runs to a customer-managed Agent
- Agent handles queueing and execution
- hardware is customer-owned and remote

### Cloud mode

- CLI talks to the BenchCI backend
- backend schedules work to a cloud-connected Agent
- artifacts return through the backend path

This lets the same bench and suite definitions scale from:

- single-developer local debugging
- to shared customer-managed labs
- to backend-controlled managed benches

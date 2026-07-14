# BenchCI Architecture

Use this page to understand how CLI, Agent, backend, dashboard, workspaces, scheduling, and real hardware execution fit together.

---

BenchCI is hardware CI for embedded systems. It combines a local execution
engine with optional remote Agent execution, backend scheduling,
workspace-aware access control, and review-ready evidence workflows.

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
- import external JUnit/CTRF results and LCOV coverage
- create and download release evidence bundles and reports
- start an Agent process

### Dashboard

The dashboard is the browser-based workspace view. It can show:

- workspace health
- available benches
- run history
- run details
- run events
- failure context
- reliability history and advisory failure assessments
- evidence, DUT identity, coverage, fuzzing, and fault summaries
- firmware assurance and artifact audit history
- artifacts plus evidence/JUnit/CTRF downloads
- release bundles, review sign-off, coverage matrices, and reports
- workspace artifact policy, teammates, roles, invites, and onboarding

Dashboard URL:

```text
https://app.benchci.dev
```

### Runner

Runner is the core execution engine. It:

- loads `bench.yaml` and `suite.yaml`
- cross-validates the suite against the bench
- discovers required nodes, transports, GPIO, and power resources
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
- cloud assignment polling when running in Cloud Agent mode

### Backend

The BenchCI backend handles:

- account login and refresh
- workspace membership
- workspace status and usage limits
- cloud bench inventory
- private/shared/reserved bench visibility
- cloud run submission
- scheduling and assignment
- agent polling
- agent event reporting
- cloud artifact return
- LCOV and external-result ingestion
- run evidence indexing and workspace-policy redaction
- artifact policy and audit events
- run and release-bundle lifecycle controls
- release review history, coverage matrices, and report generation
- reliability history and advisory failure assessment
- dashboard APIs

Current hosted backend:

```text
https://api.benchci.dev
```

## High-level flow

```text
Developer / CI / Dashboard
      ↓
 BenchCI CLI or Browser
      ↓
local runner, Agent, or backend-controlled cloud path
      ↓
 real hardware bench
      ↓
 logs + results + measurements + evidence
```

## Local execution flow

```text
bench.yaml + suite.yaml
        ↓
   benchci run
        ↓
    run_local(...)
        ↓
 start transports / GPIO / power / measurement resources
        ↓
 execute steps
        ↓
   results.json + evidence.json + evidence.html + logs
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
 cloud-connected Agent
      ↓
  run_local(...)
      ↓
 events + artifacts
      ↓
Backend + Dashboard + CLI
```

## Evidence and traceability flow

BenchCI now treats every run as an evidence-producing operation.

```text
bench.yaml + suite.yaml + firmware artifact
        ↓
local runner / Agent / Cloud Agent
        ↓
results.json + evidence.json + evidence.html + logs
        ↓
CLI artifact download + backend indexing + dashboard visibility
```

The evidence package can include:

- firmware SHA256
- Git commit, branch, remote, and dirty-state metadata
- CI provider and job URL
- bench config SHA256
- suite SHA256
- input snapshots of `bench.yaml` and `suite.yaml`
- requirement IDs
- test case IDs
- risk IDs
- structured failure explanations
- artifact file list
- artifact manifest with SHA256 hashes
- captured measurement values and run metrics
- configured or UART-verified DUT identity
- LCOV coverage summaries
- imported JUnit/CTRF source and artifact metadata
- protocol fuzzing campaign summaries and replay data
- experimental controlled fault-injection and recovery evidence
- firmware handling, verification, deletion, and audit metadata

The backend indexes key fields for Cloud runs so the dashboard can show evidence and traceability without downloading the full ZIP.

## Workspace model

BenchCI uses workspaces to isolate:

- users
- benches
- agents
- runs
- artifacts
- release bundles and review records
- permissions
- workspace usage limits

A user logs in with a BenchCI account. The active workspace determines which benches and runs are visible.

Bench types can include:

- private workspace benches
- managed shared benches
- reserved managed benches
- public demo benches where enabled

## Bench operation modes

BenchCI supports three bench operation modes. All three use the same `bench.yaml` + `suite.yaml` model and the same Agent execution path.

### Bring Your Own Bench (BYOB)

The user defines `bench.yaml` from scratch using any supported backends. BenchCI imposes no hardware constraints. Fully user-managed hardware.

```text
bench.yaml  -> user-defined nodes, transports, GPIO, power, measurement
suite.yaml  -> test logic targeting those logical names
```

### DIY BenchCI Bench

The user assembles a Raspberry Pi or Linux controller with community-supported modules such as USB relays, GPIO-connected relays, HTTP-accessible instruments, I2C power monitors, SCPI instruments, or serial sensors. BenchCI provides the GPIO, power, and measurement drivers; the user selects and wires the hardware.

```text
gpio_power / usb_relay_serial / http_relay                 -> power
i2c_power_monitor / scpi_measurement / script_measurement  -> measurement
local_gpio / remote_gpio                                    -> GPIO
```

<!-- Unreleased official hardware section is intentionally hidden until release. -->

---

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
- classic CAN and CAN FD over Linux SocketCAN
- I2C
- SPI

Bounded robustness steps are available for UART, CAN, Modbus RTU, and Modbus
TCP. Experimental controlled fault steps currently cover allow-listed power
glitches, GPIO glitches, and malformed UART bytes.

## Supported GPIO backends

BenchCI currently supports:

- `local_gpio`
- `remote_gpio`

<!-- Unreleased hardware GPIO backend docs are intentionally hidden until release. -->

## Supported flash backends

BenchCI currently supports:

- `openocd`
- `cubeprog`
- `jlink`
- `esptool`

## Supported bench resources

Power resources can use GPIO, HTTP relay, or serial relay backends.
Measurement resources can use HTTP/lab controllers, SCPI instruments, SCPI
power-supply readback, I2C power monitors, scripts, or serial responses.

## Artifact model

BenchCI produces structured result, evidence, input-snapshot, integrity, and
log artifacts. Typical output looks like this:

```text
benchci-results/
└── 20260328-142200/
    ├── results.json
    ├── evidence.json
    ├── evidence.html
    ├── manifest.json
    ├── metadata.json
    ├── inputs/
    │   ├── bench.yaml
    │   └── suite.yaml
    └── logs/
        ├── fuzz/
        ├── measurements/
        └── nodes/
            ├── dut/
            │   ├── flash.log
            │   ├── gpio.log
            │   ├── transport-console.log
            │   └── transport-bus.log
            └── helper/
                └── transport-uplink.log
```

Remote Agent runs expose the same results through an artifact ZIP. Cloud runs upload artifacts through the backend so the CLI and dashboard can inspect them.

## Why the Agent matters

The Agent turns BenchCI from a single-machine runner into shared hardware infrastructure. Teams can host multiple benches behind one Agent, register them once, and reuse them from CI or developer machines without copying `bench.yaml` into every remote execution environment.

## Execution modes (Direct vs Cloud)

BenchCI can currently be used in three practical ways:

### Direct local mode

- CLI calls local runner directly
- hardware is attached to the same machine
- simplest development workflow

### Direct remote Agent mode

- CLI submits runs to a customer-managed Agent
- Agent handles queueing and execution
- hardware is customer-owned and remote

### Cloud mode

- CLI talks to the BenchCI backend
- backend schedules work to a cloud-connected Agent
- artifacts and events return through the backend path
- dashboard provides visibility into status, failures, artifacts, evidence, and traceability

This lets the same bench and suite definitions scale from:

- single-developer local debugging
- to shared customer-managed labs
- to backend-controlled managed benches

## Bench reliability flow

BenchCI includes a reliability loop around real hardware execution:

```text
CLI validation and self-test
        ↓
Agent startup health checks
        ↓
Backend bench health storage
        ↓
Scheduler avoids unhealthy benches
        ↓
Dashboard health, history, and failure-source visibility
```

This means a bench is no longer treated as ready only because it is online. It
must also report acceptable health before the scheduler assigns cloud runs.
Recent terminal-run history is analyzed separately to surface last-10/last-30
health, flaky tests, cross-bench mismatches, repeated infrastructure failures,
and advisory history-backed failure assessments.

The intended user-facing workflow is:

```text
validate              -> Is my YAML valid and compatible?
benches self-test     -> Is the physical bench ready?
dry-run plan          -> What would the run do?
cloud scheduling      -> Is there a healthy/degraded matching bench?
dashboard             -> What failed, and what is the likely source?
```

See [Validation, Self-Test, and Dry-Run Planning](diagnostics.md) and [Cloud Agent Health, Resource Locking, and Scheduling](cloud_agent_health.md).

## Release evidence bundles

BenchCI includes a first-class bundling workflow for QA release evidence.

```text
Individual cloud runs (done/failed)
        ↓
benchci releases create / Dashboard Releases view
        ↓
Backend generates bundle ZIP
        ↓
coverage-matrix.json / .csv / .html
release-summary.json / .html
per-run evidence.json / evidence.html / manifest.json
HASHES.txt
        ↓
Submit for review with comment
        ↓
Approve or reject with hash-linked event
        ↓
Download ZIP or HTML/PDF report
```

A release bundle aggregates:

- per-run evidence and manifests
- requirement, test case, and risk traceability across all included runs
- a coverage matrix showing the latest and full per-run requirement/test results
- DUT identity and LCOV context when available
- external-result artifacts and source labels when available
- experimental fault-injection summary counts when present
- review state, lock timestamp, comments, and hash-linked review events
- SHA256 hashes of every file in the bundle

Approved bundles are locked against normal deletion. HTML/PDF reports can be
generated from the same evidence model. They are review aids, not certification
claims.

This lets teams produce a structured, tamper-evident hardware validation record
for a firmware release — connecting CI runs directly to engineering
requirements, risk IDs, DUT identity, coverage, and review decisions.

See [QA Evidence Workflow](qa_evidence_workflow.md) and [Evidence Reports](evidence_reports.md).

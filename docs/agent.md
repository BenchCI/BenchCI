# BenchCI Agent

BenchCI Agent runs on machines connected to real hardware. It exposes an HTTP API for remote execution, registered benches, run status, events, artifacts, and remote GPIO.

The Agent can also run in Cloud Mode, where it polls the BenchCI backend for assignments and reports results back to the backend.

## What the Agent does

The Agent can:

- accept uploaded-bench runs
- accept registered-bench runs
- queue runs
- enforce one active run per bench
- execute `run_local(...)` near the hardware
- expose structured run events
- package and serve artifacts
- provide remote GPIO endpoints for split deployments
- connect to the BenchCI backend as a cloud execution worker

## Where the Agent fits

The Agent is the remote execution layer in BenchCI.

It is used when you want:

- developer machines to stay separate from hardware machines
- CI pipelines to trigger real hardware tests over the network
- multiple reusable benches behind one machine
- registered bench IDs instead of repeatedly uploading bench definitions
- split deployments where a Linux machine exposes GPIO remotely

In the backend-controlled cloud path, the Agent also acts as the execution worker that polls the backend for assigned runs and uploads results after execution.

## Start the Agent

```bash
benchci agent serve
```

Default settings:

```text
host: 0.0.0.0
port: 8080
```

## Authentication

If `BENCHCI_AGENT_TOKEN` is set, the Agent requires `Authorization: Bearer <token>` for protected endpoints.

Example:

```bash
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

## Health check

```bash
curl http://localhost:8080/health
```

The health response includes information such as:

- service name
- Agent version
- `agent_id`
- `agent_name`
- queue depth
- whether auth is enabled
- number of active GPIO sessions
- whether registered bench mode is enabled

## Registered benches

The Agent can optionally load `agent.yaml` and register benches at startup.

Example:

```yaml
agent:
  id: lab-agent-1
  name: Main hardware lab

benches:
  - id: nucleo-uart
    bench_file: /opt/benchci/benches/nucleo-uart/bench.yaml
    tags: [stm32, uart]

  - id: plc-modbus
    bench_file: /opt/benchci/benches/plc-modbus/bench.yaml
    tags: [modbus, industrial]
```

When `agent.yaml` is present, the Agent loads the file, resolves each `bench_file`, and exposes those benches through the API.

## Bench endpoints

List benches:

```bash
curl -H "Authorization: Bearer $BENCHCI_AGENT_TOKEN" \
  http://localhost:8080/v1/benches
```

Get one bench:

```bash
curl -H "Authorization: Bearer $BENCHCI_AGENT_TOKEN" \
  http://localhost:8080/v1/benches/nucleo-uart
```

Bench summaries include:

- `bench_id`
- `agent_id`
- bench name and description
- tags
- busy/idle status
- current run ID
- capability summary:
  - transports
  - whether GPIO exists
  - whether power resources exist
  - flash backends
  - node count

## Run submission modes

### Uploaded-bench mode

The client uploads:

- `bench.yaml`
- `suite.yaml`
- optional artifact file
- `skip_flash`
- optional `verbose`

This is backward-compatible and does not require a pre-registered bench.

### Registered-bench mode

The client submits JSON containing:

- `bench_id`
- `suite_yaml`
- optional uploaded artifact payload
- `skip_flash`
- optional `verbose`

This mode reuses a bench already known by the Agent and is the preferred model for shared hardware infrastructure.

## Run endpoints

Create uploaded-bench run:

```text
POST /v1/runs
```

Create registered-bench run:

```text
POST /v1/runs/json
```

Fetch run status:

```text
GET /v1/runs/{run_id}
```

Fetch run events:

```text
GET /v1/runs/{run_id}/events
```

Download artifacts ZIP:

```text
GET /v1/runs/{run_id}/artifacts.zip
```

## Cloud Agent mode

In Cloud Agent mode, the Agent does not wait for direct run submissions from a user or CI runner. Instead, it polls the BenchCI backend.

Example:

```bash
benchci agent cloud \
  --backend https://benchci-backend.fly.dev \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --agent-name "Lab Agent 01"
```

The cloud Agent loop:

1. sends heartbeat
2. syncs bench summary/capabilities
3. polls for the next assignment
4. executes the assigned suite with `run_local(...)`
5. sends structured events
6. uploads artifacts
7. reports completion

The Agent token is created during workspace/customer onboarding by the BenchCI owner/admin process.

## Run lifecycle

Agent runs move through these states:

- `queued`
- `preparing`
- `running`
- `uploading_artifacts`
- `done`
- `failed`

Each run stores:

- current status
- mode (`uploaded` or `registered`)
- optional `bench_id`
- `exit_code`
- timestamps
- current test and step
- structured events

## Verbose runs

BenchCI supports verbose execution mode for both uploaded-bench and registered-bench runs.

When verbose mode is enabled:

- the runner produces richer step-level diagnostics
- failure messages include additional context
- more detailed log information may appear in artifacts
- event payloads may include richer execution details
- run behavior stays the same; only observability changes

Verbose mode is controlled by the CLI using `--verbose` and is propagated through the Agent to the underlying `run_local(...)` execution.

Notes:

- verbose output is primarily visible in artifacts and structured events
- the Agent does not stream raw verbose terminal output directly to clients
- the best place to inspect verbose remote diagnostics is the downloaded artifact ZIP

## Scheduling model

The Agent keeps:

- one queue for submitted runs
- one lock per registered bench

This means:

- a bench can only run one job at a time
- different benches can still be queued independently
- uploaded-bench runs are serialized through a synthetic uploaded-bench lock

## Events

The Agent stores structured events emitted by the runner, such as:

- `run.started`
- `test.started`
- `step.started`
- `step.finished`
- `step.failed`
- `run.finished`
- `run.failed`

These events make it possible to build richer CLI or UI progress views.

## Remote GPIO

The Agent also exposes remote GPIO endpoints used by `remote_gpio` benches:

- `POST /v1/gpio/session/start`
- `POST /v1/gpio/session/stop`
- `POST /v1/gpio/set`
- `POST /v1/gpio/get`
- `POST /v1/gpio/wait_value`
- `POST /v1/gpio/wait_edge`

This allows one Linux machine to control GPIO on behalf of a runner or another Agent-accessible workflow.

## Artifacts

Runs produce artifacts such as:

- `results.json`
- per-node transport logs
- `flash.log`
- `gpio.log`
- power logs when power resources are used

Verbose runs may produce more detailed artifact content for debugging and failure analysis.

The Agent packages the run results directory as a ZIP and serves it through the artifacts endpoint, or uploads it to the backend in Cloud Agent mode.

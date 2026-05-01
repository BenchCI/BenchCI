# BenchCI Agent

BenchCI Agent runs on machines connected to real hardware.

It is the bridge between CI/developers and the physical bench.

---

## Do you need an Agent?

For local testing:

```text
developer machine -> hardware
```

You do **not** need an Agent.

For remote or CI testing:

```text
CI/developer -> BenchCI Agent -> hardware
```

You usually need an Agent.

For BenchCI Cloud:

```text
CI/developer -> BenchCI backend -> cloud-connected Agent -> hardware
```

You need a cloud-connected Agent.

---

## Recommended first path

Before starting Agent mode, verify local execution on the hardware machine:

```bash
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf
```

Do not move to Cloud Mode until local execution works.

---

## Cloud Agent quick start

Cloud Agent mode is the recommended path for GitHub Actions, GitLab CI, remote developers, and shared hardware labs.

### 1. Get an Agent token

Agent tokens are created during workspace onboarding.

Contact the BenchCI team or your workspace owner to receive a token.

Keep Agent tokens out of source control and rotate them if leaked.

### 2. Start the cloud-connected Agent

```bash
benchci agent cloud \
  --backend https://api.benchci.dev \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --agent-name "Lab Agent 01"
```

The Agent will:

- register or sync the bench
- publish capabilities
- send heartbeats
- poll for assignments
- execute runs near the hardware
- upload events, artifacts, evidence, and traceability metadata

### 3. Verify the bench is visible

From a developer machine or CI environment:

```bash
benchci benches list
```

You should see the bench ID and online/idle status.

You can also verify it in the dashboard:

```text
https://app.benchci.dev
```

---

## Direct Agent mode

Direct Agent mode is useful when the client can reach the hardware machine over the network.

Start the Agent:

```bash
benchci agent serve
```

Default settings:

```text
host: 0.0.0.0
port: 8080
```

Run against the Agent:

```bash
benchci run \
  --agent http://agent-host:8080 \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf
```

With authentication:

```bash
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

Then run:

```bash
benchci run \
  --agent http://agent-host:8080 \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

---

## What the Agent does

The Agent can:

- accept uploaded-bench runs
- accept registered-bench runs
- queue runs
- enforce one active run per bench
- execute local run near the hardware
- expose structured run events
- package and serve artifacts, including `results.json`, `evidence.json`, `evidence.html`, and input snapshots
- provide remote GPIO endpoints for split deployments
- connect to the BenchCI backend as a cloud execution worker

---

## Where the Agent fits

Use the Agent when you want:

- developer machines to stay separate from hardware machines
- CI pipelines to trigger real hardware tests
- multiple reusable benches behind one machine
- registered bench IDs instead of repeatedly uploading bench definitions
- shared hardware access
- split deployments where a Linux machine exposes GPIO remotely

---

## Health check

```bash
curl http://localhost:8080/health
```

If auth is enabled:

```bash
curl -H "Authorization: Bearer $BENCHCI_AGENT_TOKEN" \
  http://localhost:8080/health
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

---

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

When `agent.yaml` is present, the Agent loads each `bench_file` and exposes those benches through the API.

---

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

---

## Run submission modes

### Uploaded-bench mode

The client uploads:

- `bench.yaml`
- `suite.yaml`
- optional artifact file
- `skip_flash`
- optional `verbose`

This mode is useful for early testing and does not require a pre-registered bench.

### Registered-bench mode

The client submits:

- `bench_id`
- `suite.yaml`
- optional artifact file
- `skip_flash`
- optional `verbose`

This mode reuses a bench already known by the Agent and is preferred for shared labs.

---

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

---

## Cloud Agent lifecycle

In Cloud Agent mode, the Agent polls the BenchCI backend.

The loop is:

1. send heartbeat
2. sync bench summary/capabilities
3. poll for the next assignment
4. execute the assigned suite with local run
5. send structured events
6. upload artifacts
7. report completion

The lab machine does not need a public inbound port. It makes outbound requests to BenchCI.

---

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
- mode (`uploaded`, `registered`, or cloud assignment)
- optional `bench_id`
- `exit_code`
- events
- artifacts

---

## Evidence artifacts from Agent runs

Agent and Cloud Agent runs preserve the same evidence package produced by local execution.

The artifact ZIP can include:

- `results.json`
- `evidence.json`
- `evidence.html`
- `metadata.json`
- `inputs/bench.yaml`
- `inputs/suite.yaml`
- per-node logs such as `flash.log`, `transport-*.log`, and `gpio.log`
- power logs where power resources are used

For Cloud Agent runs, the backend extracts key fields from `evidence.json`, such as firmware hash, Git commit, CI job URL, requirement IDs, test case IDs, risk IDs, and whether `evidence.html` is available.

## Security notes

- Keep Agent tokens out of source control.
- Use one token per lab Agent or customer workspace when possible.
- Rotate leaked tokens.
- Prefer Cloud Agent mode when you do not want inbound network access to lab machines.
- Restrict direct Agent access to trusted networks.

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

Workspace owners and admins with an active account can create Agent tokens from the BenchCI dashboard. Copy the token when it is created; the plaintext value is shown only once.

Keep Agent tokens out of source control and rotate them if leaked.

### 2. Start the cloud-connected Agent

```bash
benchci agent cloud \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench
```

<!-- Unreleased hardware metadata example is intentionally hidden until release. -->

The Agent will:

- register or sync the bench
- publish capabilities, including transport, flash, GPIO, power, and measurement support
- send heartbeats
- poll for assignments
- execute runs on the hardware-connected machine
- upload events, artifacts, evidence, and traceability metadata

### 3. Verify the bench is visible

From a developer machine or CI environment:

```bash
benchci benches list
```

You should see the configured ID, cloud ID, and online/idle status. They are
usually identical. If the configured ID collided with an existing cloud ID,
BenchCI assigns a tenant-safe cloud ID while retaining the configured ID as a
workspace alias. Runs can keep using a unique configured alias; use the cloud
ID shown by `benchci benches list` if the backend reports that an alias is
ambiguous.

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
- execute local runs on the hardware-connected machine
- expose structured run events
- package and serve artifacts, including `results.json`, `evidence.json`, `evidence.html`, `manifest.json`, and input snapshots
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
- registered bench health counts

---

## Registered benches

In Direct Agent mode, the Agent can load `agent.yaml` and register benches at startup. One `benchci agent serve` process can expose multiple bench IDs; you do not need one terminal or one Agent process per bench.

Use this when the hardware-connected machine owns the bench definitions and callers should select a stable `--bench-id` instead of uploading `bench.yaml` on every run.

Cloud Agent mode is different: `benchci agent cloud` manages one bench from its `--bench` argument and publishes that bench to the cloud scheduler. It does not load multiple benches from `agent.yaml`.

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

Start the Agent with that config:

```bash
export BENCHCI_AGENT_CONFIG=/opt/benchci/agent.yaml
benchci agent serve
```

Or with authentication:

```bash
export BENCHCI_AGENT_CONFIG=/opt/benchci/agent.yaml
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

If `BENCHCI_AGENT_CONFIG` is not set, the Agent looks for `~/benchci-agent-results/agent.yaml`.

At startup, the Agent loads each `bench_file` and exposes those benches through the API.

Paths in `bench_file` are resolved relative to the directory containing `agent.yaml`, so `./bench.yaml` refers to a file next to the agent config regardless of where the `benchci agent serve` command is invoked.

Submit a run to one registered bench by using its ID:

```bash
benchci run \
  --agent http://agent-host:8080 \
  --bench-id nucleo-uart \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

The Agent queues incoming runs and executes them on the hardware-connected machine using the selected bench file.

### Hardware profile metadata (optional)

Registered benches can optionally declare a hardware profile and revision. These fields are descriptive only — they do not change how the bench runs.

```yaml
benches:
  - id: lab-bench-001
    bench_file: ./bench.yaml
    tags: [raspberry-pi-5]
    hardware_profile: generic
    hardware_revision: local
```

Known profiles at this time:

| Profile ID | Description |
|---|---|
| `generic` | No profile — all capabilities come from `bench.yaml`. |

<!-- Unreleased hardware profile row is intentionally hidden until release. -->

An unknown `hardware_profile` value is accepted without error. It is included in the capability summary with `hardware_profile_known: false`.

---

## Verify registered benches

After starting an Agent with `agent.yaml`, you can check which benches it loaded.

List registered benches:

```bash
curl -H "Authorization: Bearer $BENCHCI_AGENT_TOKEN" \
  http://localhost:8080/v1/benches
```

Inspect one registered bench:

```bash
curl -H "Authorization: Bearer $BENCHCI_AGENT_TOKEN" \
  http://localhost:8080/v1/benches/nucleo-uart
```

These checks are optional, but useful when confirming that `bench_file` paths, tags, and capability summaries are correct before submitting runs. Normal run submission should still use `benchci run --agent ...`.

Bench summaries include:

- `bench_id`
- `agent_id`
- bench name and description
- tags
- busy/idle status
- current run ID
- capability summary, including transports, GPIO/power/measurement availability, flash/power/measurement backends, and node count
- optional hardware profile metadata: `hardware_profile`, `hardware_revision`, `hardware_profile_known`, `hardware_channels`

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

Use `benchci run --agent ...` for normal usage. The CLI handles run submission, status polling, event streaming, and artifact download.

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

Each Direct Agent run stores:

- current status
- mode (`uploaded` or `registered`)
- `bench_id` for registered-bench runs; uploaded-bench runs leave this empty because the bench YAML is uploaded with the run
- `exit_code`
- events
- artifacts

Cloud runs are tracked by the backend instead. They either target an exact bench ID or match scheduler requirements, and the assignment sent to the Cloud Agent includes the selected bench ID.

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

---

## Security notes

- Keep Agent tokens out of source control.
- Use one token per lab machine or Agent service. A single Agent can register multiple benches from the same machine.
- Rotate leaked tokens.
- Prefer Cloud Agent mode when you do not want inbound network access to lab machines.
- Restrict direct Agent access to trusted networks.

---

## Agent startup self-check and bench health

Startup self-checks are available in both Agent modes, but they are used differently.

In Direct Agent mode, `benchci agent serve` can run a non-destructive self-test for each registered bench loaded from `agent.yaml`. The result is exposed through the Agent health and bench endpoints. Uploaded-bench runs do not have startup bench health because the bench YAML is supplied per run.

In Cloud Agent mode, `benchci agent cloud` can run the same non-destructive self-test for its managed bench and sync the result to the backend. Cloud scheduling and the dashboard use that synced health state.

The health state can be:

```text
healthy
degraded
failing
unknown
```

Optional health depth controls:

```bash
export BENCHCI_AGENT_SELF_TEST_READ_INPUTS=0
export BENCHCI_AGENT_SELF_TEST_READ_MEASUREMENTS=0
```

Startup health checks always run and open/close configured hardware interfaces. They remain non-destructive: they do not flash, reset, toggle relays, drive GPIO outputs, send protocol commands, or read measurements unless enabled.

Health reports are written on the Agent machine. Direct Agent reports use:

```text
~/benchci-agent-results/
  bench-health/
    <bench_id>/
      self-test.log
      self-test-summary.json
      nodes/
      resources/
```

Cloud Agent reports use:

```text
~/.benchci/
  agent-health/
    <bench_id>/
      self-test.log
      self-test-summary.json
      nodes/
      resources/
```

See [Cloud Agent Health, Resource Locking, and Scheduling](cloud_agent_health.md).

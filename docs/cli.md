# BenchCI CLI

The BenchCI CLI is the main entry point for validating configs, running tests, managing sessions, and starting the Agent.

## Available commands

BenchCI currently provides:

- `login`
- `logout`
- `whoami`
- `validate`
- `run`
- `doctor`
- `agent serve`

## `benchci login`

Activate a BenchCI license and store a local session.

```bash
benchci login
```

Or:

```bash
benchci login --license-key "YOUR_LICENSE_KEY"
```

Optional backend override:

```bash
benchci login --api-url https://your-backend.example.com
```

## `benchci logout`

Remove the stored BenchCI session.

```bash
benchci logout
```

## `benchci whoami`

Show the current BenchCI session and license status.

```bash
benchci whoami
```

## `benchci validate`

Validate `bench.yaml` and/or `suite.yaml` without touching hardware.

```bash
benchci validate --bench bench.yaml --suite suite.yaml
```

You can validate only one file type if needed:

```bash
benchci validate --bench bench.yaml
benchci validate --suite suite.yaml
```

## `benchci run`

Run a suite locally or remotely.

### Local mode

Requires `--bench` and `--suite`.

```bash
benchci run \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf
```

### Local mode without flashing

```bash
benchci run \
  --bench bench.yaml \
  --suite suite.yaml \
  --skip-flash
```

### Remote uploaded-bench mode

In uploaded-bench mode, the CLI uploads `bench.yaml`, `suite.yaml`, and the artifact to the Agent.

```bash
benchci run \
  --agent http://agent-host:8080 \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

### Remote registered-bench mode

In registered-bench mode, the Agent already knows the bench and you only provide `--bench-id`, the suite, and the artifact.

```bash
benchci run \
  --agent http://agent-host:8080 \
  --bench-id my-registered-bench \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

### Important rules

- local runs require `--bench`
- remote uploaded-bench runs require `--agent` and `--bench`
- remote registered-bench runs require `--agent` and `--bench-id`
- `--bench` and `--bench-id` are mutually exclusive

### Remote run lifecycle

The CLI polls the Agent until the run reaches a terminal state:

- `queued`
- `preparing`
- `running`
- `uploading_artifacts`
- `done`
- `failed`

When the run finishes, the CLI attempts to download the artifact ZIP into `benchci-results/agent_<run_id>.zip`.

## `benchci doctor`

Run environment diagnostics.

```bash
benchci doctor
```

Useful options:

```bash
benchci doctor --bench bench.yaml
benchci doctor --port /dev/ttyUSB0 --baud 115200
benchci doctor --agent http://agent-host:8080
benchci doctor --agent http://agent-host:8080 --token "$BENCHCI_AGENT_TOKEN"
benchci doctor --json
benchci doctor --export doctor-report.zip
```

## `benchci agent serve`

Start a BenchCI Agent on the current machine.

```bash
benchci agent serve
```

The Agent is used for remote execution and remote GPIO services.

## Session behavior

Commands that execute runs require a valid BenchCI session. The CLI refreshes the stored session when needed before running hardware operations.

## Result artifacts

Local runs write results under a timestamped directory inside `benchci-results/`. Remote runs download a ZIP artifact bundle into `benchci-results/`.

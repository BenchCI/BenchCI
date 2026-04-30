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
- `agent cloud`
- `benches list`
- `benches show`
- `runs list`
- `runs show`
- `runs events`
- `runs artifacts`

## `benchci login`

Log in with your BenchCI account and store a local session.

```bash
benchci login
```


BenchCI uses account and workspace based authentication. Your active workspace determines which Cloud Mode benches and runs are visible.

## `benchci logout`

Remove the stored BenchCI session.

```bash
benchci logout
```

## `benchci whoami`

Show the current BenchCI session, user, and active workspace.

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

Run a suite locally, remotely, or through the backend-controlled cloud path.

### Execution mode selection

BenchCI selects execution mode based on the flags you provide.

- no `--agent` and no `--cloud` → local execution
- with `--agent` → remote Agent execution
- with `--cloud` → backend-controlled cloud execution

Examples:

Local:

```bash
benchci run --bench bench.yaml --suite suite.yaml
```

Remote Agent:

```bash
benchci run --agent http://agent-host:8080 ...
```

Cloud:

```bash
benchci run --cloud --bench-id my-cloud-bench ...
```

### Local mode

Requires `--bench` and `--suite`.

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/fw.elf
```

### Local mode without flashing

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --skip-flash
```

### Local mode with verbose diagnostics

Use `--verbose` when you want richer failure context and more detailed step-level logging.

```bash
benchci run   --bench bench.yaml   --suite suite.yaml   --artifact build/fw.elf   --verbose
```

Verbose mode can include additional diagnostics such as:

- step durations
- resolved timeouts
- active log paths
- richer failure context
- recent transport tail information where available

### Remote uploaded-bench mode

In uploaded-bench mode, the CLI uploads `bench.yaml`, `suite.yaml`, and the artifact to the Agent.

```bash
benchci run   --agent http://agent-host:8080   --bench bench.yaml   --suite suite.yaml   --artifact build/fw.elf   --token "$BENCHCI_AGENT_TOKEN"
```

With verbose diagnostics:

```bash
benchci run   --agent http://agent-host:8080   --bench bench.yaml   --suite suite.yaml   --artifact build/fw.elf   --token "$BENCHCI_AGENT_TOKEN"   --verbose
```

### Remote registered-bench mode

In registered-bench mode, the Agent already knows the bench and you only provide `--bench-id`, the suite, and the artifact.

```bash
benchci run   --agent http://agent-host:8080   --bench-id my-registered-bench   --suite suite.yaml   --artifact build/fw.elf   --token "$BENCHCI_AGENT_TOKEN"
```

With verbose diagnostics:

```bash
benchci run   --agent http://agent-host:8080   --bench-id my-registered-bench   --suite suite.yaml   --artifact build/fw.elf   --token "$BENCHCI_AGENT_TOKEN"   --verbose
```

### Cloud mode

In cloud mode, the CLI talks to the BenchCI backend instead of directly to the Agent.

Run against a specific cloud bench:

```bash
benchci run   --cloud   --bench-id my-cloud-bench   --suite suite.yaml   --artifact build/fw.elf
```

Run using scheduler requirements:

```bash
benchci run   --cloud   --tag uart   --transport uart   --flash-backend openocd   --suite suite.yaml   --artifact build/fw.elf
```

Optional cloud capability filters include:

- `--tag`
- `--transport`
- `--flash-backend`
- `--has-gpio` / `--no-has-gpio`
- `--has-power` / `--no-has-power`
- `--min-node-count`

### Important rules

- local runs require `--bench`
- remote uploaded-bench runs require `--agent` and `--bench`
- remote registered-bench runs require `--agent` and `--bench-id`
- cloud runs require `--cloud` and either `--bench-id` or cloud capability filters
- `--agent` and `--cloud` are mutually exclusive
- `--bench` and `--bench-id` are mutually exclusive outside cloud mode

### Remote run lifecycle

The CLI polls the Agent until the run reaches a terminal state:

- `queued`
- `preparing`
- `running`
- `uploading_artifacts`
- `done`
- `failed`

When the run finishes, the CLI attempts to download the artifact ZIP into `benchci-results/agent_<run_id>.zip`.

### Cloud run lifecycle

The CLI polls the backend until the run reaches a terminal state:

- `queued`
- `preparing`
- `running`
- `uploading_artifacts`
- `done`
- `failed`

When the run finishes, the CLI attempts to download the artifact ZIP into `benchci-results/cloud_<run_id>.zip`.

### Verbose behavior in remote runs

Verbose mode is supported for remote runs as well.

Notes:

- the CLI forwards `--verbose` to the Agent or backend submission path
- the Agent executes the run in verbose mode
- richer diagnostics are reflected in artifacts and structured run events
- the CLI does not stream the Agent's full raw verbose terminal output directly; inspect downloaded artifacts for the most detailed logs

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

## `benchci agent cloud`

Start the cloud-connected Agent loop on the current machine.

```bash
benchci agent cloud   --backend https://api.benchci.dev   --token YOUR_AGENT_TOKEN   --bench bench.yaml
```

Optional cloud Agent fields include:

- `--bench-id`
- `--tag`
- `--agent-name`
- `--region`
- `--poll-interval-s`

The agent token is created by the BenchCI owner/admin side during onboarding.

## `benchci benches list`

List cloud benches visible through the backend and the active workspace.

```bash
benchci benches list
```

Machine-readable output:

```bash
benchci benches list --json
```

## `benchci benches show`

Show one cloud bench.

```bash
benchci benches show my-cloud-bench
```

## `benchci runs list`

List cloud runs.

```bash
benchci runs list
```

## `benchci runs show`

Show one cloud run.

```bash
benchci runs show <RUN_ID>
```

## `benchci runs events`

Show structured events for one cloud run.

```bash
benchci runs events <RUN_ID>
```

## `benchci runs artifacts`

Download artifacts for one cloud run.

```bash
benchci runs artifacts <RUN_ID>
```

## Session behavior

Commands that execute cloud runs require a valid BenchCI session. The CLI refreshes the stored session when needed before running hardware operations.

## Result artifacts

Local runs write results under a timestamped directory inside `benchci-results/`. Remote runs and cloud runs download a ZIP artifact bundle into `benchci-results/`.

Verbose runs may produce richer diagnostic context in:

- `results.json`
- transport logs
- `flash.log`
- `gpio.log`

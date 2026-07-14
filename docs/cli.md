# BenchCI CLI

Use this page as the command reference for login, validation, local runs, Agent runs, Cloud Mode, benches, runs, artifacts, and diagnostics.

---

The BenchCI CLI is the main entry point for validating configs, running tests, managing sessions, and starting the Agent.


## Common commands

```bash
benchci login
benchci whoami
benchci init --preset flash-uart
benchci validate --bench bench.yaml --suite suite.yaml
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf
benchci benches list
benchci run --cloud --bench-id my-cloud-bench --suite suite.yaml --artifact build/fw.elf
```

---

## Available commands

BenchCI currently provides:

- `register`
- `login`
- `logout`
- `whoami`
- `init`
- `validate`
- `run`
- `measure`
- `demo`
- `doctor`
- `agent serve`
- `agent cloud`
- `benches self-test`
- `benches list`
- `benches show`
- `workspaces list`
- `workspaces use`
- `runs list`
- `runs show`
- `runs events`
- `runs download`
- `runs export`
- `runs attach-results`
- `runs create-external`
- `coverage upload`
- `releases create`
- `releases list`
- `releases show`
- `releases download`
- `releases report`

## `benchci register`

Create a new BenchCI account and your first workspace.

```bash
benchci register
```

Optionally, use the dashboard (app.benchci.dev)

## `benchci login`

Log in with your BenchCI account and store a local session.

```bash
benchci login
```

MFA-enabled human accounts are prompted for an authenticator code after the
password check. For scripted human use, pass `--totp-code 123456` or
`--recovery-code bc-...`; do not store authenticator secrets in CI.

BenchCI uses account and workspace based authentication. Your active workspace determines which Cloud Mode benches and runs are visible.

## `benchci logout`

Remove the stored BenchCI session.

```bash
benchci logout
```

## `benchci whoami`

Show the current BenchCI session, user, active workspace, and workspace limits.

```bash
benchci whoami
```

Example output:

```text
✓ BenchCI session is active
  Backend: https://api.benchci.dev
  User: engineer@company.com (Jane)
  Active workspace: Acme (developer)
  Workspace plan: Team
  Workspace status: active
  Workspace entitled: True
  Limits: — seats · 10 benches · 5 CI runners · 10,000 runs/mo
  User status: active
```

When no monthly run cap applies, the monthly run limit shows `∞`.

## `benchci init`

Generate starter `bench.yaml` and `suite.yaml` files from validated presets.

```bash
benchci init --list-presets
benchci init --preset flash-uart
benchci init --preset uart-smoke --yes --bench-output bench.yaml --suite-output suite.yaml
```

Interactive mode is used by default when you run in a TTY. `--yes` skips prompts for scripts and bootstrap flows. Existing files are not overwritten unless you pass `--force`.

The generated pair is validated with BenchCI's config models before it is written, and the command prints follow-up commands for `benchci doctor`, `benchci validate`, and `benchci run`. The run hint includes `--artifact` only for presets that include firmware flashing.

Current presets include:

- `uart-smoke`
- `flash-uart`
- `gpio-reset-ready`
- `power-cycle`
- `measurement-threshold`
- `can-handshake`
- `modbus-rtu`
- `modbus-tcp`
- `uart-fuzz`
- `can-fuzz`
- `modbus-rtu-fuzz`
- `modbus-tcp-fuzz`
- `i2c-sensor-smoke`
- `spi-flash-verify`

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

Run without uploading firmware bytes to BenchCI Cloud:

```bash
benchci run   --cloud   --bench-id my-cloud-bench   --suite suite.yaml   --firmware-url "$SIGNED_FIRMWARE_URL"   --firmware-sha256 "$FIRMWARE_SHA256"
```

Delete uploaded firmware bytes after the assigned Agent fetches them:

```bash
benchci run   --cloud   --bench-id my-cloud-bench   --suite suite.yaml   --artifact build/fw.elf   --firmware-handling-mode delete_after_fetch
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
- `--firmware-url` requires `--cloud` and `--firmware-sha256`
- `--firmware-url` and `--artifact` are mutually exclusive
- `--firmware-handling-mode` accepts `brokered`, `delete_after_fetch`, or `external_url`

### Evidence and metrics summaries

When a run produces evidence, the CLI can print useful summary fields such as firmware hash, Git commit, CI URL, bench/suite hashes, traceability IDs, artifact report availability, and captured metrics from measurement steps.

For example, a low-power test may record:

```text
sleep_current_a: 0.042 A
```

### Remote run lifecycle

The CLI polls the Agent until the run reaches a terminal state:

- `queued`
- `preparing`
- `running`
- `uploading_artifacts`
- `done`
- `failed`

When the run finishes, the CLI attempts to download the artifact ZIP into `<results-dir>/agent_<run_id>.zip`. The default results directory is `benchci-results`; use `--results-dir` to change it.

### Cloud run lifecycle

The CLI polls the backend until the run reaches a terminal state:

- `queued`
- `preparing`
- `running`
- `uploading_artifacts`
- `done`
- `failed`

When the run finishes, the CLI attempts to download the artifact ZIP into `<results-dir>/cloud_<run_id>.zip`. The default results directory is `benchci-results`; use `--results-dir` to change it.

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

### Improved doctor output

`benchci doctor` is intended to help users build a correct `bench.yaml` without guessing.

It can show:

- OS, Python, and BenchCI version
- login/workspace/API status when available
- serial ports with likely usage hints
- USB devices such as ST-Link, USB-UART, USB-RS485, relays, or probes
- GPIO chips such as `/dev/gpiochip0`
- common flashing tools such as OpenOCD, STM32CubeProgrammer, J-Link, and esptool
- bench-specific checks when `--bench bench.yaml` is provided

Useful focused commands:

```bash
benchci doctor --port /dev/ttyUSB0 --baud 115200
benchci doctor --bench bench.yaml
benchci doctor --agent http://agent-host:8080
benchci doctor --json
benchci doctor --export doctor-report.zip
```

When a failure suggests checking ports, tools, or GPIO access, run doctor on the machine connected to the hardware.

## `benchci agent serve`

Start a BenchCI Agent on the current machine.

```bash
benchci agent serve
```

The Agent is used for remote execution and remote GPIO services.

## `benchci agent cloud`

Start the cloud-connected Agent loop on the current machine.

```bash
benchci agent cloud   --token YOUR_AGENT_TOKEN   --bench bench.yaml
```

Optional cloud Agent fields include:

- `--bench-id`
- `--tag`
- `--region`
- `--poll-interval-s`

`--agent-name` is optional metadata. In normal dashboard-created Agent flows, use the name configured in the dashboard.

Workspace owners and admins with an active account can create Agent tokens from the BenchCI dashboard.

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

Show one cloud run, including indexed evidence, structured failure context,
DUT identity, fault-injection summaries, coverage, and reliability history
when those fields are available for the run.

```bash
benchci runs show <RUN_ID>
```

For failed runs, the response may include both the canonical failure source
and an advisory history-backed assessment. The assessment never changes the
recorded pass/fail result or canonical failure classification.

## `benchci runs events`

Show structured events for one cloud run.

```bash
benchci runs events <RUN_ID>
```

## `benchci runs download`

Download the artifact ZIP for a completed cloud run.

```bash
benchci runs download <RUN_ID>
```

With a custom output path:

```bash
benchci runs download <RUN_ID> --output results/my-run.zip
```

The default destination is `benchci-results/<RUN_ID>.zip`.

## `benchci runs export`

Download backend-generated JUnit XML or CTRF JSON for one cloud run.

```bash
benchci runs export --format junit-xml <RUN_ID>
benchci runs export --format ctrf <RUN_ID> --output report.ctrf.json
```

## `benchci runs attach-results`

Attach external JUnit XML, CTRF JSON, logs, or artifact references to an existing run.

```bash
benchci runs attach-results report.xml --run-id <RUN_ID> --framework pytest --source pytest
benchci runs attach-results --run-id <RUN_ID> --log pytest.log --artifact artifacts/scope.png
```

## `benchci runs create-external`

Create a cloud-visible run from an existing external test workflow.

```bash
benchci runs create-external --name "hardware nightly" --junit report.xml --framework pytest --source pytest
benchci runs create-external --name "labgrid nightly" --junit report.xml --artifacts artifacts/ --framework pytest --source labgrid
benchci runs create-external --name "rev-b nightly" --junit report.xml --firmware-sha256 "$SHA256" --firmware-filename firmware.elf --dut-hardware-revision rev-b --dut-serial-number "$SERIAL"
benchci runs create-external --workspace-id <WORKSPACE_ID> --name "workspace-specific nightly" --junit report.xml --framework pytest
```

By default, external runs are created in your active workspace. Use `--workspace-id` when the same user or CI token belongs to multiple workspaces and the run should be recorded somewhere else.

## `benchci coverage upload`

Attach code coverage from unit tests or simulation (LCOV format) to a cloud run. This is separate from the hardware test results — the coverage data is not measured from the hardware run itself.

```bash
benchci coverage upload coverage/lcov.info --run-id <RUN_ID>
```

## `benchci measure`

Run a one-off measurement resource from `bench.yaml`.

```bash
benchci measure --bench bench.yaml supply_current
benchci measure --bench bench.yaml supply_current --repeat 10 --interval-ms 500
benchci measure --bench bench.yaml supply_current --json
```

Use this to debug HTTP, SCPI, I2C, script, and serial measurement resources before wiring them into a full suite.

## `benchci demo`

Run the local no-hardware demo.

```bash
benchci demo
benchci demo --verbose
benchci demo --open-dashboard
```

## `benchci workspaces list`

List workspaces available to the current account.

```bash
benchci workspaces list
benchci workspaces list --json
```

## `benchci workspaces use`

Switch the active workspace used by cloud operations.

```bash
benchci workspaces use <WORKSPACE_ID>
```

The CLI refreshes its backend-bound session when switching so subsequent cloud requests use the same workspace locally and server-side.

## `benchci releases create`

Create a release evidence bundle from completed cloud run IDs.

```bash
benchci releases create "Firmware v1.2.3" --runs RUN_ID_1,RUN_ID_2
```

## `benchci releases list`

List release evidence bundles for the active workspace.

```bash
benchci releases list
```

## `benchci releases show`

Show release bundle metadata, included runs, and coverage summary.

```bash
benchci releases show <BUNDLE_ID>
```

## `benchci releases download`

Download a release evidence bundle ZIP.

```bash
benchci releases download <BUNDLE_ID>
benchci releases download <BUNDLE_ID> --out release-v1.2.3.zip
```

## `benchci releases report`

Download a human-readable release report as HTML or PDF:

```bash
benchci releases report <BUNDLE_ID>
benchci releases report <BUNDLE_ID> --template generic-qa --format html --out release-report.html
benchci releases report <BUNDLE_ID> --template iec-62304-style --format pdf --out release-report.pdf
benchci releases report <BUNDLE_ID> --template iso-26262-style --format pdf
```

Supported templates are `generic-qa`, `iec-62304-style`, and
`iso-26262-style`. Reports include the bundle review state and are evidence
review aids, not certification or regulatory approval.

## Session behavior

Commands that execute cloud runs require a valid BenchCI session. The CLI refreshes the stored session when needed before running hardware operations.

## Result artifacts and evidence

Local runs write results under a timestamped directory inside the configured results directory. By default this is `benchci-results/`, or `artifacts.root_dir` from `bench.yaml` for local runs. Passing `--results-dir` overrides the result root for local, remote Agent, and cloud runs.

Typical outputs include:

- `results.json` — execution summary, test results, structured failures, and per-test traceability
- `evidence.json` — machine-readable evidence report
- `evidence.html` — human-readable evidence report
- `metadata.json` — supporting run metadata
- `inputs/bench.yaml` and `inputs/suite.yaml` — snapshots of the exact inputs used
- transport logs
- `flash.log`
- `gpio.log`
- `power.log` where power resources are used

The CLI prints a compact evidence summary when evidence is available, including firmware hash, Git commit, CI job URL, bench, suite, and traceability IDs.

## Failure output

BenchCI failures are structured when possible. Instead of only showing a raw exception, CLI, artifacts, backend, and dashboard can include:

- failure category
- title and message
- explanation
- suggested checks
- failed step context
- related artifact paths
- raw error details where useful

This is why failed runs may point you to a specific log such as `flash.log`, `transport-console.log`, `gpio.log`, or `power.log`.

## Diagnostics and readiness commands

### `benchci validate`

Validate files without touching hardware:

```bash
benchci validate --bench bench.yaml --suite suite.yaml
benchci validate --bench bench.yaml --suite suite.yaml --json
benchci validate --bench bench.yaml --suite suite.yaml --output validation.json
```

For QA/release workflows, treat `benchci validate` as a static check of BenchCI testware: it reviews the hardware configuration and suite definition before dynamic execution on a physical DUT. See [Static Testing and Evidence Review](static_testing.md).

### `benchci benches self-test`

Check bench readiness:

```bash
benchci benches self-test --bench bench.yaml
benchci benches self-test --bench bench.yaml --open-hardware
benchci benches self-test --bench bench.yaml --open-hardware --log-dir bench-health
```

Optional read-only checks:

```bash
benchci benches self-test --bench bench.yaml --open-hardware --read-inputs
benchci benches self-test --bench bench.yaml --open-hardware --read-measurements
```

Self-test is non-destructive by default. It does not flash, reset, toggle relays, drive GPIO outputs, or send protocol commands.

### `benchci run --dry-run-plan`

Preview execution without touching hardware:

```bash
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf --dry-run-plan
benchci run --bench bench.yaml --suite suite.yaml --dry-run-plan --skip-flash
benchci run --bench bench.yaml --suite suite.yaml --dry-run-plan --json
benchci run --bench bench.yaml --suite suite.yaml --dry-run-plan --plan-output plan.json
```

See [Validation, Self-Test, and Dry-Run Planning](diagnostics.md).

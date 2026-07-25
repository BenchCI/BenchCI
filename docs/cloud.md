# BenchCI Cloud

BenchCI Cloud lets you run real hardware tests through the BenchCI backend instead of connecting directly to a hardware machine.

It is the recommended model for CI pipelines, shared benches, private customer benches, and remote teams.

---

## Why Cloud Mode exists

Direct hardware access is inconvenient in CI:

- GitHub-hosted runners cannot usually reach your lab network
- exposing lab machines publicly is risky
- multiple engineers need shared access
- hardware should be queued and locked during runs
- results should be visible in a dashboard

Cloud Mode solves this by using a cloud-connected Agent.

```text
CI / Developer
      ↓
BenchCI CLI
      ↓
BenchCI Backend
      ↓
Queue / Scheduler
      ↓
Cloud-connected Agent
      ↓
Real hardware bench
      ↓
Artifacts + results
```

The Agent makes outbound requests to the backend, so your lab machine does not need a public inbound port.

---

## Before using Cloud Mode

Cloud Mode requires at least one BenchCI Agent registered to your workspace and connected to a real hardware bench.

Before running Cloud Mode, make sure:

- the Agent machine is connected to the DUT, debugger, UART/CAN/Modbus adapters, GPIO, relays, measurement devices, or other required hardware
- local execution works on the Agent machine
- the Agent is registered to your BenchCI workspace
- the bench appears in the dashboard
- the bench is online/idle
- you know the bench ID to use from CLI or CI

Check visible benches:

```bash
benchci benches list
```

If no benches appear, set up the Agent first:

[BenchCI Agent](agent.md)

---

## Login

```bash
benchci login
```

---

## List available benches

```bash
benchci benches list
```

Example output:

```text
my-bench
  configured_id: my-bench
  cloud_id: my-bench
  status: idle
```

The configured ID is the value passed to `benchci agent cloud --bench-id`.
BenchCI normally uses the same cloud ID. If that cloud ID is already in use,
the backend assigns a tenant-safe cloud ID and preserves the configured ID as
an alias. `benchci benches list` and `benchci benches show` display both.

Cloud runs may use either the cloud ID or a configured alias that resolves to
one accessible bench in the active workspace. If multiple accessible benches
share the same configured alias, the API returns `409` with candidate cloud
IDs; use one of those cloud IDs to disambiguate.

---

## Run on a specific bench

```bash
benchci run \
  --cloud \
  --bench-id my-bench \
  --suite suite.yaml \
  --artifact build/fw.elf
```

With richer diagnostics:

```bash
benchci run \
  --cloud \
  --bench-id my-bench \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --verbose
```

## Firmware handling modes

BenchCI Cloud supports three firmware handling models:

- `brokered`: the CLI uploads firmware bytes to BenchCI Cloud so the assigned Agent can fetch them.
- `delete_after_fetch`: the CLI uploads firmware bytes, then BenchCI queues and immediately attempts deletion after the assigned Agent fetches them. A failed storage operation is retried.
- `external_url`: the CLI sends a signed or private firmware URL plus SHA256. BenchCI stores only a redacted URL reference in run metadata and clears the full URL after Agent assignment.

Workspace owners/admins can set the default policy in the dashboard. A run can override it when needed.

Delete-after-fetch run example:

```bash
benchci run \
  --cloud \
  --bench-id my-bench \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --firmware-handling-mode delete_after_fetch
```

No-upload run example:

```bash
benchci run \
  --cloud \
  --bench-id my-bench \
  --suite suite.yaml \
  --firmware-url "$SIGNED_FIRMWARE_URL" \
  --firmware-sha256 "$FIRMWARE_SHA256"
```

The Agent downloads the URL on the hardware-connected machine, verifies the SHA256 before flashing, and fails the run with `FLASH_FAILED` if the bytes do not match.

---

## Run by capability

Instead of choosing a bench ID, you can request a bench by capability.

A bench exposes capabilities when its Cloud Agent syncs the bench summary to the backend. Define the hardware in `bench.yaml`, then start the Cloud Agent with a stable bench ID and optional tags:

```bash
benchci agent cloud \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --tag uart
```

BenchCI derives selectors from the synced bench:

- `--tag` from Agent `--tag` values, or from node tags when no Agent tags are supplied
- `--transport` from node transport backends
- `--flash-backend` from node flash backends
- `--has-gpio` from node GPIO definitions
- `--has-power` and `--power-backend` from power resources
- `--has-measurements` and `--measurement-backend` from measurement resources
- `--min-node-count` from the number of nodes

Check what the backend sees:

```bash
benchci benches show my-bench
```

```bash
benchci run \
  --cloud \
  --tag uart \
  --transport uart \
  --suite suite.yaml \
  --artifact build/fw.elf
```

Other useful selectors include:

```bash
# Flash backend
benchci run --cloud --flash-backend openocd --suite suite.yaml --artifact build/fw.elf

# GPIO / power / measurements
benchci run --cloud --has-gpio --suite suite.yaml --artifact build/fw.elf
benchci run --cloud --has-power --suite suite.yaml --artifact build/fw.elf
benchci run --cloud --has-measurements --suite suite.yaml --artifact build/fw.elf

# Specific power or measurement backend
benchci run --cloud --power-backend gpio_power --suite suite.yaml --artifact build/fw.elf
benchci run --cloud --measurement-backend scpi_power_supply_measurement --suite suite.yaml --artifact build/fw.elf

# Multiple selectors combine (all must be satisfied)
benchci run --cloud --transport uart --has-power --flash-backend openocd \
  --suite suite.yaml --artifact build/fw.elf
```

If multiple benches match your request, the scheduler selects an available bench based on capability and availability. Bench summaries can also expose power and measurement capabilities so teams can understand which benches are suitable for a given suite.

---

## Inspect runs

```bash
benchci runs list
benchci runs show <RUN_ID>
benchci runs events <RUN_ID>
benchci runs download <RUN_ID>
benchci runs export --format junit-xml <RUN_ID>
benchci runs export --format ctrf <RUN_ID>
```

The same runs can be inspected from the dashboard:

```text
https://app.benchci.dev
```

---

## Bench types

BenchCI Cloud can expose:

- shared benches
- reserved benches
- private customer benches
- managed demo benches

Typical meanings:

- `private` → owned by one workspace
- `managed_shared` → owned by BenchCI/internal workspace and shared by grants
- `managed_reserved` → reserved for a specific customer workspace
- `public_demo` → demo/evaluation bench where enabled

---

## Cloud Agent

A cloud-connected Agent polls the backend for assignments.

Example:

```bash
benchci agent cloud \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench
```

The Agent:

1. sends heartbeat
2. syncs capabilities
3. receives assignments
4. executes tests on the hardware-connected Agent
5. reports events
6. uploads artifacts, evidence reports, and structured run metadata
7. marks the run done or failed

---

## Evidence and traceability in Cloud Mode

Cloud Mode preserves the same evidence files generated by local execution. The Agent uploads the artifact ZIP to the backend.

The backend extracts and indexes useful fields such as:

- firmware SHA256
- firmware filename
- firmware handling mode, size, deletion/fetch/verification timestamps, and artifact audit events
- suite SHA256
- bench config SHA256
- static DUT identity from `bench.yaml`
- Git commit, branch, and remote
- CI provider and CI job URL
- requirement IDs
- test case IDs
- risk IDs
- LCOV coverage summary when uploaded
- external JUnit/CTRF import source and framework when attached
- fuzz summaries and campaign metadata inside `evidence.json`
- whether `evidence.html` is present

The dashboard shows these fields in the run detail view. The full evidence package remains available by downloading the artifacts ZIP.

This lets CI runs produce evidence that connects a firmware build, source revision, bench, suite, requirement IDs, fuzz seeds or first failing cases when present, and logs in one place.

## Coverage and external results

Upload LCOV coverage for a run:

```bash
benchci coverage upload coverage/lcov.info --run-id <RUN_ID>
```

Attach results from an existing external test workflow:

```bash
benchci runs attach-results report.xml --run-id <RUN_ID> --framework pytest --source pytest
benchci runs attach-results --run-id <RUN_ID> --log pytest.log --artifact artifacts/scope.png
benchci runs create-external --name "hardware nightly" --junit report.xml --artifacts artifacts/ --framework pytest --source pytest
benchci runs create-external --workspace-id <WORKSPACE_ID> --name "hardware nightly" --junit report.xml --framework pytest
```

Local log and artifact paths are uploaded into the external-results payload with SHA256 metadata, so the dashboard can offer authenticated downloads. URL artifacts remain external links. Inline uploads are bounded to keep run storage predictable: at most 20 logs, 50 artifacts, 256 KiB per log, 1 MiB per inline artifact, 1 MiB total log text, and 5 MiB total inline artifact content per request.

JUnit XML and CTRF JSON documents are limited to 5 MiB each. An inline log or artifact must use either `content` or `content_base64`, not both.

The backend owns the canonical JUnit XML and CTRF transformations so CLI exports and dashboard downloads use the same representation.

External runs use the active workspace by default. Pass `--workspace-id` when a multi-workspace user or CI token needs to create the run in a specific workspace.

## Release review

Release evidence bundles support `draft`, `under_review`, `approved`, and `rejected` review states. Submit, approve, and reject actions require a comment and are recorded as hash-linked review events. Approved bundles are locked for review integrity, cannot be removed through the normal delete endpoint, and remain downloadable as evidence packages.

## Run and bundle lifecycle

Workspace owners/admins can remove runs from the dashboard when the run is not
actively assigned or executing. Runs already included in a release bundle
cannot be removed until the bundle is removed. Run removal deletes the run's
events, artifact audit rows, and stored artifact files.

Owners/admins can remove non-approved release bundles. Approved bundles remain
locked. Firmware-byte deletion is separate from run deletion: deleting retained
firmware keeps the run evidence, hashes, and audit history.

## Report templates

Release bundles can generate human-readable reports from the same bundle data used by the ZIP evidence package:

```bash
benchci releases report <BUNDLE_ID> --template generic-qa --format html --out release-report.html
benchci releases report <BUNDLE_ID> --template iec-62304-style --format pdf --out release-report.pdf
benchci releases report <BUNDLE_ID> --template iso-26262-style --format pdf
```

Available templates are `generic-qa`, `iec-62304-style`, and `iso-26262-style`. The generated report includes release metadata, review state and comments, run summary, DUT identity, firmware hashes, LCOV summary, traceability rows, and external-result source labels.

Reports are review aids generated from BenchCI evidence. They must not be presented as an official assessment, regulatory approval, or replacement for your organization's quality process.

## Workspace visibility

Cloud Mode is workspace-aware.

Users see benches, runs, and artifacts that:

- belong to their workspace
- are shared with their workspace
- are reserved for their workspace
- are public demo benches where enabled

Your active workspace determines what `benchci benches list` and `benchci runs list` show.

---

## Recommended CI pattern

Use secrets for BenchCI credentials and bench selection.

Typical variables:

```text
BENCHCI_EMAIL
BENCHCI_PASSWORD
BENCHCI_BENCH_ID
```

Optional variable for a stable CI machine identity:

```text
BENCHCI_MACHINE_ID=my-repo-ci
```

Most hosted CI jobs should leave `BENCHCI_MACHINE_ID` unset. Set it only for a persistent runner or a non-parallel pipeline lane that should always count as the same CI runner. If another active CI session already uses the same value, login is blocked until that session logs out or expires.

Authenticator MFA is for human dashboard and CLI sign-ins. CI jobs should use
the normal `benchci login` automation flow shown below, which creates a
short-lived CI session; do not store TOTP codes or authenticator secrets in CI.

Typical CI run:

```bash
benchci login \
  --email "$BENCHCI_EMAIL" \
  --password "$BENCHCI_PASSWORD"

benchci run \
  --cloud \
  --bench-id "$BENCHCI_BENCH_ID" \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --verbose
```

The CLI automatically logs out the CI session after `benchci run --cloud` completes, freeing the runner slot immediately regardless of run outcome. No explicit `benchci logout` is needed in CI.

See:

- [GitHub Actions](github_actions.md)
- [GitLab CI](gitlab_ci.md)

---

## Common issues

### No benches listed

Check that:

- the Agent is running
- the Agent token is valid
- the workspace is active
- the bench ID is registered
- you are logged into the expected workspace

### Bench is offline

Check the Agent process and network access from the Agent machine to the backend.

### Run stays queued

Check whether the requested bench is busy/offline or whether capability filters are too restrictive.

### Artifact not found

Check the artifact path in CI and make sure the build job passes it to the hardware-test job.

## Bench health and scheduling

Cloud Mode uses bench health when scheduling runs.

The scheduler assigns runs only to benches with:

```text
healthy
degraded
```

The scheduler avoids benches with:

```text
failing
unknown
missing health
malformed health
```

A queued run remains queued if no healthy/degraded matching bench is available. This prevents known-unhealthy benches from producing misleading hardware test failures.

Check bench state:

```bash
benchci benches list
benchci benches show my-bench
```

## Reliability history and flaky tests

BenchCI also analyzes recent terminal run history so a team can spot patterns that a single run cannot show.

For each bench/test-case pair, BenchCI summarizes the last 10 and last 30 completed runs. The run detail API, dashboard, and `benchci runs show` can show warnings such as:

- a test failed at least 3 of the last 10 runs on the same bench
- the same test passes frequently on another bench but fails on this bench
- the bench has repeated infrastructure failures
- the bench agent is offline or stale

These warnings do not block runs or releases. They are investigation aids. A failed run is still a failed run; the history view helps you decide whether to start with firmware/test logic or with the bench fixture, cabling, adapters, Agent host, or lab infrastructure.

Failed-run responses may include a `failure_assessment` with the canonical source, a history-backed likely source, confidence, reasons, and supporting signals. This assessment is advisory. BenchCI never rewrites the canonical category or source emitted by the runner.

BenchCI uses these signals separately:

- **Firmware or test failure**: the test reached the DUT and reported an assertion, timeout, protocol failure, or other result that belongs to the firmware/test path.
- **Bench infrastructure failure**: BenchCI could not complete the hardware workflow because of a bench, fixture, power, flash, Agent, adapter, or lab-host problem.
- **Historically flaky behavior**: recent history shows repeated failures for the same test on the same bench, even when the current failure source is not definitive.

Inspect the signals from the CLI:

```bash
benchci runs show <RUN_ID>
benchci benches show my-bench
```

See [Cloud Agent Health, Resource Locking, and Scheduling](cloud_agent_health.md).

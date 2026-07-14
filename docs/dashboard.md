# Dashboard

The BenchCI dashboard is the browser-based control center for your workspace.

Dashboard URL:

```text
https://app.benchci.dev
```

Use it after your first Cloud run to inspect status, events, artifacts,
evidence, firmware assurance, DUT identity, coverage, reliability history, and
failure context. You can also manage release review workflows and submit
customer requests from your active workspace.

---

## Why the dashboard matters

The CLI is good for running tests.

The dashboard is good for understanding the state of your hardware validation system:

- which benches are online
- which runs are queued or running
- what failed recently
- which workspace resources are available
- what artifacts were produced
- what evidence, identity, coverage, and firmware-assurance metadata was indexed
- whether recent history suggests a flaky test or bench issue
- which release bundles are awaiting review
- whether a bench is ready for CI use

---

## Login

Use your BenchCI email and password.

If you are creating the first account for a company, register a workspace owner account.

If you were invited to an existing workspace, use the invite link. Existing BenchCI users should sign in from the invite link to accept the invite; new users should register from the invite link.

Users who belong to multiple active workspaces can select the active workspace from the dashboard sidebar. CLI users can switch with `benchci workspaces use <workspace_id>`.

---

## What the dashboard shows

The dashboard is designed to show:

- workspace health
- online/offline benches
- queued/running runs
- recent failures
- run timelines
- run events
- bench capabilities, including power and measurement resources where available
- artifact, evidence JSON/HTML, JUnit, and CTRF downloads where allowed
- firmware handling status and artifact audit history
- LCOV coverage summaries
- configured or UART-verified DUT identity
- experimental controlled fault-injection summaries
- fuzz campaign summary, seed, first failing case, and log path when fuzzing is used
- captured metrics and measurements where available
- requirement/test/risk traceability
- reliability history, flaky-test warnings, and advisory failure assessments
- release review state, hash-linked review events, and release report downloads
- customer bug reports and feature requests for the active workspace
- starter `bench.yaml` and `suite.yaml` generation
- workspace onboarding, artifact policy, teammates, roles, invites, and Agent tokens

---

## Core pages

### Overview

Shows high-level workspace health:

- online benches
- offline benches
- queued runs
- running runs
- 7-day pass rate (shown as "—" when no completed runs exist in the window)
- recent failures
- benches under warning or failure conditions
- release bundles currently under review
- Runs This Month — always visible; shows remaining count when a monthly run cap applies

Use this page as the shared workspace status view.

### Runs

Shows run history and run detail.

Use it to inspect:

- status
- bench assignment
- agent assignment
- DUT revision, serial, asset, or fixture-slot filters
- duration
- error classification
- structured failure explanation and suggested checks
- advisory reliability and historical failure-source assessment
- event timeline
- evidence report summary
- firmware handling, deletion state, and artifact audit events
- configured or verified DUT identity
- LCOV coverage summary
- imported external test source and downloadable artifacts
- fuzzing and experimental fault-injection summaries
- requirement/test/risk traceability
- artifacts, evidence HTML/JSON, JUnit, and CTRF exports

Workspace owners and admins can remove runs that are not actively assigned or
executing. A run included in a release bundle cannot be removed until the
bundle is removed. Removing a run deletes its events, audit rows, and stored
artifact ZIP; deleting retained firmware bytes is a separate action that keeps
the run evidence and audit history.

BenchCI admins can set workspace-specific generated artifact retention from the
Admin panel. This controls artifact ZIP cleanup and non-bundled completed/failed
run cleanup; release bundle packages and approved review trails are managed
separately.

### Benches

Shows benches visible to your workspace.

Bench cards include:

- bench ID
- name
- status
- type
- tags
- agent
- transports
- flash backends
- node count
- startup health status and diagnostic findings
- scheduler eligibility
- last-10 and last-30 run-history summaries
- recent outcomes and top flaky tests where available

Workspace owners and admins can remove a bench that is not currently running by clicking **Remove** on the bench card. A removed bench can re-register the next time its Agent connects; removing it does not permanently delete the bench record or prevent future use.

### Config Builder

Creates starter `bench.yaml` and `suite.yaml` files in the browser.

The Config Builder is preset-based and export-only. It does not save config to the cloud, deploy Agent settings, or create database records. Use it to choose a common flow, adjust the compact form fields, preview both YAML files, then copy or download them into your repository.

Available presets match `benchci init`:

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

After exporting, validate and inspect the files with the CLI:

```bash
benchci doctor --bench bench.yaml
benchci validate --bench bench.yaml --suite suite.yaml
```

### Releases

Shows release bundles and their associated hardware run evidence.

Use it to:

- create a new release bundle from a name, optional version/description, and completed cloud run IDs
- view the latest-result coverage matrix for the bundle, with the full per-run matrix preserved in the downloaded ZIP
- inspect included runs, DUT context, LCOV summaries, and coverage trends
- submit a draft or rejected bundle for review with a required comment
- approve or reject an under-review bundle as a workspace owner/admin
- inspect hash-linked review events
- download the evidence ZIP
- view or download review reports as HTML or PDF

Approved bundles are locked for review integrity. Owners and admins can remove
other bundles, but approved bundles cannot be removed through the normal
dashboard or API path.

Generated reports are review aids; they are not certification or regulatory
approval.

### Requests

Shows customer request intake for the active workspace.

All active workspace members can submit:

- bug reports
- feature requests

Requests include:

- type
- severity
- title and description
- optional run ID
- optional bench ID
- the current dashboard page URL
- workspace and requester context

The page also shows recent workspace request history and the current request status:

```text
Received
Reviewing
Planned
Done
Rejected
```

Repeated requests may be grouped during BenchCI review. The dashboard shows the current status, but request submission does not create a public roadmap, vote count, or customer-facing SLA.

### Workspace

Shows workspace details, status, usage limits, firmware artifact policy,
onboarding commands, team access, and Agent token management where your role
allows.

Use this page when:

- connecting a new Agent
- checking Cloud Mode workspace setup
- copying CLI commands
- selecting the default firmware handling mode and retention policy
- inviting teammates
- changing teammate roles, suspending access, and removing records where allowed
- managing workspace Agent tokens

## Run detail evidence

For Cloud runs, the run detail panel can show an Evidence Report section with:

- firmware filename and SHA256
- Git commit, branch, and remote
- CI provider and CI job URL
- bench ID and Agent ID
- suite hash
- bench config hash
- result status
- whether `evidence.html` and `manifest.json` are included in artifacts
- evidence quality warnings for missing or incomplete fields
- captured metrics and measurements when the suite records them
- protocol fuzzing summary, campaigns, seeds, failures, first failing case, and fuzz log hints when the suite uses fuzzing
- configured and UART-verified DUT identity, including verification status and response hash
- experimental fault-injection recovery and watchdog summaries
- LCOV line, function, and branch coverage
- imported external-result source/framework and authenticated artifact downloads
- measurement resource, backend, preset, SCPI query, raw response, and instrument address when available
- lightweight metric trend previews for repeated numeric measurements

When these artifacts are present, the dashboard can open `evidence.html`,
download `evidence.json`, and export JUnit XML or CTRF JSON directly from run
detail. The full evidence package remains available in the artifacts ZIP.

## Traceability view

If `suite.yaml` includes traceability fields, the dashboard can show:

- requirement IDs
- test case IDs
- risk IDs
- tags
- per-test mapping

This helps teams connect a failed or passed hardware run to the requirement, risk, or test case it covers.

## Failure context

Failed runs can show structured failure information:

- category
- title
- explanation
- suggested checks
- failed step
- relevant artifact paths

This reduces generic “unknown failure” cases and points users toward the right log or hardware check.

## Bench health and failure source

The dashboard can show bench health on bench cards:

```text
Healthy
Degraded
Failing
Unknown
```

Bench health panels can include:

- health summary
- last checked timestamp
- scheduling eligibility message
- pass/warn/fail/skip counts
- warning or failing diagnostic checks
- categories and suggested fixes

Failed run details can show a likely failure source:

```text
Firmware
Test logic
Bench infrastructure
Agent / cloud
Configuration
Unknown
```

This helps users decide whether a failure is more likely to come from the firmware, the test suite, the bench infrastructure, the Agent/cloud path, or configuration.

When enough history exists, run detail can separately show a historical
failure assessment with the canonical source, history-suggested source,
confidence, reasons, and supporting signals. This is advisory only and never
rewrites the canonical failure or run result.

Run detail can also show reliability-history cards:

```text
Possible bench issue
Flaky test
Cross-bench mismatch
```

These cards use recent completed run history for the same bench and test case. They are warnings for investigation, not automatic pass/fail overrides. The Benches view shows the same history as a bench reliability indicator with last-10 and last-30 summaries, recent outcomes, and top flaky tests when present.

See [Cloud Agent Health, Resource Locking, and Scheduling](cloud_agent_health.md).


## Measurements and metrics

Run detail can show measurement cards for values captured by `measure` and `assert_metric` steps.

For SCPI-backed measurements, cards can include:

- metric name
- value and unit
- quantity
- pass/fail assertion status
- resource name
- backend, such as `scpi_measurement` or `scpi_power_supply_measurement`
- preset, such as `generic`, `owon_sp`, `rigol_dp_basic`, or `keysight_basic`
- SCPI source query
- instrument address
- raw response where available
- measurement log path where available

This makes electrical evidence visible without requiring every user to open `results.json` first.

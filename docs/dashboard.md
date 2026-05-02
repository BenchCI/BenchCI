# Dashboard

The BenchCI dashboard is the browser-based control center for your workspace.

Dashboard URL:

```text
https://app.benchci.dev
```

Use it after your first Cloud run to inspect run status, events, logs, artifacts, and failure context.

---

## Why the dashboard matters

The CLI is good for running tests.

The dashboard is good for understanding the state of your hardware validation system:

- which benches are online
- which runs are queued or running
- what failed recently
- which workspace resources are available
- what artifacts were produced
- whether a bench is ready for CI use

---

## Login

Use your BenchCI email and password.

If you are creating the first account for a company, register a workspace owner account.

If you were invited to an existing workspace, use the invite link.

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
- artifacts
- evidence report summary
- captured metrics and measurements where available
- requirement/test/risk traceability
- setup guidance

---

## Core pages

### Overview

Shows high-level workspace health:

- online benches
- offline benches
- queued runs
- running runs
- pass/fail signals
- recent failures

Use this page as the team-level status view.

### Runs

Shows run history and run detail.

Use it to inspect:

- status
- bench assignment
- agent assignment
- duration
- error classification
- structured failure explanation and suggested checks
- event timeline
- evidence report summary
- requirement/test/risk traceability
- artifacts

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

### Setup

Shows onboarding commands and workspace setup guidance.

Use this page when:

- connecting a new Agent
- checking Cloud Mode setup
- copying CLI commands
- onboarding a new workspace

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
- captured metrics and measurements when the suite records them

The full evidence report is available in the artifacts ZIP as `evidence.html` and `evidence.json`.

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

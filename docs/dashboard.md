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
- bench capabilities
- artifacts
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
- event timeline
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

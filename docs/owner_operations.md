# Workspace Owner Operations

Use this page when you own or administer a BenchCI workspace and need to onboard hardware, manage Agent access, review runs, or coordinate support requests.

---

## Dashboard

Use the BenchCI dashboard for workspace operations:

```text
https://app.benchci.dev
```

From the dashboard, workspace owners and admins can review workspace status,
manage connected benches, create or revoke Agent tokens, manage teammates and
roles, set firmware artifact policy, inspect or remove eligible runs, review
release bundles, download artifacts/reports, and submit support or feature
requests.

## Typical Onboarding Flow

1. Create a workspace in the BenchCI dashboard.
2. Verify your email and confirm the workspace is active or in trial.
3. For commercial usage after the 30-day Team-feature trial, contact `tech@benchci.dev`.
4. Create an Agent token if your team will connect lab hardware.
5. Start the Agent on the machine connected to your hardware.
6. Confirm the bench appears in the dashboard.
7. Run an end-to-end validation from the CLI, CI, or Cloud Mode.
8. Review results, artifacts, evidence, and any failure details in the dashboard.
9. Submit onboarding blockers or product requests from the dashboard Requests page.

## Trial And Workspace Limits

New workspaces start a 30-day trial of Team features after email verification. Workspace
seat, bench, concurrent CI runner, and monthly run limits are shown in the
dashboard where available.

For commercial usage after the trial, contact `tech@benchci.dev`. If your
workspace status, limits, or access do not look correct, contact BenchCI support
from the dashboard.

## Agent Tokens

Agent tokens let a lab Agent connect hardware to your BenchCI workspace. Create a separate token for each lab machine or Agent service. A single Agent can register multiple benches from the same machine, but do not reuse one token across different lab machines.

The full token is shown once when it is created. Store it in a secure secret store or password manager. BenchCI cannot show the full token again later.

You can manage tokens from the dashboard:

- **Revoke** a token to disable an Agent without deleting the record.

Workspace owners/admins revoke tokens from the normal workspace dashboard.
Permanent token-record deletion is an administrative cleanup operation and is
not exposed as a normal workspace-owner action.

Keep Agent tokens out of source control, CI logs, screenshots, and shared documents. Rotate a token if it may have been exposed.

## Bench Management

Workspace owners and admins can remove benches from the dashboard when a bench is idle. Removing a bench cleans up the visible bench list, but the Agent can register it again if it reconnects with the same bench ID.

Use bench removal when hardware is renamed, moved, retired, or accidentally registered with the wrong identifier.

## Firmware Artifact Policy

Owners and admins can set the workspace default:

- `brokered`
- `delete_after_fetch`
- `external_url`

For brokered firmware, the policy also sets the retention window. Evidence
metadata retention is controlled separately. Per-run overrides are available
from the CLI.

Run detail shows firmware SHA256, handling mode, fetched/verified/deleted
timestamps, redacted external references, and artifact audit events. Deleting
retained firmware bytes keeps the run record, evidence metadata, hashes, and
audit history.

## Run And Release Lifecycle

Owners and admins can remove runs that are not actively assigned or executing.
Runs included in a release bundle must be unlinked by removing the bundle first.
Run removal deletes events, audit rows, and stored artifacts for that run.

Release bundles can move through `draft`, `under_review`, `approved`, and
`rejected`. Developers can submit for review; owners/admins approve or reject.
Every action requires a comment and creates a hash-linked review event.
Approved bundles are locked against normal deletion.

## Requests And Support

Use the dashboard Requests page to report bugs, request features, or share onboarding blockers. Include the affected workspace, bench, run, and artifact context when possible.

Requests may show status updates such as received, reviewing, planned, done, or rejected. For urgent production blockers, include the run ID and a short description of the business impact.

## Production Readiness Checklist

A workspace is ready for production hardware validation when:

- users can sign in and access the correct workspace
- the workspace status and limits look correct
- the Agent can connect from the lab machine
- the bench appears in the dashboard
- the CLI can list and target the bench
- a Cloud Mode or Agent-backed run can execute
- run events and logs appear in the dashboard
- artifacts can be downloaded
- `results.json`, `evidence.json`, `evidence.html`, and `manifest.json` are present where expected
- evidence, traceability, DUT identity, coverage, fault, fuzz, and measurement cards appear when the run records that metadata
- failed runs show clear failure context
- recent history and advisory failure assessment are understandable when available
- firmware artifact handling and audit events match workspace policy
- a release bundle can be created, reviewed, downloaded, and reported on if the workflow uses release bundles

## Evidence Review

For a new workspace or bench, review at least one successful run and one failed run before relying on the setup in production CI.

Check that:

- the CLI prints useful run and evidence summaries
- dashboard run detail shows failure context
- canonical failure source remains distinct from any history-backed assessment
- artifacts include result and evidence files
- traceability fields appear when `suite.yaml` includes requirement, test case, or risk IDs
- verified identity and experimental fault evidence are visible when those features are configured
- approved release records preserve review comments and event hashes
- the team understands that BenchCI records verification evidence, but does not certify the product by itself

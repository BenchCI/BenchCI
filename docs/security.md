# Security

Use this page to understand account sessions, Agent tokens, Cloud Agent connectivity, workspace isolation, and recommended operational practices.

## Authentication

BenchCI currently supports:

- user sessions for CLI access
- agent tokens for machine authentication
- optional protected Agent endpoints

## Cloud Agent Connectivity

Cloud-connected agents initiate outbound connections to the backend.

This reduces the need for exposing inbound hardware machines publicly.

## Resource Isolation

BenchCI supports workspace-oriented ownership models for:

- runs
- benches
- agents

This enables separation between customer environments.

## Artifacts

Run outputs such as logs and results are scoped to the owning workspace/session path.

## Firmware artifact handling

BenchCI Cloud records firmware integrity metadata separately from retained firmware bytes.

Workspace policy controls the default run handling mode:

- `brokered`: BenchCI Cloud brokers firmware bytes to the assigned Agent.
- `delete_after_fetch`: BenchCI Cloud deletes retained source firmware bytes after the assigned Agent fetches them.
- `external_url`: the run references a customer-controlled URL and SHA256; BenchCI stores a redacted URL reference and clears the full URL after Agent assignment.

Runs store firmware SHA256, filename, size, handling mode, fetch/verification/deletion timestamps, and artifact audit events. Customer-initiated firmware deletion keeps evidence metadata, hashes, and audit history unless workspace policy is changed to remove evidence metadata.

Use `benchci run --cloud --firmware-url URL --firmware-sha256 SHA256` when firmware bytes should not be uploaded to BenchCI Cloud. The Agent verifies the downloaded bytes before flashing.

The no-upload path supports Agent-reachable HTTP or HTTPS URLs, including short-lived signed URLs and authenticated private artifact-store links encoded by the provider. Local filesystem paths and `file://` URLs are not supported by `--firmware-url`; keep those artifacts behind an HTTP(S) endpoint reachable by the assigned Agent.

## Evidence and artifact sensitivity

Evidence artifacts may contain information that should be treated as internal engineering data:

- firmware filenames and hashes
- Git commit, branch, and remote URL
- CI job URL
- bench and Agent identifiers
- test names, requirement IDs, risk IDs, and logs
- input snapshots of `bench.yaml` and `suite.yaml`
- captured metrics and measurements
- DUT hardware revision, serial number, asset ID, fixture slot, and verification status
- imported external-result logs and artifacts
- protocol fuzzing inputs and first failing cases
- experimental fault-injection targets and recovery observations
- release review comments and actor identifiers
- artifact integrity manifests

Do not publish artifact ZIPs unless you have reviewed them. Treat evidence reports as workspace-scoped engineering records.

## Agent token lifecycle

Workspace owners and admins with an active account can create Agent tokens from the BenchCI dashboard. BenchCI admins may also issue tokens during initial onboarding.

**Token visibility**: The plaintext token value is shown exactly once — at
creation time in the workspace dashboard or administrative tooling. After that,
only the token ID and status are visible. There is no way to retrieve the token
value later.

**Revoke vs. permanent delete**:
- **Revoke** disables the token. The Agent using it will receive 401 on its next heartbeat. The token record remains and can be audited.
- **Permanent delete** removes the token record entirely. This is an
  administrative cleanup operation; workspace owners/admins use revoke in the
  normal workspace UI.

Tokens are stored as SHA-256 hashes. Existing plaintext tokens are automatically migrated to hashed form on the next Agent connection.

## Token and secret handling

Do not store Agent tokens, account passwords, or CI secrets in `bench.yaml`, `suite.yaml`, or evidence reports. Use environment variables and CI secret stores.

For remote GPIO, HTTP relay, and HTTP measurement backends, prefer environment variables or private lab-network endpoints. Do not commit access tokens, passwords, or private controller URLs unless they are safe to share.

## Recommended Best Practices

- rotate tokens periodically
- run agents on dedicated lab machines
- restrict unnecessary inbound ports
- physically secure lab hardware
- review artifact retention policies

## Workspace Access

BenchCI uses workspaces to scope:

- users
- benches
- runs
- agents
- customer requests
- artifacts
- release bundles and review events
- workspace usage limits

A user only sees benches, runs, artifacts, and customer request history available to the active workspace. BenchCI admins can review the global customer request queue for triage.

## Dashboard Sessions

The dashboard uses the same account/workspace model as the CLI. Keep browser sessions on trusted machines and rotate credentials if access is no longer needed.

Authenticator MFA can be enabled per user for human dashboard and CLI sign-ins.
Users receive one-time recovery codes during setup or regeneration; store them
outside BenchCI because they are not shown again. BenchCI sends email alerts
when MFA is enabled, disabled, reset, or recovery codes are regenerated.

Lost phone plus lost recovery codes requires a BenchCI admin/support MFA reset.
That reset clears the user's MFA state and recovery codes, revokes all sessions,
and records a security audit event. MFA is not required for CI automation
sessions; CI should use the documented `benchci login` CI flow rather than
storing TOTP codes or authenticator secrets.

Workspace roles are `owner`, `admin`, `developer`, and `viewer`. Sensitive
mutations are role-gated: artifact-policy changes, Agent token creation/revoke,
member management, run/bundle removal, release approval/rejection, and workspace
configuration are restricted to the roles allowed by the backend.

## Trial And Commercial Access

New workspaces start a 30-day trial of Team features after email verification. For
commercial usage after the trial, contact `tech@benchci.dev`.

## Run And Release Deletion Safety

Run deletion is blocked while a run is actively assigned or executing. A run
that belongs to a release bundle cannot be deleted until the bundle is removed.
Deleting a run removes its events, artifact audit rows, and stored artifact
files.

Generated run/evidence artifact retention is workspace-configurable by BenchCI
admins. The current default is 365 days unless a workspace-specific policy is
set; retained firmware-byte handling is controlled separately by the workspace
artifact policy.

Release bundles record hash-linked review events. Approved bundles are locked
and cannot be removed through the normal delete endpoint. This protects the
review trail from accidental cleanup. Deleting retained firmware bytes is a
separate operation that preserves run evidence, SHA256 metadata, and audit
events.

## Resource Locking And Health Safety

BenchCI uses resource locking to prevent concurrent runs on the same machine from using the same physical interface at the same time.

If another run is already using a required resource, BenchCI fails early with a resource-lock error instead of letting two runs fight over the same hardware.

Locks are host-wide by default: `/tmp/benchci-locks` on POSIX and
`%PROGRAMDATA%\BenchCI\locks` on Windows. This lets CI service accounts and
interactive users coordinate access to the same hardware. Set
`BENCHCI_LOCK_DIR` only when the replacement is a shared, machine-wide
directory; BenchCI fails clearly if it cannot establish a safe shared lock
location.

Agent startup health checks are non-destructive by default and should not expose secrets. Keep Agent tokens, HTTP relay credentials, and measurement-controller credentials in environment variables or private secret stores.

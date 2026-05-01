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

## Evidence and artifact sensitivity

Evidence artifacts may contain information that should be treated as internal engineering data:

- firmware filenames and hashes
- Git commit, branch, and remote URL
- CI job URL
- bench and Agent identifiers
- test names, requirement IDs, risk IDs, and logs
- input snapshots of `bench.yaml` and `suite.yaml`

Do not publish artifact ZIPs unless you have reviewed them. Treat evidence reports as workspace-scoped engineering records.

## Token and secret handling

Do not store Agent tokens, account passwords, or CI secrets in `bench.yaml`, `suite.yaml`, or evidence reports. Use environment variables and CI secret stores.

For remote GPIO, prefer `token_env` so the token is read from the environment rather than committed to source control.

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
- artifacts
- plan limits

A user only sees benches and runs available to the active workspace.

## Dashboard Sessions

The dashboard uses the same account/workspace model as the CLI. Keep browser sessions on trusted machines and rotate credentials if access is no longer needed.

## Manual Activation

Early access and paid workspace activation are handled manually by the BenchCI owner/admin process. This avoids exposing payment automation before the product requires self-serve billing.

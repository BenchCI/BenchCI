# Firmware Handling Assurance

BenchCI gives you three ways to get firmware to the bench agent without compromising your supply chain or IP boundaries. This document explains the security model behind each mode, what BenchCI stores, and where the trust boundaries are.

## The Three Modes

### `brokered` (default)

Your CI pipeline uploads the firmware binary to BenchCI cloud storage. BenchCI forwards it to the agent over an encrypted channel. BenchCI holds the binary only for the duration of your configured retention window (default: 24 hours after the run starts).

**What BenchCI stores:** BenchCI stores the binary in workspace-scoped artifact storage for the configured retention window. Only agents with a valid run assignment for your workspace can download it through the assignment flow. If your team needs specific contractual commitments for storage encryption, region, retention, or staff access, confirm those requirements in your workspace agreement before using brokered firmware storage.

**When to use it:** When you have no external artifact store and want the simplest setup.

---

### `delete_after_fetch` (privacy-first)

Same upload path as `brokered`, but after the agent confirms receipt BenchCI
commits a deletion job and immediately dispatches it. If the storage provider
is temporarily unavailable, the run assignment still proceeds and deletion is
retried with backoff. The artifact audit log records `firmware_deleted_at` and
the successful-deletion event only after the physical object is gone.

**What BenchCI stores:** The SHA-256 hash, filename, and size remain in the run record for evidence review. The binary is gone.

**When to use it:** When regulatory or IP requirements prohibit third-party storage of your firmware binary.

---

### `external_url` (no-upload)

You pass `--firmware-url` and `--firmware-sha256` to the BenchCI CLI or API. BenchCI never receives the binary. The agent downloads it directly from your artifact store (S3, GitLab Package Registry, GitHub Releases, internal CDN, etc.) using the URL you provide.

The Agent streams external firmware with a 200 MiB safety limit. Signed URL paths and query parameters are redacted from dashboard and failure output; fetch failures record only the redacted host reference and HTTP status.

BenchCI redacts any query-string tokens from the URL before storing it. The full URL (including secrets) is visible to the agent during assignment but cleared from BenchCI storage once the agent acknowledges receipt.

**What BenchCI stores:** The redacted URL, SHA-256 hash, filename, and agent-verified hash confirmation.

**When to use it:** When you already have a signed-URL artifact workflow and want zero firmware egress to BenchCI.

---

## Workspace Isolation

Every firmware binary, run record, and evidence bundle is scoped to a workspace ID. Cross-workspace access requires an explicit bench-sharing grant configured by a workspace owner. Agent tokens are tied to the agent registration, not the workspace, but each run assignment is workspace-verified before the agent can fetch artifacts.

## Agent Token Trust Boundaries

- Agent tokens are long-lived registration credentials. Store them in your CI secret manager (GitHub Actions secrets, GitLab CI variables, etc.).
- An agent token grants the ability to pull run assignments and report results for benches registered under that token. It does **not** grant workspace admin access.
- Rotate agent tokens via the workspace settings page.

## Retention and Deletion Policy

| Mode | Binary retained | Hash retained | Deletion proof |
|------|----------------|---------------|----------------|
| brokered | Until retention window expires | Forever | `firmware_deleted_at` in run record |
| delete_after_fetch | Deletion dispatched immediately after fetch; retried on storage failure | Forever | `firmware_deleted_at` + successful-deletion audit event |
| external_url | Never uploaded | Forever | N/A — never held |

Retention windows are configured per workspace under **Settings → Artifact Policy**.

## Support Access

BenchCI does not provide a customer-managed support-access grant for firmware binaries. If you need to share diagnostic data with support, use redacted evidence packages or artifacts you intentionally provide outside the firmware retention path.

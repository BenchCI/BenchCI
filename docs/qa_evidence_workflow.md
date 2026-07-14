# QA Evidence Workflow

Use this page when you need to move from individual run evidence to a bundled artifact you can bring to a release review or attach to a QA record.

BenchCI produces structured verification evidence for each hardware test run.
Workspaces can package multiple runs into a **release evidence bundle** — a
self-contained ZIP with per-run evidence, a requirement coverage matrix, review
history, LCOV summaries, and a hash manifest.

**What BenchCI does not do:** The bundle is a structured record. It is not a product certification and it does not replace your company's sign-off procedure. Whether a bundle meets a specific customer or release requirement is a judgment call made by your team and your QA process.

---

## What is a release evidence bundle?

A release evidence bundle packages the runs you choose into a single ZIP file. It includes:

```text
release-evidence-v1.2.3.zip
  release-summary.json      ← bundle metadata and coverage counts
  release-summary.html      ← human-readable bundle summary report
  coverage-matrix.json      ← full per-run requirement/test rows
  coverage-matrix-latest.json
                            ← latest result per requirement/test pair
  coverage-matrix.csv       ← full matrix, spreadsheet-friendly
  coverage-matrix.html      ← standalone full coverage table
  HASHES.txt                ← SHA256 of every file in the bundle
  runs/
    <run_id>/
      evidence.json
      evidence.html
      manifest.json
      external-artifacts/
        ...
```

Inline artifacts imported from external JUnit/CTRF workflows are included under
the corresponding run when present. `release-summary.json` and
`release-summary.html` also include the review state, lock timestamp,
hash-linked review events, included-run DUT identity, fault summary counts, and
LCOV coverage summary.

Each bundle is workspace-permissioned. Only members of your workspace can list,
download, or view bundles.

---

## How to create a bundle (CLI)

The `benchci releases` command group manages bundles.

### 1. Find the run IDs you want to include

```bash
benchci runs list
```

Run IDs appear in the `RUN ID` column. You can also copy run IDs from the dashboard Runs page.

Only terminal runs (status `done` or `failed`) can be included. Up to 100 runs per bundle.

### 2. Create the bundle

```bash
benchci releases create "Firmware v1.2.3 Release" \
  --version "1.2.3" \
  --runs 4c1e9b7a2fd3,7b3fa1c8e921 \
  --description "Pre-release validation runs against REQ-BOOT and REQ-COMM"
```

`--version` and `--description` are optional. The bundle name is required (positional) and `--runs` is required.

The CLI prints the bundle ID on success:

```text
Bundle created: bnd_a3f9c2e1b047
Status: ready
```

Bundle generation is synchronous and completes before the command returns. For typical release bundles (2–20 runs) this takes a few seconds.

### 3. Download the bundle

```bash
benchci releases download bnd_a3f9c2e1b047
```

The ZIP is written to the current directory as
`benchci_release_bnd_a3f9c2e1b047.zip` unless `--out` is provided.

### Other CLI commands

```bash
benchci releases list              # list all bundles in your workspace
benchci releases show bnd_a3f9c2e1b047   # show bundle metadata
benchci releases report bnd_a3f9c2e1b047 --format html
benchci releases report bnd_a3f9c2e1b047 --template iec-62304-style --format pdf
```

---

## How to create a bundle (Dashboard)

1. Open the **Releases** view in the BenchCI dashboard.
2. Click **Create bundle**.
3. Enter the bundle name, optional version and description, and paste or type the run IDs to include.
4. Click **Create**. The bundle appears in the list with status `ready` when generation completes.
5. Click **Download** to save the ZIP.

The **Releases** view also shows the coverage summary, included runs, DUT and
LCOV context, review state/history, and report downloads.

## Review and sign-off

New bundles start in `draft`.

The dashboard supports this review flow:

```text
draft or rejected
        ↓ submit with comment
under_review
        ↓ approve or reject with comment
approved or rejected
```

Workspace developers, admins, and owners can submit a bundle for review.
Workspace owners and admins can approve or reject it. Each action requires a
comment and creates a hash-linked review event. The bundle ZIP is regenerated
after review changes so the downloaded package contains the current review
history.

Approved bundles are locked and cannot be removed through the normal dashboard
or API delete path. Owners and admins may remove non-approved bundles. A run
included in any release bundle cannot be removed until that bundle is removed.

## Human-readable release reports

Generate HTML or PDF reports from the same evidence used by the bundle:

```bash
benchci releases report bnd_a3f9c2e1b047 \
  --template generic-qa \
  --format html \
  --out release-report.html

benchci releases report bnd_a3f9c2e1b047 \
  --template iso-26262-style \
  --format pdf \
  --out release-report.pdf
```

Available templates are:

- `generic-qa`
- `iec-62304-style`
- `iso-26262-style`

Reports include release metadata, review state/comments, run summaries, DUT
identity, firmware hashes, LCOV summaries, traceability rows, fault summaries,
and external-result source labels. A draft, under-review, or rejected report is
labeled with that state.

These reports are evidence review aids. They are not official assessments,
certification, or regulatory approval.

---

## How requirement coverage works

The coverage matrix is built from traceability metadata in your suite.yaml.

### Connect tests to requirements

Add `requirement_ids` to each test case:

```yaml
tests:
  - name: boot_ok
    test_case_id: TC-BOOT-001
    requirement_ids:
      - REQ-BOOT-001
      - REQ-BOOT-002
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "[BOOT] OK"
          within_ms: 3000

  - name: comm_latency
    test_case_id: TC-COMM-001
    requirement_ids:
      - REQ-COMM-001
    steps:
      - send_uart:
          node: dut
          transport: console
          data: "PING\n"
      - expect_uart:
          node: dut
          transport: console
          contains: "PONG"
          within_ms: 1000
```

`test_case_id` and `requirement_ids` are optional at the test level. You can also set `requirement_ids` at the suite level to apply to all tests in the suite.

See [Suite Configuration](suite_config.md) for the full traceability field reference.

### How the matrix is built

When you create a bundle, BenchCI parses the evidence from each selected run and writes two machine-readable views:

- `coverage-matrix.json` contains the full per-run matrix: one row per `(run_id, requirement_id, test_case_id)`.
- `coverage-matrix-latest.json` contains the latest result per `(requirement_id, test_case_id)` pair. This is the default view used by the dashboard and `/coverage` API.
- Result states are `pass`, `fail`, or `not_run`.
- If a requirement appears in multiple runs, the most recently created run wins.

`not_run` means the traceability record exists but the test did not produce a
passing or failing result, for example because it was skipped or interrupted by
an infrastructure failure. Requirements that never appear in the selected
runs' evidence are absent from the matrix; BenchCI does not infer a master
requirement list from source files that were not part of the indexed evidence.

Coverage rows include:
- `requirement_id`
- `test_case_id`
- `test_name`
- `result` and `latest_result` (pass / fail / not_run). For full rows, `result` is the per-run result; `latest_result` is kept for backward compatibility.
- `run_id` and `run_status` of the run that produced the row
- DUT identity fields and attached LCOV summary when available
- `firmware_sha256` and `suite_version` from that run
- `last_run_at` timestamp

### Coverage is bundle-scoped

The matrix reflects only the runs you included in the bundle. It is a snapshot, not a live cross-run view.

If a traced test is present but was skipped or did not reach a valid test
result, its requirement/test pair can show as `not_run`. If a requirement is
missing entirely, confirm that it was included in the submitted suite and
preserved in the selected runs' traceability evidence.

---

## How to share the bundle with your QA team

The downloaded ZIP is self-contained. You can:

- Attach it to a QA review ticket or release review checklist.
- Upload it to a shared drive or document management system.
- Open `coverage-matrix.html` in a browser — it is a standalone full per-run table with no external dependencies.
- Import `coverage-matrix.csv` into a spreadsheet for QA managers who prefer tabular review.
- Use `coverage-matrix-latest.json` when an automated consumer only needs the latest result per requirement/test pair.
- Attach `HASHES.txt` alongside the ZIP to let reviewers verify the bundle was not modified after generation.
- Preserve the approved ZIP rather than recreating a new bundle when the review
  event history is part of the release record.

The `release-summary.json` file at the top of the ZIP contains the bundle
metadata, review state/history, coverage and LCOV counts, and run list. It is
the starting point if you are building automated processing on top of bundles.

---

## Workflow example

A typical pre-release validation workflow:

```bash
# Trigger CI validation runs across your suite
benchci run --cloud --bench-id dut-stm32 \
  --suite suite.yaml --artifact build/v1.2.3.elf

# Run finishes: get the run ID from output or dashboard
benchci runs list

# Create the release bundle
benchci releases create "STM32 v1.2.3 pre-release" \
  --version "1.2.3" \
  --runs 4c1e9b7a2fd3,7b3fa1c8e921,9d2ae3f01b44

# Download the ZIP
benchci releases download bnd_a3f9c2e1b047

# Generate a human-readable review report
benchci releases report bnd_a3f9c2e1b047 \
  --template generic-qa \
  --format pdf \
  --out stm32-v1.2.3-review.pdf
```

---

## What to do when coverage is incomplete

If the matrix shows `not_run` for requirements you expected to cover:

1. **Confirm the suite ran those tests.** Check `results.json` in the per-run evidence — are the test cases present?
2. **Confirm `requirement_ids` is set on those tests.** Open the `inputs/suite.yaml` from a run's evidence ZIP to see what was actually submitted.
3. **Check if the run failed early.** If a run failed before a test executed, that test will not appear in the coverage data.
4. **Add a run that covers the missing requirement.** Create a new bundle that includes that run.

Coverage data is only as complete as the traceability metadata in your suite.yaml files.

---

## Related pages

- [Evidence Reports and Traceability](evidence_reports.md) — per-run evidence file reference
- [BenchCI and the Test Process](test_process.md) — how BenchCI maps to planning, analysis, design, implementation, execution, and completion
- [Suite Configuration](suite_config.md) — full suite.yaml reference including traceability fields
- [Cloud Mode](cloud.md) — how to run tests with BenchCI Cloud
- [CLI Reference](cli.md) — full CLI command reference

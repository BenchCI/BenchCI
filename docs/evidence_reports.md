# Evidence Reports and Traceability

Use this page when you want BenchCI runs to produce verification evidence that is easier to review, share, and attach to release or QA records.

BenchCI evidence reports are not a certification by themselves. They are structured records that help teams prove what was tested, where it ran, which firmware was used, and which requirements or risks were covered.

---

## What BenchCI produces

For local runs, BenchCI writes evidence files under `benchci-results/`. For Agent and Cloud runs, the same files are included in the downloaded artifact ZIP.

Typical files include:

```text
benchci-results/
├── results.json
├── evidence.json
├── evidence.html
├── manifest.json
├── metadata.json
├── inputs/
│   ├── bench.yaml
│   └── suite.yaml
└── nodes/
    └── dut/
        ├── flash.log
        ├── gpio.log
        └── transport-console.log
```

The exact logs depend on the bench and suite.

---

## `results.json`

`results.json` is the execution summary. It includes:

- run status
- test results
- duration
- structured failure information when a run fails
- per-test traceability fields when provided

Failed tests can include:

- failure category
- failure title
- explanation
- suggested checks
- failed step context
- related artifact paths

---

## `evidence.json`

`evidence.json` is the machine-readable evidence record.

It can include:

- run ID and status
- start/finish timestamps
- firmware filename and SHA256
- Git commit, branch, remote, and dirty-state metadata
- CI provider and CI job URL when running in CI
- bench name, bench ID, Agent ID, and bench config SHA256
- suite name and suite SHA256
- result summary
- structured failure details
- traceability IDs
- artifact file list
- artifact manifest with SHA256 hashes
- captured measurements and metrics
- environment metadata

This makes a run easier to connect to a build, a source revision, a real hardware bench, and a release or QA record.

---

## `manifest.json`

`manifest.json` is an artifact integrity manifest. It records generated files, file sizes, and SHA256 hashes.

This is useful when evidence needs to be attached to release records or shared with another team because reviewers can verify that artifacts have not changed after the run.

## Measurements and metrics

When a suite uses `measure` or `assert_metric`, BenchCI can include captured values in results and evidence.

Example values:

```text
sleep_current_a = 0.042 A
limit           = 0.150 A
result          = passed
```

This makes evidence stronger than simple pass/fail logs because it records the actual observed hardware behavior.

## `evidence.html`

`evidence.html` is a human-readable report generated from the same evidence data.

It is useful for:

- release review
- QA records
- customer acceptance notes
- internal audit trails
- debugging handoff
- attaching to Jira, Confluence, GitHub, GitLab, or issue trackers

For Cloud Mode, download the run artifacts from the CLI or dashboard and open `evidence.html` from the ZIP.

---

## Input snapshots

BenchCI stores input snapshots in:

```text
inputs/bench.yaml
inputs/suite.yaml
```

This is important because `bench.yaml` and `suite.yaml` may change later. The evidence package preserves the version that was actually used for the run.

---

## Traceability fields in `suite.yaml`

Traceability fields are optional. Use them when you want to connect a test run to requirements, test cases, risks, releases, or tags.

```yaml
version: "1"

suite:
  name: stm32-smoke-regression
  description: Basic real-hardware regression suite
  version: "1.0.0"
  release_id: "demo-fw-0.1.0"
  requirement_ids:
    - REQ-BOOT-001
  risk_ids:
    - RISK-BOOT-001
  tags:
    - smoke
    - hardware-ci

tests:
  - name: firmware boots and prints ready
    test_case_id: TC-BOOT-001
    requirement_ids:
      - REQ-BOOT-001
    risk_ids:
      - RISK-BOOT-001
    tags:
      - boot
      - uart
    steps:
      - flash:
          node: dut
      - expect_uart:
          node: dut
          transport: console
          contains: "READY"
          within_ms: 5000
```

---

## What the IDs mean

### Requirement IDs

A requirement describes what the product or firmware must do.

```text
REQ-BOOT-001: The device shall boot and print READY within 5 seconds after reset.
```

### Test case IDs

A test case describes the concrete procedure used to verify one or more requirements.

```text
TC-BOOT-001: Flash firmware, reset the DUT, and wait for READY over UART.
```

### Risk IDs

A risk describes what could go wrong and why the test matters.

```text
RISK-BOOT-001: Firmware update may leave the device stuck or silent after reset.
```

The useful chain is:

```text
Risk -> Requirement -> Test case -> BenchCI run evidence
```

---

## Recommended ID format

Keep IDs simple and stable:

```text
REQ-BOOT-001
TC-BOOT-001
RISK-BOOT-001
```

Common prefixes:

- `REQ-` for requirements
- `TC-` for test cases
- `RISK-` for risks

You do not need a requirement-management system to start. Plain IDs in `suite.yaml` are enough for early usage.

---

## Dashboard visibility

For Cloud Mode runs, the backend extracts important evidence and traceability fields from uploaded artifacts. The dashboard can show:

- firmware hash
- Git commit and branch
- CI job URL
- bench and Agent identity
- suite hash
- bench config hash
- requirement IDs
- test case IDs
- risk IDs
- whether `evidence.html` is available in artifacts

The full evidence package remains available through the artifacts ZIP.

---

## Certification and compliance wording

BenchCI evidence reports can support certification, QA, and release workflows, but BenchCI does not certify a product by itself.

Recommended wording:

```text
BenchCI helps generate traceable real-hardware verification evidence.
```

Avoid saying:

```text
BenchCI makes your product certified.
```

For regulated teams, BenchCI evidence can become part of a larger verification, validation, review, and approval process.

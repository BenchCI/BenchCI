# Evidence Reports and Traceability

Use this page when you want BenchCI runs to produce verification evidence that is easier to review, share, and attach to release or QA records.

BenchCI evidence reports are not a certification by themselves. They are structured records that help teams prove what was tested, where it ran, which firmware was used, and which requirements or risks were covered.

Release evidence bundles also include an offline-verifiable hash manifest and, when configured, an Ed25519 signature. See [Release Evidence Bundle Integrity](evidence-integrity.md) for verification instructions and the trust-anchor limitations.

---

## How BenchCI maps testing concepts to evidence

BenchCI’s traceability story is designed to support practical verification and validation conversations:

```text
Risk
  -> Requirement
      -> Test case
          -> Firmware build + source revision
              -> Physical DUT
                  -> Real hardware run
                      -> Evidence, logs, measurements, and manifests
                          -> Release review decision
```

In ISTQB-style terms:

| Testing concept | BenchCI artifact or field |
| --- | --- |
| Test object | Firmware, DUT, board revision, gateway, ECU, fixture, or hardware/software work product being tested. |
| Test basis | Requirements, risks, user stories, acceptance criteria, standards, customer expectations, or release gates referenced by IDs. |
| Test case | `tests[].test_case_id`, test name, steps, expected UART/protocol/measurement behavior, and pass/fail result. |
| Testware | `suite.yaml`, `bench.yaml`, evidence files, logs, artifact manifests, coverage attachments, release bundles, and reports. |
| Coverage | Requirement/test coverage matrices, plus separate LCOV line/function/branch code coverage when uploaded. |
| Stakeholder information | Evidence HTML/PDF, release bundle state, review comments, approval history, hashes, artifacts, and customer export records. |

BenchCI records evidence and mappings. It does not validate that an identifier exists in an external requirements system, prove that a mapping is semantically correct, certify the product, or replace the customer’s QA/regulatory process.

For the broader process view, see [BenchCI and the Test Process](test_process.md).

---

## Static-analysis and review evidence

Static analysis and real-hardware execution answer different questions. Static-analysis tools can find code, configuration, standards, and review-readiness issues without running the firmware. BenchCI runs show what a specific firmware build did on a specific physical DUT.

For release review, keep both types of evidence close together:

```text
static analysis / unit tests / code review
  + BenchCI hardware run evidence
  + release bundle review state
  = stronger stakeholder decision record
```

BenchCI does not replace MISRA checkers, cppcheck, clang-tidy, Ruff, SAST tools, or peer review. It can package their outputs as external artifacts or imported results when they support the same release decision.

See [Static Testing and Evidence Review](static_testing.md) for a testware validation checklist and release evidence review checklist.

---

## What BenchCI produces

For local runs, BenchCI writes evidence files under `benchci-results/` (if not overridden by `--results-dir`). For Agent and Cloud runs, the same files are included in the downloaded artifact ZIP.

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
└── logs/
    ├── fuzz/
    │   └── uart_protocol_fuzz-step2-uart.jsonl
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
- CI provider and CI job URL when running in CI (auto-detected for GitHub Actions, GitLab CI, Bitbucket Pipelines, CircleCI, Jenkins, Azure Pipelines, AWS CodeBuild, and any environment with `CI=true`)
- bench name, bench ID, Agent ID, and bench config SHA256
- suite name and suite SHA256
- result summary
- structured failure details
- fuzz campaign summaries, seeds, first failing cases, and fuzz log paths when fuzzing is used
- traceability IDs
- artifact file list
- artifact manifest with SHA256 hashes
- captured measurements and metrics
- environment metadata
- LCOV coverage summary when attached to a cloud run
- firmware handling mode, fetch/hash-verification/deletion timestamps, and artifact audit context
- external JUnit/CTRF source, framework, tests, logs, and artifact metadata when imported

This makes a run easier to connect to a build, a source revision, a real hardware bench, and a release or QA record.

When UART DUT self-identification is configured, each DUT record also includes its identity source, verification status, configured/observed recognized fields, and a SHA256 of the response line. The raw identity response is not copied into the structured identity block.

Experimental controlled fault steps add a `fault_injections` section with the fault type, allow-listed target, bounded parameters, restoration timestamp, recovery result/time, and observable watchdog result. These records document what BenchCI requested and observed; they do not establish precision electrical timing.

## Fuzz evidence

When a suite uses `fuzz_uart`, `fuzz_can`, or `fuzz_modbus`, evidence includes:

- campaign protocol
- seed
- test and step index
- configured iterations
- cases executed
- failure count
- first failing case
- JSONL case log path

Use this metadata to replay a failure by rerunning the same fuzz step with the recorded seed and generator settings. See [Protocol Fuzzing](fuzzing.md).

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

## CI detection and override

BenchCI records CI metadata in `evidence.json` and `evidence.html` so a test run can be traced back to the build that produced it. When a run is detected as CI, the evidence can include the CI provider and job URL in addition to the Git commit, firmware hash, bench identity, suite hash, and result summary.

This is useful when evidence is attached to release records, QA reviews, customer acceptance notes, or issue trackers because reviewers can confirm which automated job produced the hardware-test evidence.

BenchCI detects CI environments from common environment variables:

| Provider | Detection variable |
|----------|--------------------|
| GitHub Actions | `GITHUB_ACTIONS` |
| GitLab CI | `GITLAB_CI` |
| Bitbucket Pipelines | `BITBUCKET_BUILD_NUMBER` |
| CircleCI | `CIRCLECI` |
| Jenkins | `JENKINS_URL` |
| Azure Pipelines | `TF_BUILD` |
| AWS CodeBuild | `CODEBUILD_BUILD_ID` |
| Generic CI | `CI=true` |

### Overriding CI detection

Use `BENCHCI_IS_CI` when the automatic detection does not match how you want the run recorded.

Force CI detection off when you are debugging interactively inside a CI-like environment and do not want the report to look like an official CI run:

```bash
export BENCHCI_IS_CI=0
```

Force CI detection on when BenchCI runs inside a custom or unsupported CI system:

```bash
export BENCHCI_IS_CI=1
```

When `BENCHCI_IS_CI=1` and no specific provider variable is detected, BenchCI records the provider as `generic_ci`.

This override only controls how the run is classified in evidence metadata. It does not make tests pass or fail differently.

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
- configured or UART-verified DUT identity and response hash
- LCOV line/function/branch coverage
- protocol fuzzing campaign and replay summaries
- experimental fault-injection recovery summaries
- firmware handling and artifact audit history
- external-result source/framework and authenticated artifact downloads
- evidence quality warnings
- whether `evidence.html` is available in artifacts

When these artifacts are present, the dashboard can open `evidence.html`,
download `evidence.json`, and export JUnit XML or CTRF JSON directly from run
detail. The full evidence package remains available through the artifacts ZIP.

---

## Failure source and bench readiness evidence

Structured failures can include a likely source:

```text
firmware
test_logic
bench_infrastructure
agent_cloud
configuration
unknown
```

This helps reviewers understand whether a failed run is likely a product-under-test problem or a bench/automation problem.

Cloud run history can add an advisory `failure_assessment` with:

- canonical failure source
- history-suggested source
- confidence
- reasons and supporting signals

The assessment is displayed separately from the canonical failure and never
changes the recorded run result or runner-issued category/source.

Bench self-test logs can also be kept as readiness evidence:

```bash
benchci benches self-test --bench bench.yaml --open-hardware --log-dir bench-health
```

The generated `self-test-summary.json` and logs can be attached to bring-up notes, customer onboarding records, or lab troubleshooting tickets.

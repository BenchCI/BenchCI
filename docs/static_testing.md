# Static Testing and Evidence Review

Use this page when you want to catch reviewable defects before a hardware run, or when a QA/test manager asks how BenchCI fits alongside static analysis, reviews, and release sign-off.

BenchCI is primarily a real-hardware execution and evidence platform. It does not replace MISRA checkers, cppcheck, clang-tidy, Ruff, SAST tools, compiler warnings, peer review, or your organization’s QA process.

It does support a useful static-testing story:

> BenchCI can statically check and review hardware-CI testware before dynamic execution on a physical DUT, then package the resulting evidence for release review.

---

## Static testing in BenchCI terms

Static testing evaluates a work product without executing the software under test. In an embedded CI workflow, that can include source code, requirements, design notes, test cases, CI workflows, and BenchCI configuration.

BenchCI maps the idea this way:

| Static-testing concept | BenchCI equivalent |
| --- | --- |
| Work product under review | `suite.yaml`, `bench.yaml`, CI workflow files, imported static-analysis reports, release bundles |
| Static analysis | `benchci validate`, dry-run planning, external analyzers such as MISRA/cppcheck/clang-tidy/Ruff |
| Review | Human review of test intent, bench setup, traceability fields, evidence reports, and release bundles |
| Early defect detection | Catch invalid YAML, missing resources, wrong node references, unsupported artifacts, incomplete traceability, or unclear review evidence before relying on a hardware run |
| Review record | `evidence.html`, `evidence.json`, artifact manifests, release reports, review comments, approval history |

Static testing and dynamic testing complement each other. Static checks can find testware, configuration, coverage, standard-conformance, and review-readiness problems early. Dynamic BenchCI runs then show what the firmware actually did on real hardware.

---

## Static checks for BenchCI testware

Run `benchci validate` before a hardware run:

```bash
benchci validate --bench bench.yaml --suite suite.yaml
benchci validate --bench bench.yaml --suite suite.yaml --json
benchci validate --bench bench.yaml --suite suite.yaml --output validation.json
```

This checks the BenchCI testware without flashing, resetting, or communicating with the DUT. Depending on the files, it can catch:

- invalid `bench.yaml` or `suite.yaml` structure;
- suite steps that reference unknown nodes, transports, power resources, measurement resources, or buses;
- incompatible suite/bench combinations;
- missing firmware artifact configuration for flashing steps;
- unsupported or incomplete raw binary flash settings;
- unsafe or unapproved controlled fault-injection targets;
- likely GPIO, power, protocol, or measurement configuration mistakes.

Use dry-run planning when you want to review the planned execution sequence:

```bash
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf --dry-run-plan
benchci run --bench bench.yaml --suite suite.yaml --dry-run-plan --json
benchci run --bench bench.yaml --suite suite.yaml --dry-run-plan --plan-output plan.json
```

Dry-run planning is useful in pull requests because reviewers can inspect intent before the lab bench is touched.

---

## Review checklist before running on hardware

For suites that support release, customer, or QA evidence, review the testware before execution:

| Review item | Example question |
| --- | --- |
| Test basis | Are the referenced requirements, risks, acceptance criteria, or change requests clear enough for this suite? |
| Test case clarity | Do test names and `TC-*` IDs explain what is verified? |
| Requirement coverage | Are expected `REQ-*` IDs present where the result should support requirement evidence? |
| Risk coverage | Are important `RISK-*` IDs linked to the tests that reduce or monitor them? |
| Bench validity | Does `benchci validate --bench bench.yaml --suite suite.yaml` pass? |
| Execution plan | Does `--dry-run-plan` show the intended flash/reset/protocol/measurement sequence? |
| DUT identity | Is the intended board, hardware revision, serial number, or self-identification behavior documented? |
| Firmware identity | Will the run record a firmware filename, hash, and source revision? |
| Evidence quality | Will logs, measurements, artifacts, and manifests be retained for review? |
| Safety and lab risk | Are power, GPIO, fuzzing, and fault-injection steps bounded and appropriate for automation? |

BenchCI records IDs and evidence. It does not prove that a requirement exists in the customer’s ALM system, that a test semantically verifies a requirement, or that a product is certified.

---

## Static-analysis evidence from firmware CI

BenchCI does not need to run every static analyzer itself. A practical pipeline is:

```text
compile firmware
  -> run static analysis and unit tests
    -> run BenchCI real-hardware tests
      -> attach static-analysis outputs and hardware evidence to the release bundle
```

Examples of useful static-analysis artifacts:

- MISRA or coding-standard summaries;
- cppcheck, clang-tidy, or compiler-warning reports;
- Ruff, mypy, or SAST reports for support tooling;
- code-review summaries;
- unit-test JUnit XML and LCOV coverage;
- acceptance-criteria or requirements-review notes.

For Cloud Mode, attach external reports to an existing run when they support the same release decision:

```bash
benchci runs attach-results \
  --run-id <RUN_ID> \
  --artifact reports/cppcheck.xml \
  --artifact reports/misra-summary.pdf \
  --log reports/compiler-warnings.log
```

If an external test framework produced JUnit XML or CTRF JSON, import or attach it so BenchCI can show those results beside hardware evidence:

```bash
benchci runs create-external \
  --name "static-analysis-and-unit-tests" \
  --junit reports/unit-tests.xml \
  --artifact reports/lcov.info \
  --artifact reports/clang-tidy.txt
```

Use this as evidence packaging, not as a claim that BenchCI has independently verified the static-analysis findings.

---

## Release evidence review checklist

Before approving a release evidence bundle, reviewers can use this checklist:

| Review item | Example question |
| --- | --- |
| Scope | Does the bundle name/version match the release candidate being reviewed? |
| Runs included | Are the right hardware runs included, and are stale or exploratory runs excluded? |
| Requirement coverage | Are the expected requirement IDs covered, failed, or explicitly out of scope? |
| Test case coverage | Are test case IDs present and understandable? |
| Risk coverage | Are important risks linked to tests or review notes? |
| Firmware identity | Do included runs record the expected firmware hash, filename, source commit, and CI job? |
| DUT identity | Do included runs record the expected DUT, hardware revision, serial number, or identity response hash? |
| Static evidence | Are relevant static-analysis, unit-test, review, or coverage artifacts attached or referenced? |
| Dynamic evidence | Are hardware logs, measurements, failure details, and artifact manifests present? |
| Failures and skips | Are failures, skipped tests, and `not_run` rows understood and dispositioned? |
| Review decision | Is the approval/rejection comment specific enough for future readers? |
| Integrity | Is the approved ZIP/hash record preserved rather than regenerated after sign-off? |

This checklist is intentionally lightweight. Safety-critical or customer-audited teams may have additional independence, documentation, risk, or retention requirements outside BenchCI.

---

## Review roles in lightweight BenchCI language

Formal review processes often name roles such as author, reviewer, moderator, scribe, and review leader. BenchCI can support the same idea without forcing a heavyweight workflow:

| Review role | Typical BenchCI interpretation |
| --- | --- |
| Author | Firmware engineer, test author, or validation engineer who created the suite/run/bundle |
| Reviewer | QA lead, firmware lead, validation engineer, safety/security reviewer, or customer-facing technical owner |
| Moderator / review leader | Release owner who drives the evidence review to a decision |
| Scribe / recorder | BenchCI review events, comments, timestamps, bundle state, and exported reports |

For first pilots, keep this simple: use clear comments, preserve the approved bundle, and make unresolved risks visible.

---

## Related pages

- [BenchCI and the Test Process](test_process.md)
- [Test Design Techniques for Embedded Hardware](test_design_techniques.md)
- [Evidence Reports and Traceability](evidence_reports.md)
- [QA Evidence Workflow](qa_evidence_workflow.md)
- [Validation, Self-Test, and Dry-Run Planning](diagnostics.md)
- [JUnit XML and CTRF Import Guide](junit-ctrf-import-guide.md)

# BenchCI and the Test Process

Use this page when you want to explain where BenchCI fits in a mature testing workflow.

BenchCI supports the test process by turning real-hardware execution into structured, reviewable evidence. It does not define your test strategy, validate requirement correctness, replace QA judgment, or certify your product.

In practical terms, BenchCI helps embedded teams connect:

```text
Planning → Analysis → Design → Implementation → Execution → Completion
```

to:

```text
Risk → Requirement → Test Case → Firmware Build → Physical DUT → Real Run → Evidence → Release Decision
```

---

## Quick mapping

| Test process activity | How BenchCI supports it |
| --- | --- |
| Planning | Helps teams define hardware execution scope, bench availability, CI entry points, release gates, artifact expectations, and evidence needs. |
| Analysis | Captures references to the test basis: requirements, risks, acceptance criteria, customer expectations, standards, user stories, and release IDs. |
| Design | Represents test intent as named test cases with expected behavior, requirement IDs, risk IDs, tags, measurements, and pass/fail criteria. |
| Implementation | Turns test designs into executable testware: `suite.yaml`, `bench.yaml`, CI workflow files, fixtures, scripts, and artifact settings. |
| Execution | Runs tests on real hardware through local, Agent, or Cloud execution and records logs, results, firmware hash, DUT identity, metrics, and artifacts. |
| Completion | Produces evidence reports, release bundles, coverage matrices, review state, approval history, and downloadable records for stakeholder decisions. |

---

## Planning

In the planning activity, teams decide what needs to be tested, where testing will happen, how results will be reviewed, and what evidence is expected.

BenchCI can support planning by making hardware execution explicit:

- which benches or DUTs are available;
- which execution mode will be used: local, direct Agent, or Cloud Mode;
- which CI pipelines can trigger hardware runs;
- which artifacts must be retained;
- which release gates require real-hardware evidence;
- which evidence fields should be present before release review.

BenchCI does not decide your test objectives or acceptance policy. Your team still owns test strategy, risk appetite, coverage expectations, independence requirements, and sign-off authority.

---

## Analysis

In the analysis activity, teams examine the test basis and identify what should be verified.

The test basis may include:

- product requirements;
- customer requirements;
- user stories and acceptance criteria;
- known risks;
- safety, regulatory, or contractual expectations;
- release notes or change requests.

BenchCI supports analysis by letting teams carry identifiers from that test basis into executable hardware tests:

```yaml
suite:
  release_id: "fw-2.4.0-rc1"
  requirement_ids:
    - REQ-BOOT-READY
  risk_ids:
    - RISK-BOOT-LOCKUP
```

These IDs make later evidence easier to review. BenchCI records the IDs and mappings; it does not validate that the external requirement exists or that the mapping is semantically correct.

---

## Design

In the design activity, teams decide which test cases, data, expected results, and checks are needed.

In BenchCI, test design usually appears in `suite.yaml`:

```yaml
tests:
  - name: "release candidate boots to ready state"
    test_case_id: TC-BOOT-READY-001
    requirement_ids:
      - REQ-BOOT-READY
    risk_ids:
      - RISK-BOOT-LOCKUP
    steps:
      - flash:
          node: dut
      - reset:
          node: dut
      - expect_uart:
          node: dut
          transport: console
          contains: "READY"
          within_ms: 5000
```

BenchCI test design can include:

- named test cases;
- expected UART, CAN, Modbus, I2C, SPI, GPIO, power, or measurement behavior;
- requirement, risk, release, and tag metadata;
- pass/fail assertions;
- bounded robustness checks such as protocol fuzzing;
- measurement thresholds and metrics.

Test design techniques such as boundary value analysis, decision tables, and state transition testing can be represented with test names, `test_case_id` values, tags, and expected behavior. See [Test Design Techniques for Embedded Hardware](test_design_techniques.md).

Keep simple smoke suites simple. Add traceability metadata when the run should support QA, release, or customer evidence.

---

## Implementation

In the implementation activity, teams turn test designs into executable testware.

BenchCI testware can include:

- `suite.yaml` — test logic, expected behavior, and traceability metadata;
- `bench.yaml` — hardware topology, DUT identity, transports, flashing, reset, power, and measurement resources;
- CI workflow files for GitHub Actions, GitLab CI, or another CI system;
- helper scripts or device commands;
- fixture wiring and bench setup;
- artifact retention and evidence settings.

The important separation is:

```text
bench.yaml  -> describes the physical execution environment
suite.yaml  -> describes test intent
```

That separation helps teams reuse the same test intent across local execution, Agent execution, and Cloud Mode without hard-coding every hardware detail into the suite.

Before touching hardware, teams can also statically check and review BenchCI testware. `benchci validate` checks `bench.yaml` and `suite.yaml` structure and compatibility without flashing, resetting, or communicating with the DUT. Dry-run planning can show the intended execution sequence before a lab resource is used.

In ISTQB language, this is static testing of the testware. It helps catch invalid configuration, unclear traceability, wrong resource references, and review-readiness gaps before dynamic execution on real hardware. See [Static Testing and Evidence Review](static_testing.md).

---

## Execution

In the execution activity, BenchCI runs the implemented tests against real hardware.

Depending on your setup, execution can happen:

- locally on a machine connected to the DUT;
- through a BenchCI Agent connected to shared lab hardware;
- through BenchCI Cloud Mode with backend scheduling and dashboard visibility.

During execution, BenchCI can record:

- run status and timing;
- per-test pass/fail results;
- firmware filename and SHA256;
- source commit and CI job metadata;
- bench and Agent identity;
- configured or observed DUT identity;
- logs and transport output;
- measurements and metrics;
- fuzz campaign details;
- artifact manifests and hashes;
- structured failure details.

This is where BenchCI is strongest: it turns dynamic testing on physical hardware into repeatable evidence rather than an informal lab observation.

---

## Completion

In the completion activity, teams summarize results, preserve evidence, assess whether objectives were met, and provide information for stakeholders.

BenchCI supports completion with:

- `evidence.json` for machine-readable run evidence;
- `evidence.html` for human-readable run evidence;
- artifact ZIPs with logs, manifests, and input snapshots;
- release evidence bundles;
- requirement/test coverage matrices;
- review state and approval history;
- HTML/PDF release reports;
- downloadable records for QA tickets, customer reviews, or internal release checklists.

This supports stakeholder decisions such as:

- whether a release candidate has enough hardware evidence to proceed;
- which requirements were exercised;
- which tests failed or were not run;
- which firmware hash and DUT identity produced the result;
- whether additional tests or reruns are needed.

---

## Requirement traceability vs. code coverage

BenchCI distinguishes two related but different ideas:

| Topic | Question it answers |
| --- | --- |
| Requirement/test traceability | Which requirement or risk was exercised by which test case, on which run, with which firmware and DUT? |
| LCOV code coverage | Which source lines, functions, or branches were executed in an uploaded coverage report? |

Both can support confidence, but they are not interchangeable.

Requirement/test traceability helps release and QA stakeholders understand evidence against the test basis. Code coverage helps engineering teams understand executed source structure. BenchCI can show both when data is provided.

---

## Test levels in embedded BenchCI language

ISTQB-style test levels are useful because each level has different objectives. BenchCI does not force a formal level model, but teams can represent the intent with suite/test names, requirement IDs, test case IDs, risk IDs, and tags.

| Test level | Embedded interpretation | BenchCI examples |
| --- | --- | --- |
| Component testing | A low-level firmware module, driver behavior, or narrow DUT capability is checked in isolation where practical. | UART command handler smoke test, bootloader response check, low-level GPIO behavior, imported unit-test results with LCOV. |
| Component integration testing | Interactions between firmware modules, drivers, peripherals, or bench resources are checked. | Driver + peripheral checks over I2C/SPI, flash + reset + UART startup, power resource + DUT recovery. |
| System testing | The whole DUT or product behavior is checked on real hardware. | Boot-to-ready smoke suite, protocol regression against a real device, current consumption threshold, end-to-end device workflow. |
| System integration testing | The DUT is checked against other systems or external services. | CAN/Modbus/network interactions, PLC or gateway communication, lab-controller or external artifact workflow integration. |
| Acceptance testing | Evidence is produced for stakeholder review and release readiness. | Release-candidate suite, customer acceptance notes, QA review bundle, regulatory or contractual acceptance support. |

Suggested tags: `component`, `component-integration`, `system`, `system-integration`, and `acceptance`.

These tags are conventions. BenchCI records them; your team decides what each level means for your product and quality process.

---

## Test types BenchCI can support

Testing types can appear at any level. BenchCI is strongest when the type is visible in the suite name, test name, tags, and evidence.

| Test type | BenchCI interpretation |
| --- | --- |
| Functional testing | Checks required DUT behavior such as boot output, command response, protocol behavior, GPIO state, or measurement threshold. |
| Non-functional testing | Checks quality characteristics such as timing, power, reliability, robustness, security regression, or maintainability signals. |
| Black-box testing | Derives checks from requirements, expected behavior, protocols, acceptance criteria, or customer-visible behavior. |
| White-box testing | Uses implementation knowledge or uploaded code coverage such as LCOV line/function/branch summaries. |
| Confirmation testing | Reruns a previously failing hardware-visible scenario to confirm a defect fix. |
| Regression testing | Repeats known checks after changes to catch unintended side effects. |
| Maintenance testing | Tests an already-running product after firmware patches, hardware revisions, toolchain upgrades, protocol changes, migrations, or retirement activities. |

Suggested tags: `functional`, `non-functional`, `black-box`, `white-box`, `confirmation`, `regression`, and `maintenance`.

---

## Shift-left hardware validation

Shift-left testing means starting useful testing earlier, not skipping later testing.

Embedded teams already shift left with compilation, static analysis, host-side unit tests, and simulation. BenchCI extends that idea by moving selected real-hardware checks into CI:

```text
build firmware
  -> run host checks
    -> run BenchCI smoke/regression suite on real hardware
      -> preserve evidence for release review
```

Good candidates for shift-left hardware validation:

- boot and smoke tests that finish quickly;
- protocol checks that catch common regressions;
- deterministic confirmation tests for recently fixed defects;
- power/reset recovery checks that are safe to automate;
- bounded fuzz campaigns with fixed seeds;
- measurement thresholds that can run on a stable bench.

Longer exploratory, manual, destructive, calibration-sensitive, or high-risk electrical tests may still belong later in the lifecycle or in a controlled lab procedure.

---

## Regression, confirmation, and maintenance evidence

BenchCI fits three recurring SDLC activities especially well:

- **Regression testing:** run the same real-hardware suite after firmware changes and keep the evidence attached to CI or release bundles.
- **Confirmation testing:** rerun the scenario that failed before the fix, then compare the new result, firmware hash, DUT identity, and artifacts.
- **Maintenance testing:** validate firmware patches, hardware revisions, toolchain upgrades, protocol changes, migrations, and retirement activities with a reviewable evidence package.

The practical pattern is:

```yaml
suite:
  tags:
    - regression
    - system

tests:
  - name: fixed watchdog reset no longer reproduces
    test_case_id: TC-WATCHDOG-RESET-042
    requirement_ids:
      - REQ-BOOT-READY
    risk_ids:
      - RISK-BOOT-LOCKUP
    tags:
      - confirmation
      - maintenance
```

Use release bundles when the result needs to support a QA, customer, or stakeholder decision.

---

## What BenchCI does not replace

BenchCI supports the test process, but your organization still owns:

- test strategy and planning;
- requirement quality and approval;
- risk analysis;
- test case review and independence rules;
- regulatory interpretation;
- final release decisions;
- customer or certification submissions;
- quality-management records outside BenchCI.

BenchCI is best understood as a real-hardware execution and evidence platform. It helps teams produce better information for the test process; it is not a certification body or a full requirements-management system.

---

## Related pages

- [Evidence Reports and Traceability](evidence_reports.md)
- [QA Evidence Workflow](qa_evidence_workflow.md)
- [Static Testing and Evidence Review](static_testing.md)
- [Test Design Techniques for Embedded Hardware](test_design_techniques.md)
- [Suite Configuration](suite_config.md)
- [Bench Configuration](bench_config.md)
- [Dashboard](dashboard.md)

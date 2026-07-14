# Test Design Techniques for Embedded Hardware

Use this page when you want to explain how BenchCI suites can reflect deliberate test analysis and design, not just ad hoc hardware checks.

BenchCI does not choose your test technique, prove that your test design is complete, validate requirements, or certify coverage adequacy. It helps you record the chosen test intent in `suite.yaml`, execute it on real hardware, and preserve the resulting evidence.

---

## Test analysis and design in BenchCI terms

Test techniques help answer two practical questions:

```text
Analysis: What should be tested?
Design:   How should it be tested?
```

In BenchCI, those decisions usually become:

- test names and `test_case_id` values;
- requirement, risk, release, and tag metadata;
- UART, CAN, Modbus, I2C, SPI, GPIO, power, measurement, fuzzing, or artifact steps;
- expected outputs, threshold assertions, and evidence records.

Recommended lightweight tags:

| Technique family | Useful tags |
| --- | --- |
| Black-box / specification-based | `black-box`, `equivalence-partitioning`, `boundary-value`, `decision-table`, `state-transition` |
| White-box / structure-based | `white-box`, `statement-coverage`, `branch-coverage`, `lcov` |
| Experience-based | `error-guessing`, `exploratory`, `checklist-based`, `fault-attack` |
| Collaboration-based | `acceptance-criteria`, `atdd`, `bdd`, `user-story` |

Tags are conventions, not reserved schema fields. They are useful because they make test intent visible in evidence reports, dashboards, release bundles, and reviews without requiring a full test-management system.

---

## Black-box techniques

Black-box techniques design tests from the test basis: requirements, risks, user stories, acceptance criteria, protocols, standards, or customer-visible behavior. They remain useful even if the implementation changes, as long as required behavior stays the same.

### Equivalence partitioning

Equivalence partitioning divides input or state space into groups expected to be handled the same way.

Embedded examples:

- PWM duty cycle: invalid low, valid range, invalid high;
- protocol command length: too short, valid, too long;
- firmware version: older, same, newer;
- battery voltage: below operating range, normal range, above safe range.

BenchCI pattern:

```yaml
tests:
  - name: pwm duty valid representative accepted
    test_case_id: TC-PWM-EP-VALID
    tags: [black-box, equivalence-partitioning, functional]
```

BenchCI records the representative test case and evidence. Your team decides whether the partitions are correctly defined.

### Boundary value analysis

Boundary value analysis exercises the edges of ordered partitions because defects often live near minimum, maximum, and threshold values.

Embedded examples:

- voltage safety range: just below, at, and just above the boundary;
- current budget limit: just below, at, and just above the limit;
- temperature derating threshold;
- packet length limit;
- timeout threshold.

BenchCI pattern:

```yaml
tests:
  - name: voltage just below lower boundary is rejected
    test_case_id: TC-VOLT-BVA-LOW-001
    tags: [black-box, boundary-value, safety, measurement]
```

See `examples/19-boundary-value-threshold/` for a template.

### Decision table testing

Decision tables are useful when combinations of conditions produce different outcomes.

Embedded examples:

- firmware update allowed only when battery is OK, firmware is signed, and the device is idle;
- motor output enabled only when interlock, command, and diagnostic state are valid;
- gateway forwarding allowed only when source, destination, authentication, and mode rules match.

BenchCI pattern:

```yaml
tests:
  - name: update rejected when firmware is unsigned
    test_case_id: TC-UPDATE-DT-UNSIGNED
    tags: [black-box, decision-table, safety, negative-test]
```

See `examples/21-decision-table-safety-update/` for a template.

### State transition testing

State transition testing is useful when firmware behavior depends on current state and events.

Embedded examples:

- firmware update flow: idle → downloading → verifying → installing → rebooting → ready;
- bootloader/app handoff;
- pairing or provisioning flow;
- fault state and recovery flow;
- power-mode transitions.

BenchCI pattern:

```yaml
tests:
  - name: update flow follows valid transition sequence
    test_case_id: TC-UPDATE-ST-VALID
    tags: [black-box, state-transition, system, regression]
```

See `examples/20-state-transition-update-flow/` for a template.

---

## White-box techniques

White-box techniques use knowledge of implementation structure. BenchCI does not instrument code by itself, but it can attach LCOV summaries from unit tests, simulation, or external workflows and show them beside hardware evidence.

### Statement and branch coverage

Statement coverage asks which executable statements ran. Branch coverage asks which control-flow branches ran. Branch coverage is stronger because 100% branch coverage implies statement coverage, but not vice versa.

BenchCI pattern:

```text
unit tests / simulation produce LCOV
  -> benchci coverage upload coverage.info --run-id <RUN_ID>
  -> release bundle shows LCOV plus real-hardware evidence
```

Important boundary:

- LCOV code coverage is not the same as requirement/test coverage.
- Uploaded LCOV does not prove that the flashed firmware binary exactly matches the coverage source unless your process establishes that link.
- White-box coverage can miss defects of omission when a requirement was never implemented.

---

## Experience-based techniques

Experience-based techniques use tester and domain knowledge to find defects that formal techniques may miss.

### Error guessing and fault attacks

Use error guessing when engineers know where embedded systems tend to fail:

- reset during flash or update;
- brownout near a safety threshold;
- malformed or unexpected protocol input;
- noisy UART/CAN communication;
- timing-sensitive boot or sleep transitions.

BenchCI supports some of these through bounded fuzzing, power/reset steps, measurement thresholds, and experimental allow-listed fault-injection steps.

### Exploratory testing

Exploratory testing is useful when specifications are weak, time is short, or the team is learning the product. BenchCI can preserve the follow-up automated checks once exploratory work reveals repeatable scenarios.

Recommended pattern:

```text
manual/exploratory observation
  -> write a small BenchCI regression or confirmation suite
  -> preserve evidence in CI/release review
```

### Checklist-based testing

Checklist-based testing is useful for recurring hardware validation tasks that need human judgment.

Good checklist items:

- each item is separately checkable;
- each item is not already fully automated;
- the checklist captures experience about how the product fails.

Do not turn every automated assertion into a manual checklist item. Use BenchCI for repeatable execution and use checklists for review judgment.

---

## User stories, acceptance criteria, and ATDD

Collaborative techniques help avoid defects by improving the test basis before implementation.

For software/user-facing work, user stories are often described with the “3 Cs”:

- Card: the short story;
- Conversation: shared understanding of how it will be used;
- Confirmation: acceptance criteria.

For embedded firmware, acceptance criteria may appear as:

- Given/When/Then scenarios;
- rule-oriented bullet lists;
- input/output tables;
- protocol examples;
- safety or timing thresholds.

BenchCI can turn selected acceptance criteria into executable hardware evidence:

```yaml
tests:
  - name: accepted firmware update reaches ready state
    test_case_id: TC-ACCEPT-UPDATE-READY
    requirement_ids:
      - REQ-UPDATE-READY
    tags:
      - acceptance
      - atdd
      - state-transition
```

ATDD is a test-first collaboration approach. BenchCI can support it after the team has written clear acceptance criteria, but BenchCI does not decide whether those criteria are sufficient.

---

## Practical guidance

- Use black-box tags when the test comes from requirements, acceptance criteria, protocol behavior, or risk analysis.
- Use white-box tags when the test depends on implementation knowledge or uploaded code coverage.
- Use experience-based tags for exploratory follow-up, fault attacks, or known failure modes.
- Use `requirement_ids`, `test_case_id`, `risk_ids`, and `tags` when evidence should support QA or release review.
- Keep simple smoke suites simple; add technique metadata when it makes review easier.

---

## Related pages

- [BenchCI and the Test Process](test_process.md)
- [Static Testing and Evidence Review](static_testing.md)
- [Suite Configuration](suite_config.md)
- [Evidence Reports and Traceability](evidence_reports.md)
- [BenchCI Examples](examples.md)

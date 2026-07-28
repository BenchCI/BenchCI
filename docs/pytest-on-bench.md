# Run your pytest suite on a BenchCI bench

Many embedded teams already have a pytest suite that talks to hardware — over a
serial port, a debug probe, a CAN interface, or an instrument. You do not have
to rewrite those tests to get BenchCI's evidence, traceability, and release
workflow around them.

There are two ways to combine pytest and BenchCI. Pick the one that matches when your tests run.

| You want to… | Use | Bench Agent needed? |
| --- | --- | --- |
| Import results from a pytest run that already happened | `benchci runs create-external` | No |
| Run pytest **as a step on the bench**, during a BenchCI run (flash → pytest → evidence) | `run_external` step | Yes |

The first is a post-hoc import and is covered in
[External Test Bridge Workflow](external-test-bridge-workflow.md). This page
covers the second: making your pytest suite a live step in a BenchCI hardware
run, so flashing, pytest execution, and evidence collection happen in one
orchestrated run.

---

## The idea

`run_external` lets a suite trigger a bench-owner-approved command and collect
its JUnit report, logs, and artifacts into the same evidence bundle as native
BenchCI steps. pytest is just such a command — run it with `--junitxml` and
BenchCI ingests the result.

```text
BenchCI run
  ├─ flash firmware onto the DUT        (native step)
  ├─ wait for boot                      (native step)
  ├─ run your pytest suite on the bench (run_external → pytest --junitxml)
  └─ collect evidence                   (firmware hash, DUT identity,
                                         pytest results, logs, traceability)
```

Your pytest tests keep talking to the hardware exactly as they do today. BenchCI
adds firmware provenance, DUT identity, requirement traceability, and the release
bundle around them.

---

## Step 1 — a wrapper script (bench owner)

`run_external` never runs a bare interpreter. The bench owner approves a small
wrapper script, and suites may only append allow-listed arguments to it. This
keeps arbitrary code off the Agent: a suite author cannot change what actually
executes.

Put a wrapper on the Agent host, for example
`/opt/benchci/wrappers/run-pytest`:

```bash
#!/usr/bin/env bash
# Usage: run-pytest <suite-name>
# Runs an allow-listed pytest suite and writes a JUnit report to a fixed path.
set -euo pipefail

SUITE="${1:?suite name required}"
OUT_DIR="reports"
mkdir -p "$OUT_DIR" logs

# Only known suites may run — the suite author cannot pass an arbitrary path.
case "$SUITE" in
  smoke)      TARGET="tests/smoke" ;;
  regression) TARGET="tests/regression" ;;
  *) echo "unknown suite: $SUITE" >&2; exit 2 ;;
esac

# The DUT's serial port for this bench (see Step 3 for where this comes from).
python -m pytest "$TARGET" \
  --junitxml="$OUT_DIR/junit.xml" \
  2>&1 | tee "logs/pytest.log"
```

Make it executable and keep it under the bench owner's control:

```bash
chmod +x /opt/benchci/wrappers/run-pytest
```

Design the wrapper so it takes only positional, well-understood arguments. Do
not let suite arguments become pytest options like `-p` or `--rootdir`.

---

## Step 2 — bench policy (bench owner)

External execution is denied by default. The bench owner enables it and
allow-lists the wrapper in `bench.yaml`:

```yaml
safety:
  external:
    enabled: true
    targets:
      pytest_suite:
        work_root: /opt/benchci/projects/acme-fw
        output_root: /opt/benchci/projects/acme-fw/reports
        argv_prefix:
          - /opt/benchci/wrappers/run-pytest
        arg_patterns:
          - "^(smoke|regression)$"      # the only args a suite may pass
        max_timeout_ms: 900000
        lock_key: external:acme-bench
```

- `argv_prefix` is fixed by the bench owner. Suites can only append `args`; they
  cannot replace the command.
- `arg_patterns` restricts what those args may be — here, only `smoke` or
  `regression`.
- `work_root` / `output_root` bound where the command runs and where BenchCI is
  allowed to collect files from. Absolute paths, `..` traversal, and symlinks
  that escape these roots are rejected.
- `lock_key` serializes access so two runs cannot use the same bench at once.

---

## Step 3 — the suite step (test author)

```yaml
tests:
  - name: pytest smoke on hardware
    requirement_ids: [REQ-COMMS-001]
    steps:
      - flash:
          artifact: firmware.elf

      - expect_uart:
          node: dut
          transport: console
          contains: "[BOOT] OK"
          within_ms: 3000

      - run_external:
          target: pytest_suite
          args: ["smoke"]
          timeout_ms: 600000
          source: pytest
          framework: pytest
          junit: reports/junit.xml
          logs:
            - logs/pytest.log
```

BenchCI flashes the firmware, waits for boot, runs your pytest smoke suite on the
bench, and folds the pytest results — with pass/fail per test, the JUnit report,
and the log — into the run's evidence, next to the firmware SHA-256 and DUT
identity.

If any pytest test fails, the step fails, and the failing cases appear in the run
evidence with their names and messages.

---

## How your pytest fixtures learn about the bench

Your tests need to know which serial port (or CAN interface, or probe) to talk
to. Two simple patterns, both handled inside the wrapper so the suite stays
declarative:

**A configuration file the bench owner controls.** The wrapper points pytest at a
known config on the Agent host:

```bash
python -m pytest "$TARGET" --junitxml="$OUT_DIR/junit.xml" \
  --bench-config /opt/benchci/projects/acme-fw/bench.env
```

**Environment variables set by the wrapper.** The wrapper exports what your
fixtures expect before calling pytest:

```bash
export DUT_SERIAL_PORT="/dev/ttyACM0"
export DUT_BAUD="115200"
python -m pytest "$TARGET" --junitxml="$OUT_DIR/junit.xml"
```

Either way, the bench owner — not the suite author — decides how the hardware is
addressed, which keeps the security boundary intact.

---

## When to use which

- **Just want evidence and traceability around an existing pytest CI job?** Keep
  running pytest wherever you run it today and import the result with
  `benchci runs create-external --junit results.xml`. No bench, no wrapper.
- **Want flashing, boot checks, and pytest to happen together on a real bench,
  in one run, gated for release?** Use the `run_external` step as shown here.

Both paths produce the same kind of BenchCI evidence and can be combined in the
same release bundle.

---

## See also

- [HIL Orchestration](hil-orchestration.md) — the full `run_external` reference,
  including HTTP-triggered targets and Agent-local collection.
- [External Test Bridge Workflow](external-test-bridge-workflow.md) — importing
  JUnit/CTRF results without a bench.
- [Suite Configuration](suite_config.md) — native BenchCI step reference.

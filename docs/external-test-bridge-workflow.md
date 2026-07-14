# External Test Bridge Workflow

If your team already has hardware tests — a pytest suite, a Robot Framework run, a labgrid nightly, a custom test harness — you do not need to rewrite them to get structured evidence, dashboards, and release traceability from BenchCI.

Any test runner that can emit a JUnit XML or CTRF JSON file works. BenchCI ingests the results, captures DUT identity and firmware provenance, and produces the same evidence trail as a native BenchCI run.

---

## How it works

```text
Your existing test runner  →  JUnit XML / CTRF JSON
                                       ↓
                          benchci runs create-external
                                       ↓
             BenchCI run record (DUT identity, firmware SHA-256, results)
                                       ↓
                          Release bundle + sign-off workflow
```

No bench agent required. No changes to your existing tests.

---

## Step 1: Run your tests and produce a JUnit XML

Most test frameworks support JUnit XML output out of the box:

```bash
# pytest
pytest --junitxml=results.xml tests/

# Robot Framework
robot --xunit results.xml tests/

# Unity (via test runner script)
./run_tests.sh --junit results.xml

# any other runner that supports JUnit output
your-test-runner --junit results.xml
```

---

## Step 2: Create an external BenchCI run

```bash
benchci runs create-external \
  --name "hardware suite — rev-b" \
  --junit-xml results.xml \
  --framework pytest \
  --source your-test-runner \
  --artifacts artifacts/ \
  --firmware-sha256 "$(sha256sum firmware.elf | cut -d' ' -f1)" \
  --firmware-filename firmware.elf \
  --dut-hardware-revision rev-b \
  --dut-serial-number "$DUT_SERIAL" \
  --dut-asset-id "$DUT_ASSET_ID"
```

`--source` is a free-form label. Use whatever identifies your test runner: `pytest`, `labgrid`, `robot`, `unity`, `ctest`, etc.

By default, the run is created in the active workspace for the current CLI session. If a user or CI token can access multiple workspaces, pass `--workspace-id <WORKSPACE_ID>` to create the external run in a specific workspace.

This returns a `run_id`. The run is immediately in terminal state (`done` or `failed` based on your JUnit results) and has full DUT identity captured.

### Attaching coverage

If your run also produces LCOV coverage data (via gcovr, lcov, OpenCppCoverage, or similar):

```bash
benchci coverage upload coverage.info --run-id $RUN_ID
```

---

## Step 3: Attach the run to a release bundle

```bash
benchci releases create "v1.2.0-rc1" --runs $RUN_ID
```

---

## Step 4: Submit for review

Submit the bundle for review from the BenchCI dashboard. A workspace admin can then approve or reject it. The approval creates a tamper-evident hash chain entry linking your test evidence to the sign-off decision.

---

## GitHub Actions example

```yaml
jobs:
  hardware-ci:
    runs-on: [self-hosted, hardware]
    steps:
      - uses: actions/checkout@v4

      - name: Run hardware tests
        run: |
          pytest --junitxml=results.xml tests/
          mkdir -p artifacts && cp results.xml artifacts/
        continue-on-error: true

      - name: Report to BenchCI
        if: always()
        env:
          BENCHCI_TOKEN: ${{ secrets.BENCHCI_TOKEN }}
        run: |
          RUN_JSON=$(benchci runs create-external \
            --name "hw-suite ${{ github.ref_name }}" \
            --junit-xml results.xml \
            --framework pytest \
            --source pytest \
            --artifacts artifacts/ \
            --workspace-id "${{ vars.BENCHCI_WORKSPACE_ID }}" \
            --firmware-sha256 "${{ needs.build.outputs.firmware_sha256 }}" \
            --firmware-filename firmware.elf \
            --dut-hardware-revision "${{ vars.DUT_HW_REV }}" \
            --json)
          RUN_ID=$(printf '%s' "$RUN_JSON" | jq -r .run_id)
          echo "BENCHCI_RUN_ID=$RUN_ID" >> $GITHUB_ENV

      - name: Create release bundle on main
        if: github.ref == 'refs/heads/main'
        env:
          BENCHCI_TOKEN: ${{ secrets.BENCHCI_TOKEN }}
        run: |
          benchci releases create "v$(cat VERSION)" --runs $BENCHCI_RUN_ID
```

---

## Tips

- **Keep your test runner unchanged.** BenchCI only reads the JUnit XML output — it does not interact with your test runner's configuration or fixtures.
- **Multiple DUT configurations.** Run `create-external` once per DUT and add all resulting run IDs to the same release bundle for a multi-board evidence package.
- **Artifact downloads.** Local files and directories passed with `--artifact` or `--artifacts` are uploaded with SHA256 metadata and can be downloaded from the BenchCI dashboard. URL artifacts stay as external links.
- **Requirement traceability.** BenchCI reads `requirement_ids` and `test_case_id` from `<property>` elements inside a JUnit `<testcase>`. Add them to your JUnit output (via a pytest hook, a post-processing script, or your runner's property API) and BenchCI will show requirement coverage in the release bundle:

  ```xml
  <testcase name="test_boot">
    <properties>
      <property name="requirement_ids" value="REQ-BOOT,REQ-PWR"/>
      <property name="test_case_id" value="TC-001"/>
    </properties>
  </testcase>
  ```
- **Mixing with native runs.** A release bundle can contain both native BenchCI agent runs and external runs. The coverage matrix and requirement coverage view span all of them.

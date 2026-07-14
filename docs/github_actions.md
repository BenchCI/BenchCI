# GitHub Actions Integration

Run real hardware tests from a GitHub Actions workflow.

This is the recommended production flow:

```text
GitHub Actions builds firmware
        ↓
BenchCI CLI schedules a cloud run
        ↓
Cloud-connected Agent flashes and tests real hardware
        ↓
Results, measurements, evidence, and traceability return to GitHub Actions and the BenchCI dashboard
```

Use this when you want pull requests or pushes to validate firmware on real devices instead of stopping at compilation.

---
Run BenchCI hardware tests from a GitHub Actions workflow.

This guide shows the recommended GitHub Actions flow for BenchCI:

1. build firmware in GitHub Actions
2. upload or pass the firmware artifact
3. run BenchCI against real hardware
4. store BenchCI results as GitHub Actions artifacts

---

## Recommended setup

For most teams, use BenchCI Cloud Mode from GitHub Actions.

```text
GitHub Actions workflow
    ↓
BenchCI CLI
    ↓
BenchCI API
    ↓
BenchCI Agent
    ↓
real hardware bench
    ↓
results + logs + measurements
```

This avoids exposing your hardware lab directly to GitHub-hosted runners.

---

## Requirements

Before starting, make sure you have:

- a GitHub repository
- a BenchCI account and workspace
- a registered BenchCI bench
- a working `suite.yaml`
- firmware produced by your workflow
- BenchCI secrets stored in GitHub repository secrets

---

## Step 1 — Add GitHub secrets

In your GitHub repository, open:

```text
Settings → Secrets and variables → Actions → New repository secret
```

Add:

```text
BENCHCI_EMAIL=engineer@company.com
BENCHCI_PASSWORD=your-password
BENCHCI_BENCH_ID=my-cloud-bench
```

Optional stable CI machine identity:

```text
BENCHCI_MACHINE_ID=my-repo-ci
```

Most GitHub-hosted jobs should leave `BENCHCI_MACHINE_ID` unset. Set it only for a persistent runner or a non-parallel workflow lane that should always count as the same CI runner. If another active CI session already uses the same value, login is blocked until that session logs out or expires.

Authenticator MFA applies to human dashboard and CLI sign-ins. Do not add TOTP
codes or authenticator secrets to GitHub Actions; the `benchci login` command
below creates the existing short-lived CI session when it runs in CI.

---

## Step 2 — Create workflow file

Create:

```text
.github/workflows/hardware-ci.yml
```

Example workflow:

```yaml
name: Hardware CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build-firmware:
    runs-on: ubuntu-24.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install ARM toolchain
        run: |
          sudo apt-get update
          sudo apt-get install -y make gcc-arm-none-eabi binutils-arm-none-eabi

      - name: Build firmware
        run: |
          make
          mkdir -p build
          cp path/to/firmware.elf build/firmware.elf

      - name: Upload firmware artifact
        uses: actions/upload-artifact@v4
        with:
          name: firmware
          path: build/firmware.elf

  hardware-test:
    runs-on: ubuntu-24.04
    needs: build-firmware

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download firmware artifact
        uses: actions/download-artifact@v4
        with:
          name: firmware
          path: build

      - name: Install BenchCI
        run: |
          python -m pip install --upgrade pip
          pip install --upgrade benchci

      - name: Login to BenchCI
        run: |
          benchci login \
            --email "$BENCHCI_EMAIL" \
            --password "$BENCHCI_PASSWORD"
        env:
          BENCHCI_EMAIL: ${{ secrets.BENCHCI_EMAIL }}
          BENCHCI_PASSWORD: ${{ secrets.BENCHCI_PASSWORD }}

      - name: Run hardware test
        run: |
          benchci run \
            --cloud \
            --bench-id "$BENCHCI_BENCH_ID" \
            --suite suite.yaml \
            --artifact build/firmware.elf \
            --verbose
        env:
          BENCHCI_BENCH_ID: ${{ secrets.BENCHCI_BENCH_ID }}

      - name: Upload BenchCI results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: benchci-results
          path: benchci-results/
```

Update these paths for your project:

```text
path/to/firmware.elf
suite.yaml
```

### No-upload firmware option

If your team does not want firmware bytes uploaded to BenchCI Cloud, publish the firmware to a private artifact store, create a short-lived signed URL, compute SHA256 in CI, and pass both values:

```yaml
      - name: Run hardware test without firmware upload
        run: |
          FIRMWARE_SHA256="$(sha256sum build/firmware.elf | awk '{print $1}')"
          benchci run \
            --cloud \
            --bench-id "$BENCHCI_BENCH_ID" \
            --suite suite.yaml \
            --firmware-url "$SIGNED_FIRMWARE_URL" \
            --firmware-sha256 "$FIRMWARE_SHA256" \
            --verbose
        env:
          BENCHCI_BENCH_ID: ${{ secrets.BENCHCI_BENCH_ID }}
          SIGNED_FIRMWARE_URL: ${{ secrets.SIGNED_FIRMWARE_URL }}
```

### PR check annotations from BenchCI JUnit

BenchCI owns the canonical JUnit export for a cloud run. In a workflow where you have the BenchCI run ID available as `BENCHCI_RUN_ID`, export JUnit and hand it to a GitHub test-reporter action:

```yaml
      - name: Export BenchCI JUnit
        if: always()
        run: |
          benchci runs export "$BENCHCI_RUN_ID" \
            --format junit-xml \
            --output benchci-results/benchci-junit.xml

      - name: Publish BenchCI PR annotations
        if: always()
        uses: dorny/test-reporter@v1
        with:
          name: BenchCI hardware tests
          path: benchci-results/benchci-junit.xml
          reporter: java-junit
          fail-on-error: false
```

This keeps the transformation in BenchCI while GitHub owns PR check rendering and line/test annotations.

---

## Step 3 — Push and inspect the workflow

After pushing, the expected flow is:

1. GitHub builds your firmware
2. the firmware artifact is passed to the hardware-test job
3. BenchCI logs in
4. BenchCI schedules the run on the selected bench
5. the bench flashes firmware and executes the test suite
6. BenchCI downloads results into `benchci-results/` by default
7. GitHub uploads those results as workflow artifacts

---

## Results

BenchCI writes results into:

```text
benchci-results/
```

Typical contents include:

```text
results.json
evidence.json
evidence.html
manifest.json
evidence.json
evidence.html
metadata.json
inputs/bench.yaml
inputs/suite.yaml
flash.log
transport-*.log
gpio.log
power.log
```

The exact logs depend on your bench and test suite.

---

## Evidence in CI

When the workflow runs in CI, BenchCI can capture CI metadata such as provider, run ID, job ID, and job URL. Together with Git metadata and firmware hashes, this lets the evidence package connect a hardware result back to the exact CI build.

If your `suite.yaml` includes `requirement_ids`, `test_case_id`, `risk_ids`, `release_id`, or `tags`, those values are included in `results.json`, `evidence.json`, `evidence.html`, and the dashboard run detail.

Upload `benchci-results/`, or the directory passed to `--results-dir`, as a CI artifact so the evidence package is retained with the pipeline.

## Direct Agent mode

Use Direct Agent mode only when your runner can reach the hardware Agent directly.

This usually requires:

- a self-hosted GitHub Actions runner
- network access to the hardware machine
- BenchCI Agent running on the hardware machine

```text
GitHub Actions runner
    ↓
BenchCI CLI
    ↓
BenchCI Agent on lab machine
    ↓
real hardware bench
```

### Additional secrets

Add:

```text
BENCHCI_AGENT_URL=http://192.168.1.50:8080
BENCHCI_AGENT_TOKEN=secure-token
```

### Direct Agent example

```yaml
name: Hardware CI Direct Agent

on:
  push:
    branches:
      - main

jobs:
  hardware-test:
    runs-on: self-hosted

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install BenchCI
        run: |
          python -m pip install --upgrade pip
          pip install --upgrade benchci

      - name: Run hardware test through Agent
        run: |
          benchci run \
            --agent "$BENCHCI_AGENT_URL" \
            --bench bench.yaml \
            --suite suite.yaml \
            --artifact build/firmware.elf \
            --token "$BENCHCI_AGENT_TOKEN" \
            --verbose
        env:
          BENCHCI_AGENT_URL: ${{ secrets.BENCHCI_AGENT_URL }}
          BENCHCI_AGENT_TOKEN: ${{ secrets.BENCHCI_AGENT_TOKEN }}

      - name: Upload BenchCI results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: benchci-results
          path: benchci-results/
```

---

## Registered bench Agent mode

If the Agent already has the bench registered, use `--bench-id` instead of uploading `bench.yaml`.

```yaml
      - name: Run hardware test through registered Agent bench
        run: |
          benchci run \
            --agent "$BENCHCI_AGENT_URL" \
            --bench-id nucleo-uart \
            --suite suite.yaml \
            --artifact build/firmware.elf \
            --token "$BENCHCI_AGENT_TOKEN" \
            --verbose
        env:
          BENCHCI_AGENT_URL: ${{ secrets.BENCHCI_AGENT_URL }}
          BENCHCI_AGENT_TOKEN: ${{ secrets.BENCHCI_AGENT_TOKEN }}
```

This is usually better for stable shared lab infrastructure.

---

## Troubleshooting

If the workflow fails:

- confirm all GitHub secrets are defined
- confirm the bench ID is visible to your workspace
- confirm the firmware artifact path exists
- inspect `benchci-results/`
- rerun with `--verbose`

For Direct Agent mode:

- use a self-hosted runner if GitHub-hosted runners cannot reach your lab
- confirm the runner can reach the Agent URL
- confirm the Agent token matches
- confirm the hardware machine can flash and test locally first

## Recommended preflight before enabling CI

Before enabling GitHub Actions hardware runs, verify the bench on the hardware-connected machine:

```bash
benchci validate --bench bench.yaml --suite suite.yaml
benchci benches self-test --bench bench.yaml --open-hardware --log-dir bench-health
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf --dry-run-plan
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf
```

Then start the cloud Agent and confirm the bench is visible and healthy/degraded:

```bash
benchci benches list
```

Cloud scheduling intentionally avoids benches with failing or unknown health.

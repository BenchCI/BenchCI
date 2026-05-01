# GitLab CI Integration

Run real hardware tests from a GitLab pipeline.

This is the recommended production flow:

```text
GitLab CI builds firmware
        ↓
BenchCI CLI schedules a cloud run
        ↓
Cloud-connected Agent flashes and tests real hardware
        ↓
Results, evidence, and traceability return to GitLab artifacts and the BenchCI dashboard
```

Use this when you want pipeline validation on real devices instead of compile-only firmware checks.

---
Run BenchCI hardware tests from a GitLab pipeline.

This guide shows the recommended GitLab CI flow for BenchCI:

1. build firmware in GitLab CI
2. upload or reference the firmware artifact
3. run BenchCI against real hardware
4. store BenchCI results as GitLab artifacts

---

## Before using Cloud Mode

Cloud Mode requires at least one BenchCI Agent registered to your workspace and connected to a real hardware bench.

Before running CI, make sure:

- the Agent machine is connected to the DUT, debugger, UART/CAN/Modbus adapters, GPIO, relays, or other required hardware
- the Agent is registered to your BenchCI workspace
- the bench appears in the dashboard
- the bench is online/idle
- you know the bench ID to use in CI

You can check visible benches with:

benchci benches list

Use that bench ID as:

BENCHCI_BENCH_ID=my-cloud-bench

---

## Recommended setup

For most teams, use BenchCI Cloud Mode from GitLab CI.

```text
GitLab CI job
    ↓
BenchCI CLI
    ↓
BenchCI API
    ↓
BenchCI Agent
    ↓
real hardware bench
    ↓
results + logs
```

This keeps your GitLab Runner separate from the hardware lab network.

---

## Requirements

Before starting, make sure you have:

- a GitLab project
- a BenchCI account and workspace
- a registered BenchCI bench
- a working `suite.yaml`
- firmware produced by your pipeline
- BenchCI secrets stored as GitLab CI/CD variables

---

## Step 1 — Add GitLab variables

In your GitLab project, open:

```text
Settings → CI/CD → Variables
```

Add these variables:

```text
BENCHCI_EMAIL=engineer@company.com
BENCHCI_PASSWORD=your-password
BENCHCI_API_URL=https://api.benchci.dev
BENCHCI_BENCH_ID=my-cloud-bench
```

Use masked/protected variables where appropriate.

---

## Step 2 — Add .gitlab-ci.yml

Example pipeline:

```yaml
stages:
  - build
  - hardware-test

build-firmware:
  stage: build
  image: ubuntu:24.04
  script:
    - apt-get update
    - apt-get install -y make gcc-arm-none-eabi binutils-arm-none-eabi
    - make
    - mkdir -p build
    - cp path/to/firmware.elf build/firmware.elf
  artifacts:
    paths:
      - build/firmware.elf

hardware-test:
  stage: hardware-test
  image: python:3.11
  needs:
    - job: build-firmware
      artifacts: true
  script:
    - pip install --upgrade benchci
    - benchci login --email "$BENCHCI_EMAIL" --password "$BENCHCI_PASSWORD" --api-url "$BENCHCI_API_URL"
    - benchci run --cloud --bench-id "$BENCHCI_BENCH_ID" --suite suite.yaml --artifact build/firmware.elf --verbose
  artifacts:
    when: always
    paths:
      - benchci-results/
```

Update these paths for your project:

```text
path/to/firmware.elf
suite.yaml
```

---

## Step 3 — Push and inspect the pipeline

After pushing, the expected flow is:

1. GitLab builds your firmware
2. GitLab passes the firmware artifact to the hardware-test job
3. BenchCI logs in
4. BenchCI schedules the run on the selected bench
5. the bench flashes firmware and executes the test suite
6. BenchCI downloads results into `benchci-results/`
7. GitLab stores those results as job artifacts

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

Upload `benchci-results/` as a CI artifact so the evidence package is retained with the pipeline.

## Direct Agent mode

Use Direct Agent mode when your GitLab Runner can reach the hardware machine directly over the network.

```text
GitLab CI job
    ↓
BenchCI CLI
    ↓
BenchCI Agent on lab machine
    ↓
real hardware bench
```

### Agent variables

Add:

```text
BENCHCI_AGENT_URL=http://192.168.1.50:8080
BENCHCI_AGENT_TOKEN=secure-token
```

### Pipeline example

```yaml
stages:
  - hardware-test

hardware-test:
  stage: hardware-test
  image: python:3.11
  script:
    - pip install --upgrade benchci
    - benchci run --agent "$BENCHCI_AGENT_URL" --bench bench.yaml --suite suite.yaml --artifact build/firmware.elf --token "$BENCHCI_AGENT_TOKEN" --verbose
  artifacts:
    when: always
    paths:
      - benchci-results/
```

---

## Registered bench Agent mode

If the Agent already has the bench registered, use `--bench-id` instead of uploading `bench.yaml` from CI.

```yaml
hardware-test:
  stage: hardware-test
  image: python:3.11
  script:
    - pip install --upgrade benchci
    - benchci run --agent "$BENCHCI_AGENT_URL" --bench-id nucleo-uart --suite suite.yaml --artifact build/firmware.elf --token "$BENCHCI_AGENT_TOKEN" --verbose
  artifacts:
    when: always
    paths:
      - benchci-results/
```

This is usually better for stable shared lab infrastructure.

---

## Troubleshooting

If the job fails:

- confirm `BENCHCI_API_URL` is `https://api.benchci.dev`
- confirm the GitLab variables are available to the job
- confirm the bench ID is visible to your workspace
- confirm the firmware artifact path exists
- inspect `benchci-results/`
- rerun with `--verbose`

For Direct Agent mode:

- confirm the runner can reach the Agent URL
- confirm the Agent token matches
- confirm the hardware machine can flash and test locally first
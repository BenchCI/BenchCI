# GitLab CI Integration

This guide shows how to trigger BenchCI hardware tests from GitLab CI using a remote BenchCI Agent.

## Target setup

Use two machines:

- **Computer A**: hardware machine running BenchCI Agent
- **Computer B**: GitLab Runner machine running the BenchCI CLI

The DUT, debugger, UART/CAN interfaces, and Linux GPIO devices should be connected to Computer A.

## Architecture

```text
GitLab CI job
    ↓
BenchCI CLI on runner
    ↓
BenchCI Agent
    ↓
real hardware bench
    ↓
artifacts + results
```

## Requirements

Before starting, make sure you have:

- a GitLab project
- a GitLab Runner you control
- BenchCI installed on the runner machine
- BenchCI installed on the hardware machine
- a working bench configuration
- a working suite
- a firmware artifact
- network connectivity from runner to Agent

## Step 1 — Verify local execution on the hardware machine

On Computer A, first make sure BenchCI can run the hardware **locally**:

```bash
benchci run --bench bench.yaml --suite suite.yaml --artifact build/firmware.elf
```

Do not continue until this works.

## Step 2 — Start the Agent on the hardware machine

```bash
benchci agent serve --host 0.0.0.0 --port 8080
```

If you want authentication:

```bash
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve --host 0.0.0.0 --port 8080
```

## Step 3 — Verify reachability from the runner machine

From Computer B:

```bash
benchci doctor --agent http://192.168.1.50:8080
```

Or, if auth is enabled:

```bash
benchci doctor --agent http://192.168.1.50:8080 --token "$BENCHCI_AGENT_TOKEN"
```

You can also test with curl:

```bash
curl http://192.168.1.50:8080/health
```

## Step 4 — Install BenchCI on the runner machine

On Computer B:

```bash
pip install benchci
benchci --help
```

## Step 5 — Test the remote flow manually

Before writing a pipeline, test the full path from the runner machine.

### Uploaded-bench mode

```bash
benchci run \
  --agent http://192.168.1.50:8080 \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/firmware.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

### Registered-bench mode

If the Agent already has `bench_id: nucleo-uart`:

```bash
benchci run \
  --agent http://192.168.1.50:8080 \
  --bench-id nucleo-uart \
  --suite suite.yaml \
  --artifact build/firmware.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

## Step 6 — Create the GitLab variables

Add these variables in GitLab project settings:

- `BENCHCI_AGENT_URL`
- `BENCHCI_AGENT_TOKEN`

Example values:

```text
BENCHCI_AGENT_URL=http://192.168.1.50:8080
BENCHCI_AGENT_TOKEN=secure-token
```

## Step 7 — Create `.gitlab-ci.yml`

### Uploaded-bench example

```yaml
stages:
  - hardware-test

hardware-test:
  stage: hardware-test
  tags:
    - benchci
  script:
    - benchci run --agent "$BENCHCI_AGENT_URL" --bench bench.yaml --suite suite.yaml --artifact build/firmware.elf --token "$BENCHCI_AGENT_TOKEN"
  artifacts:
    when: always
    paths:
      - benchci-results/
```

### Registered-bench example

```yaml
stages:
  - hardware-test

hardware-test:
  stage: hardware-test
  tags:
    - benchci
  script:
    - benchci run --agent "$BENCHCI_AGENT_URL" --bench-id nucleo-uart --suite suite.yaml --artifact build/firmware.elf --token "$BENCHCI_AGENT_TOKEN"
  artifacts:
    when: always
    paths:
      - benchci-results/
```

## Step 8 — Push and inspect the job

Push the pipeline and inspect the logs.

Expected high-level flow:

1. GitLab checks out the repository
2. BenchCI logs in
3. BenchCI submits a run to the Agent
4. Agent queues and executes the run
5. CLI polls run status
6. CLI downloads the artifact ZIP
7. GitLab uploads `benchci-results/`

## What artifacts you get

From GitLab, you can retrieve:

- the downloaded Agent ZIP
- any local BenchCI output under `benchci-results/`

Inside the Agent ZIP you typically get:

- `results.json`
- `flash.log`
- `gpio.log`
- `transport-*.log`

## Notes

- the runner machine does not need direct hardware access for remote runs
- the hardware machine must have the required flash tools and runtime dependencies
- registered-bench mode is usually better for stable shared lab infrastructure


## Cloud Mode from GitLab CI

If you want GitLab CI to use backend scheduling instead of talking directly to a hardware Agent, use Cloud Mode.

Create masked/protected GitLab variables:

```text
BENCHCI_EMAIL=engineer@company.com
BENCHCI_PASSWORD=********
BENCHCI_API_URL=https://benchci-backend.fly.dev
BENCHCI_BENCH_ID=my-cloud-bench
```

Example:

```yaml
stages:
  - hardware-test

hardware-test:
  stage: hardware-test
  tags:
    - benchci
  script:
    - pip install --upgrade benchci
    - benchci login --email "$BENCHCI_EMAIL" --password "$BENCHCI_PASSWORD" --api-url "$BENCHCI_API_URL"
    - benchci run --cloud --bench-id "$BENCHCI_BENCH_ID" --suite suite.yaml --artifact build/firmware.elf --verbose
  artifacts:
    when: always
    paths:
      - benchci-results/
```

Cloud Mode is recommended when the runner should not connect directly to the lab network.

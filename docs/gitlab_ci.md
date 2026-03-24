# GitLab CI Integration

This guide shows how to run BenchCI from a GitLab CI pipeline using a remote BenchCI Agent connected to real hardware.

It is written for a first working setup and assumes:

- You have 2 computers
- The device under test (DUT) is physically connected to one of them
- You want GitLab CI to trigger BenchCI tests remotely

---

## Architecture

Use this setup:

- Computer A = BenchCI Agent machine
- Computer B = GitLab Runner machine

The DUT, debugger, communication interface, and any other hardware connections must be attached to Computer A.

Pipeline flow:

```
GitLab CI job
    ↓
BenchCI CLI
    ↓
BenchCI Agent
    ↓
Hardware bench
    ↓
Device under test
```

---

## What you need

Before starting, make sure you have:

- A GitLab project
- A GitLab Runner you can control
- BenchCI CLI installed on the runner machine
- BenchCI Agent installed on the hardware machine
- A working board configuration
- A working test suite
- A firmware artifact to flash
- Network connectivity between runner and agent

---

## Step 1 — Prepare the hardware machine

On Computer A:

- Connect the DUT
- Connect the debugger / flasher
- Connect communication interface
- Make sure the board powers correctly

This machine will run the BenchCI Agent and control the hardware.

---

## Step 2 — Install flashing and transport dependencies on the hardware machine

Install everything the board needs for local execution.

Examples:

- OpenOCD
- STM32CubeProgrammer
- SEGGER J-Link tools
- serial port access
- USB permissions / udev rules if needed

BenchCI Agent cannot flash or communicate with the device unless these dependencies already work on the hardware machine.

---

## Step 3 — Verify that local BenchCI execution works on the hardware machine

Before introducing GitLab CI, verify that BenchCI works locally on Computer A.

Example:

benchci run -b board.yaml -s suite.yaml -a build/firmware.elf

This must work first.

If local execution does not work on the agent machine, stop here and fix that before moving on.

---

## Step 4 — Create a minimal board configuration

Create board.yaml.

Example:

```yaml
name: test_board

flash:
  type: openocd
  interface: interface/stlink.cfg
  target: target/stm32f4x.cfg
  artifact: build/firmware.elf

reset:
  method: none

transport:
  backend: modbus_tcp
  host: 192.168.1.50
  port: 502
  timeout_ms: 1000
  default_slave: 1
```

Adjust all values to match your hardware.

Notes:

- flash.artifact should match the firmware file path used in the run command
- transport.port must be valid on the hardware machine
- reset should match your actual reset backend

---

## Step 5 — Create a minimal test suite

Create suite.yaml.

Example:

```yaml
name: smoke_test

tests:
  - name: boot_ok
    steps:
      - expect_uart:
          contains: "BOOT OK"
          within_ms: 5000
```

---

## Step 6 — Start BenchCI Agent on the hardware machine

On Computer A, start the Agent.

Example:

```
benchci agent serve --host 0.0.0.0 --port 8080
```

Agents can be set to require an access token. To enable set `BENCHCI_AGENT_TOKEN` environment variable.

Example:

```
export BENCHCI_AGENT_TOKEN=secure-token
```

Important:

- The Agent must listen on a reachable network interface
- Do not bind only to 127.0.0.1
- The GitLab runner machine must be able to reach the port

---

## Step 7 — Find the hardware machine IP address

Find the LAN IP of Computer A.

Suppose the IP is:

192.168.1.50

Then your Agent URL is:

http://192.168.1.50:8080

---

## Step 8 — Verify network connectivity from the runner machine

From Computer B, confirm that the agent is reachable.

Example:

curl http://192.168.1.50:8080

If this fails, check:

- Firewall rules
- Correct IP address
- Correct port
- Agent bind address
- Whether both machines are on the same network

Do not continue until the runner machine can reach the agent.

---

## Step 9 — Install BenchCI on the runner machine

On Computer B, install BenchCI CLI.

Then verify:

benchci --help

The GitLab CI job will run on this machine, so the CLI must already work here.

---

## Step 10 — Test remote execution manually from the runner machine

Before writing a pipeline, test the complete remote flow manually from Computer B.

Example:

benchci run \
  -b board.yaml \
  -s suite.yaml \
  -a build/firmware.elf \
  --agent http://192.168.1.50:8080

If this works, the pipeline is usually easy.

If this fails, fix it before moving to GitLab CI.

---

## Step 11 — Prepare the GitLab repository

Your GitLab repository should contain at least:

.gitlab-ci.yml
board.yaml
suite.yaml
build/firmware.elf

For a first integration test, it is acceptable to provide a ready-made firmware artifact.

Later, the pipeline should build firmware automatically before the BenchCI step.

---

## Step 12 — Install GitLab Runner on the runner machine

Install GitLab Runner on Computer B.

For the first setup, use the shell executor.

This is recommended because it is the easiest to debug.

---

## Step 13 — Register the GitLab Runner

Register the runner to your GitLab project.

You will need:

- GitLab instance URL
- Project registration token
- Executor type

Use:

```
shell
```

Recommended runner tag:

```
benchci
```

---

## Step 14 — Verify that the runner is online

In GitLab:

- Go to your project
- Open Settings
- Open CI/CD
- Check that the runner is listed and active

---

## Step 15 — Add GitLab CI variables

In GitLab project settings add variables:

```
LICENSE_KEY
BENCHCI_AGENT_URL
BENCHCI_AGENT_TOKEN
```

Example:

```
LICENSE_KEY=BCI_1234678-12345678
BENCHCI_AGENT_URL=http://192.168.1.50:8080
BENCHCI_AGENT_TOKEN=secure-token
```

---

## Step 16 — Create the pipeline file

Create `.gitlab-ci.yml` in the repository root.

Example:

```yaml
stages:
  - hardware-test

hardware-test:
  stage: hardware-test
  tags:
    - benchci
  script:
    - echo "Running BenchCI hardware tests"
    - benchci login --license-key "$LICENSE_KEY"
    - benchci run -b board.yaml -s suite.yaml -a build/firmware.elf --agent "$BENCHCI_AGENT_URL" --token "BENCHCI_AGENT_TOKEN"
  artifacts:
    when: always
    paths:
      - benchci-results/
```

---

## Step 17 — Push the pipeline configuration

```
git add .gitlab-ci.yml board.yaml suite.yaml
git commit -m "Add BenchCI GitLab CI integration"
git push
```

This should trigger a pipeline.

---

## Step 18 — Watch the pipeline logs

Expected flow:

1. GitLab checks out the repository
2. GitLab job starts on the runner machine
3. BenchCI CLI logs in
4. BenchCI CLI connects to Agent
5. Agent flashes firmware
6. Agent runs the test suite
7. Job finishes with pass or fail
8. Artifacts are uploaded

Example log output:

Running BenchCI hardware tests

[INFO] Connecting to agent http://192.168.1.50:8080
[INFO] Flashing firmware
[ OK ] Flash complete

[TEST] boot_ok
[ OK ] boot_ok

[ OK ] All tests passed
Artifacts saved to benchci-results/

---

## Step 19 — Download artifacts

BenchCI produces structured artifacts such as:

benchci-results/
├── results.json
├── transport.log
└── flash.log

These files can be downloaded from the GitLab job page.

---

## Summary

A working GitLab CI integration requires:

- BenchCI Agent running on a hardware machine
- BenchCI CLI installed on the GitLab runner
- network access from runner to agent
- board configuration
- test suite
- CI variables for token and agent URL
- shell executor runner
- artifact upload for debugging

Once these are in place, GitLab CI can trigger firmware flashing and automated validation on real hardware through BenchCI.

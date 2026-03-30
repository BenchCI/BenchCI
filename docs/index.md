# BenchCI Documentation

BenchCI is a hardware validation tool for embedded systems. It lets you define a bench in `bench.yaml`, describe tests in `suite.yaml`, and run those tests locally or through a remote BenchCI Agent.

## Installation

```bash
pip install benchci
```

Then activate your license:

```bash
benchci login
```

## What BenchCI can do

BenchCI can:

- flash firmware automatically
- validate device behavior over UART, Modbus RTU, Modbus TCP, and CAN
- control or observe GPIO through `local_gpio`, `remote_gpio`, or `mock_gpio`
- run repeatable real-hardware tests in CI
- produce structured artifacts per run

## Core model

BenchCI is built around:

- **bench**: the full execution environment
- **nodes**: named participants such as `dut`, `controller`, or `gateway`
- **transports**: UART, Modbus RTU, Modbus TCP, or CAN
- **GPIO**: logical input/output lines defined per node
- **suite steps**: declarative actions such as `flash`, `reset`, `send_uart`, `expect_uart`, `gpio_set`, and `expect_can`

## Execution modes

BenchCI supports:

- local execution on the machine connected to the hardware
- remote execution through a BenchCI Agent
- uploaded-bench remote runs
- registered-bench remote runs using a persistent `bench_id`
- split deployments where GPIO is controlled through a remote Linux machine

## Typical flow

```text
bench.yaml + suite.yaml
        ↓
   benchci run
        ↓
 local runner or Agent
        ↓
 real hardware bench
        ↓
 logs + results.json
```

## Documentation

```{toctree}
:maxdepth: 1

installation.md
quickstart.md
cli.md
board_config.md
suite_config.md
agent.md
architecture.md
gitlab_ci.md
linux_gpio.md
examples.md
```

## Where to start

For first-time setup, read:

1. `installation.md`
2. `quickstart.md`
3. `cli.md`

If you want to run remote hardware infrastructure, continue with:

4. `agent.md`
5. `gitlab_ci.md`

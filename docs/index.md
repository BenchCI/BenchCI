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

## What BenchCI can do today

BenchCI currently provides:

- declarative hardware testing using `bench.yaml` + `suite.yaml`
- automated firmware flashing
- protocol-aware validation over UART, Modbus RTU, Modbus TCP, and CAN
- GPIO automation through `local_gpio`, `remote_gpio`, or `mock_gpio`
- local execution on the hardware machine
- remote execution through a BenchCI Agent
- uploaded-bench and registered-bench execution models
- structured artifacts such as `results.json`, transport logs, flash logs, and GPIO logs
- CI-friendly hardware execution workflows

BenchCI can also be used in a backend-controlled cloud path where the CLI talks to the BenchCI backend, the backend schedules work to a managed Agent, and artifacts return to the CLI after execution.

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
- backend-controlled cloud execution with managed bench inventory and scheduling

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
bench_config.md
suite_config.md
agent.md
architecture.md
execution_flow.md
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
5. `architecture.md`
6. `execution_flow.md`
7. `gitlab_ci.md`

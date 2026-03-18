# BenchCI Documentation

BenchCI is a lightweight hardware-in-the-loop test runner for embedded systems.

It allows you to define hardware tests declaratively and run them against real devices using UART, Modbus, and GPIO.

---

## What You Can Do

With BenchCI you can:

* flash firmware automatically
* validate device behavior over UART and Modbus
* control and monitor GPIO signals
* run repeatable hardware tests in CI
* collect structured test artifacts

---

## How It Works

BenchCI uses two configuration files:

* `board.yaml` → describes your hardware setup
* `suite.yaml` → defines test logic

Execution flow:

```
benchci run → agent → hardware → results
```

---

## Documentation Structure

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
```

---

## Getting Started

Start with the quickstart guide:

👉 quickstart.md

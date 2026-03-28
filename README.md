# BenchCI

[![Documentation](https://img.shields.io/badge/docs-available-blue)](https://docs.benchci.dev)
[![Early Access](https://img.shields.io/badge/status-early--access-orange)](mailto:tech@benchci.dev)
![Hardware CI](https://img.shields.io/badge/focus-hardware%20CI-success)
![Embedded](https://img.shields.io/badge/target-embedded%20systems-blueviolet)
[![License](https://img.shields.io/badge/license-commercial-lightgrey)]()

> **Run hardware-in-the-loop tests on real embedded devices — locally or in CI.**

BenchCI is a lightweight test runner for embedded systems that lets you define hardware tests declaratively and execute them against real devices using UART, Modbus, CAN, and GPIO.

---

## ⚡ Why BenchCI?

Testing embedded firmware usually looks like this:

* Flash firmware manually
* Open serial terminal
* Send commands
* Watch logs
* Write ad-hoc scripts
* Repeat for every release

👉 This does **not scale**.

BenchCI turns this into a **repeatable, automated, CI-ready workflow**.

---

## 🧠 What BenchCI Does

BenchCI connects your CI pipeline directly to real hardware and allows you to:

* Flash firmware automatically (OpenOCD, CubeProgrammer, J-Link, esptool)
* Interact with devices over UART, Modbus RTU/TCP, and CAN
* Control and monitor GPIO (local or remote)
* Validate behavior with structured test steps
* Run tests on **remote hardware benches via Agent**
* Generate reproducible test artifacts

---

## 🏗️ How It Works

```
CI Pipeline / Developer
        │
        ▼
   benchci run
        │
        ▼
   BenchCI Agent
        │
        ▼
   Real Hardware Bench
        │
        ▼
   DUT / PLC / ECU
```

BenchCI separates:

* test execution (CLI / CI runner)
* hardware access (Agent + bench machine)

This allows:

* remote labs
* shared hardware
* scalable test infrastructure

---

## 📄 Configuration Model

BenchCI uses two files:

### bench.yaml

Defines your hardware:

* nodes (DUT, helper boards, PLCs, etc.)
* transports (UART, Modbus, CAN)
* flashing configuration
* GPIO control (local or remote)

### suite.yaml

Defines your tests:

* test cases
* step-by-step actions
* expected behavior

---

## 🚀 Example (30 seconds)

### suite.yaml

```
version: "1"

suite:
  name: "firmware-tests"

tests:
  - name: boot_ok
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "[BOOT] OK"
          within_ms: 3000

  - name: ping
    steps:
      - send_uart:
          node: dut
          transport: console
          data: "PING\n"
      - expect_uart:
          node: dut
          transport: console
          contains: "PONG"
          within_ms: 1000
```

Run:

```
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

BenchCI will:

* flash firmware
* reset device
* execute tests
* validate responses
* store artifacts

---

## 🔌 Supported Interfaces

BenchCI is designed for real hardware interaction:

### Communication

* UART
* Modbus RTU
* Modbus TCP
* CAN

### Hardware Control

* Linux GPIO
* Remote GPIO (via Agent)
* Mock GPIO (for development)

### Flashing Backends

* OpenOCD
* STM32CubeProgrammer
* SEGGER J-Link
* esptool (ESP32)

---

## 🧪 Example Scenarios

BenchCI includes realistic examples:

```
examples/
├── device_boot_validation/
├── local_gpio_reset_and_ready/
├── remote_gpio_power_cycle/
├── modbus_rtu_plc_validation/
├── modbus_tcp_gateway_validation/
├── can_ecu_handshake/
├── multi_node_system_smoke/
```

These demonstrate:

* firmware validation
* industrial protocol testing
* remote lab setups
* multi-device orchestration

---

## 📦 Output Artifacts

Each run produces structured outputs:

```
benchci-results/
├── results.json
├── transport.log
├── flash.log
├── gpio.log
```

Perfect for:

* CI pipelines
* debugging
* traceability

---

## 🧰 CLI Workflow

BenchCI provides built-in tools:

* benchci doctor → check environment
* benchci validate → validate configs
* benchci login → authenticate
* benchci run → execute tests

---

## 🔄 CI Integration

BenchCI is built for automation:

* GitLab CI support (example included)
* Works with GitHub Actions, Jenkins, etc.
* Agent-based execution for remote hardware

---

## 📚 Documentation

https://docs.benchci.dev

Key topics:

* Quickstart
* Installation
* Bench configuration
* Suite definition
* Agent setup
* CI integration

---

## 📌 Repository Contents

This repository contains:

* documentation
* configuration examples
* CI examples
* helper tools

BenchCI core source code is maintained in a private repository.

---

## 💼 License

BenchCI is a commercial product.

To request access:

[tech@benchci.dev](mailto:tech@benchci.dev)

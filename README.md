# BenchCI

[![Documentation](https://img.shields.io/badge/docs-available-blue)](https://docs.benchci.dev)
[![PyPI](https://img.shields.io/pypi/v/benchci)](https://pypi.org/project/benchci/)
[![Early Access](https://img.shields.io/badge/status-early--access-orange)](mailto:tech@benchci.dev)
![Hardware CI](https://img.shields.io/badge/focus-hardware%20CI-success)
![Embedded](https://img.shields.io/badge/target-embedded%20systems-blueviolet)
[![License](https://img.shields.io/badge/license-commercial-lightgrey)]()

> **Continuous Integration for Embedded Hardware**
>
> Flash firmware, run automated tests on real devices, and validate embedded systems in CI — using simple YAML configs.

---

## 🚀 Quickstart (30 seconds)

```bash
pip install benchci
benchci login
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

Create or access your BenchCI workspace from the dashboard:

```text
https://app.benchci.dev
```

👉 That’s it — BenchCI will:
- flash firmware  
- execute tests on real hardware  
- validate behavior  
- generate structured artifacts  

---

## ⚡ Why BenchCI?

Testing embedded firmware usually looks like this:

- flash firmware manually  
- open serial terminal  
- send commands  
- watch logs  
- write ad-hoc scripts  
- repeat for every release  

👉 This is **manual, fragile, and not CI-friendly**

---

### BenchCI makes hardware testing:

- ✅ declarative  
- ✅ repeatable  
- ✅ CI-ready  
- ✅ scalable across teams  

---

## 🧠 Mental Model

BenchCI separates **hardware** and **test logic**:

- `bench.yaml` → your hardware setup  
- `suite.yaml` → your tests  

```text
bench.yaml + suite.yaml
        ↓
   benchci run
        ↓
   real hardware execution
        ↓
   results + logs
```

---

## 🏗️ How It Works

```text
CI Pipeline / Developer
        │
        ▼
   benchci run
        │
        ▼
   Local Runner / Agent / Cloud Backend
        │
        ▼
   Real Hardware Bench
        │
        ▼
   DUT / PLC / ECU
```

BenchCI separates:

- execution (CLI / CI)
- hardware access (local runner or Agent)
- workspace visibility (Dashboard)
- scheduling and access control (Cloud backend)

This enables:

- remote labs  
- shared benches  
- private customer benches  
- scalable hardware testing  

---

## 🧠 What BenchCI Does

BenchCI connects your CI pipeline directly to real hardware and allows you to:

- flash firmware automatically (OpenOCD, CubeProgrammer, J-Link, esptool)  
- interact with devices over UART, Modbus RTU/TCP, and CAN  
- control and monitor GPIO (local or remote)  
- control supported relay-backed power resources  
- validate behavior with structured test steps  
- run tests locally, through a customer-managed Agent, or through BenchCI Cloud  
- generate reproducible artifacts  

---

## 📄 Configuration Model

BenchCI uses two files:

### `bench.yaml`

Defines your hardware:

- nodes (DUT, controllers, PLCs, etc.)  
- transports (UART, Modbus, CAN)  
- flashing configuration  
- GPIO control  
- optional bench-level resources such as relay-backed power control  

### `suite.yaml`

Defines your tests:

- test cases  
- step-by-step actions  
- expected behavior  

---

## 🚀 Example

### `suite.yaml`

```yaml
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

```bash
benchci run -b bench.yaml -s suite.yaml -a build/fw.elf
```

---

## 🔌 Supported Interfaces

### Communication

- UART  
- Modbus RTU  
- Modbus TCP  
- CAN  

### Hardware Control

- Linux GPIO  
- Remote GPIO (via Agent)  
- Mock GPIO  
- relay-backed power workflows  

### Flashing Backends

- OpenOCD  
- STM32CubeProgrammer  
- SEGGER J-Link  
- esptool (ESP32)  

---

## 🧪 Example Scenarios

```text
examples/
├── device_boot_validation/
├── local_gpio_reset_and_ready/
├── remote_gpio_power_cycle/
├── modbus_rtu_plc_validation/
├── modbus_tcp_gateway_validation/
├── can_ecu_handshake/
├── multi_node_system_smoke/
```

---

## 📦 Output Artifacts

BenchCI generates structured outputs:

```text
benchci-results/
└── <timestamp>/
    ├── results.json
    └── nodes/
        └── dut/
            ├── flash.log
            ├── gpio.log
            └── transport-console.log
```

Perfect for:

- CI pipelines  
- debugging  
- traceability  

---

## 🧰 CLI Workflow

- `benchci login` → authenticate with your BenchCI account/workspace  
- `benchci whoami` → show current user and active workspace  
- `benchci doctor` → check environment  
- `benchci validate` → validate configs  
- `benchci run` → execute tests  
- `benchci benches list` → list Cloud Mode benches  
- `benchci runs list` → inspect Cloud Mode runs  

---

## 🔄 CI Integration

BenchCI is designed for automation:

- GitLab CI (example included)  
- GitHub Actions / Jenkins  
- direct Agent execution  
- Cloud Mode through the backend scheduler  

---

## 🌐 Dashboard

Use the dashboard to view workspace health, benches, runs, events, failures, and artifacts:

```text
https://app.benchci.dev
```

---

## 📚 Documentation

👉 https://docs.benchci.dev

Includes:

- quickstart  
- installation  
- configuration guides  
- agent setup  
- CI integration  
- Cloud Mode  

---

## 📌 Repository Contents

This repository contains:

- documentation  
- configuration examples  
- CI examples  
- helper tools  

BenchCI core source code is maintained in a private repository.

---

## 💼 License and Access

BenchCI is a commercial product.

Current onboarding uses BenchCI accounts and workspaces. Early access and production use are activated manually by the BenchCI team, with monthly invoicing for paid customers.

For evaluation, pilot access, or pricing:

📧 tech@benchci.dev

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

- execution (CLI / CI)
- hardware access (Agent)

This enables:

- remote labs  
- shared benches  
- scalable hardware testing  

---

## 🧠 What BenchCI Does

BenchCI connects your CI pipeline directly to real hardware and allows you to:

- flash firmware automatically (OpenOCD, CubeProgrammer, J-Link, esptool)  
- interact with devices over UART, Modbus RTU/TCP, and CAN  
- control and monitor GPIO (local or remote)  
- validate behavior with structured test steps  
- run tests on **remote hardware via Agent**  
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

### Flashing Backends

- OpenOCD  
- STM32CubeProgrammer  
- SEGGER J-Link  
- esptool (ESP32)  

---

## 🧪 Example Scenarios

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

---

## 📦 Output Artifacts

BenchCI generates structured outputs:

```
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

- `benchci doctor` → check environment  
- `benchci validate` → validate configs  
- `benchci login` → authenticate  
- `benchci run` → execute tests  

---

## 🔄 CI Integration

BenchCI is designed for automation:

- GitLab CI (example included)  
- GitHub Actions / Jenkins  
- remote execution via Agent  

---

## 📚 Documentation

👉 https://docs.benchci.dev

Includes:

- quickstart  
- installation  
- configuration guides  
- agent setup  
- CI integration  

---

## 📌 Repository Contents

This repository contains:

- documentation  
- configuration examples  
- CI examples  
- helper tools  

BenchCI core source code is maintained in a private repository.

---

## 💼 License

BenchCI is a commercial product.

A valid license key is required to run commands.

For access:

📧 tech@benchci.dev

# BenchCI

[![Documentation](https://img.shields.io/badge/docs-available-blue)](https://docs.benchci.dev)
[![Early Access](https://img.shields.io/badge/status-early--access-orange)](mailto:tech@benchci.dev)
![Hardware CI](https://img.shields.io/badge/focus-hardware%20CI-success)
![Embedded](https://img.shields.io/badge/target-embedded%20systems-blueviolet)
[![License](https://img.shields.io/badge/license-commercial-lightgrey)]()

> **Run hardware-in-the-loop tests on real embedded devices — locally or in CI.**

BenchCI is a lightweight test runner for embedded systems that lets you define hardware tests declaratively and execute them against real devices using UART, Modbus, and GPIO.

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

* Flash firmware automatically
* Interact with devices over UART, Modbus RTU/TCP
* Control and monitor GPIO lines
* Validate behavior with structured test steps
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
   Hardware Device
```

---

## 🧰 CLI Workflow

BenchCI provides built-in tools to help you validate your setup:

- `benchci doctor` — check system dependencies  
- `benchci validate` — validate configuration files  
- `benchci login` — authenticate with BenchCI services  

These commands help ensure reliable execution before running tests.

---

## 🚀 Example (30 seconds)

Define your test suite:

```yaml
name: firmware_tests

tests:

  - name: boot_ok
    steps:
      - expect_uart:
          contains: "[BOOT] OK"
          within_ms: 3000

  - name: ping
    steps:
      - send_uart: "PING\n"
      - expect_uart:
          contains: "PONG"
          within_ms: 1000
```

Run it:

```
benchci run -b board.yaml -s suite.yaml -a build/fw.elf
```

BenchCI will:

* flash firmware
* reset the device
* execute tests
* validate responses
* store logs and results

---

## 🔌 Supported Interfaces

BenchCI is designed for real hardware interaction:

* UART communication
* Modbus RTU
* Modbus TCP
* Linux GPIO (input, output, edge detection)

---

## 📦 Output Artifacts

Each run produces structured results:

```
benchci-results/
├── transport.log
├── flash.log
├── gpio.log
└── results.json
```

Perfect for CI pipelines and debugging.

---

## 🔄 CI Integration

BenchCI is built for automation:

* GitLab CI support (example included)
* Works with any CI runner connected to hardware
* Agent-based execution for remote benches

See: `examples/ci/gitlab`

---

## 📚 Documentation

Full documentation:

👉 https://docs.benchci.dev

Key topics:

* Quickstart
* Installation
* Board configuration
* Test suite definition
* CI integration
* Architecture

---

## 📌 Repository Contents

This repository contains:

* documentation
* configuration examples
* CI integration examples
* helper tools

BenchCI source code is maintained in a private repository.

---

## 💼 License

BenchCI is a commercial product.

To request access:

📧 [tech@benchci.dev](mailto:tech@benchci.dev)

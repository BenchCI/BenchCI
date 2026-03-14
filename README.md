# BenchCI

[![Documentation](https://img.shields.io/badge/docs-available-blue)](docs/)
[![Early Access](https://img.shields.io/badge/status-early--access-orange)](mailto:tech@benchci.dev)
[![Hardware CI](https://img.shields.io/badge/focus-hardware%20CI-success)]()
![Hardware Testing](https://img.shields.io/badge/testing-hardware--in--loop-purple)
![Embedded](https://img.shields.io/badge/target-embedded%20systems-blueviolet)
[![License](https://img.shields.io/badge/license-commercial-lightgrey)]()

[Documentation](https://docs.benchci.dev)

[Website](https://benchci.dev)

Continuous Integration for Embedded Hardware

BenchCI is a tool for validating firmware behavior on **real hardware devices**.

It enables firmware teams to flash firmware, execute automated test suites, and verify device responses through communication transports such as UART and industrial protocols.

---

## Repository Purpose

This repository contains:

- documentation
- configuration examples
- CI integration examples
- helper tools

The BenchCI **source code is maintained in a private repository**.

BenchCI CLI binaries are distributed to licensed users.

---

## Why BenchCI?

Embedded firmware testing often requires:

- manually flashing devices
- interacting with serial terminals
- writing custom scripts
- manually verifying behavior

BenchCI automates this workflow and integrates it with CI pipelines.

Typical architecture:

```
CI Pipeline
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

BenchCI provides:

- automated firmware flashing
- repeatable hardware tests
- device communication validation
- structured artifacts
- CI integration

---

## Example Test Suite

Example `suite.yaml`

```yaml
name: uart_demo

tests:

  - name: boot_ok
    steps:
      - expect_uart:
          contains: "[BOOT] OK"
          within_ms: 3000

  - name: ping_test
    steps:
      - send_uart: "PING\n"
      - expect_uart:
          contains: "PONG"
          within_ms: 1000
```

Run tests:

```
benchci run -b board.yaml -s suite.yaml -a build/fw.elf
```

BenchCI will:

1. flash firmware
2. reset the device
3. execute the test suite
4. validate responses

---

## Documentation

Available in `docs/`

- quickstart.md
- installation.md
- board_config.md
- suite_config.md
- agent.md
- gitlab_ci.md
- architecture.md

---

## License

BenchCI is a commercial tool.

Usage requires a valid BenchCI license.

Contact:

tech@benchci.dev

# Changelog

Install the latest with `pip install --upgrade benchci`.

## 2.0.0 — initial public release

BenchCI 2.0.0 is the first generally available release: hardware CI and test evidence for
embedded teams, aligned across the CLI, embedded Agent API, documentation, and generated
evidence on a single version.

### Execution

- Local, direct-agent, and cloud run modes. Local and direct-agent runs are free and
  require no account.
- Firmware flashing via ST-Link/STM32CubeProgrammer, J-Link, OpenOCD, and esptool.
- Transports: UART, Modbus RTU/TCP, classic CAN and CAN FD (SocketCAN), I2C, SPI,
  Linux GPIO.
- Power resources (GPIO, HTTP, and serial relays) and measurement resources (SCPI and
  serial sensors) with threshold assertions.
- Bounded protocol fuzzing for UART, CAN, and Modbus; controlled fault injection
  (experimental) with allow-listed glitch steps and recovery oracles.
- `run_external`: trigger existing HIL rigs and simulators via bench-owner-approved
  commands or HTTP APIs, collecting their reports and artifacts into normal evidence.

### Evidence and release workflows (cloud)

- Every run produces structured evidence: firmware SHA256, git metadata, bench and DUT
  identity, measurements, logs, and hash-linked artifacts.
- Requirements traceability from suite definitions through runs into release coverage.
- Release bundles with review states, role-based sign-off, and immutable bundled evidence.
- Report downloads: generic QA, IEC 62304-style, and ISO 26262-style templates (review
  aids — they do not imply certification).
- External test import (JUnit XML / CTRF) and canonical exports; LCOV coverage
  correlation.
- Per-workspace firmware handling policies, including a no-upload mode where firmware
  never touches BenchCI servers.
- Bench reliability history, flaky-test detection, and cross-bench comparison.
- Verified DUT identity via optional UART self-identification.

### Platform

- Cloud scheduling across shared benches with workspace roles and access control.
- Authenticator (TOTP) MFA with recovery codes.
- Run-failure and release-approval email notifications.
- 30-day Team-feature trial for new workspaces; plans and free local mode published at
  https://benchci.dev/#pricing.

Release notes for future versions will appear here and at https://docs.benchci.dev.

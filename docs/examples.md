# BenchCI Examples

Use these examples as starting templates for real embedded workflows such as boot validation, GPIO reset, Modbus, CAN, ESP32, J-Link, remote GPIO, power resources, measurement resources, and multi-node testing.

---

This page contains **realistic example scenarios** showing how to use BenchCI in different setups.

Each example folder includes:

- `bench.yaml` → hardware configuration
- `suite.yaml` → test logic

Some examples are intentionally simple. Others show optional traceability fields used by Evidence Reports, such as requirement IDs, test case IDs, risk IDs, release IDs, and tags.

---

## Start here

If you are new to BenchCI, begin with one of the simple communication examples:

- `examples/02-modbus-rtu-plc-simple/`
- `examples/06-multi-node-uart-simple/`
- `examples/08-can-ecu-handshake-simple/`

If you want to see Evidence Reports and traceability metadata, start with:

- `examples/01-esp32-esptool-uart-traceable/`
- `examples/09-stm32wl-boot-validation-traceable/`

If you want to try the newer resource model, start with:

- `examples/10-generic-serial-power-relay/`
- `examples/11-http-power-relay/`
- `examples/12-mock-power-control/`
- `examples/13-http-measurement/`
- `examples/14-http-measurement-mock/`

These examples are templates. You must adapt ports, IP addresses, GPIO lines, firmware paths, expected responses, relay commands, measurement URLs, and flashing tool settings for your hardware.

---

## Example difficulty levels

Not every example needs traceability metadata. Public examples are intentionally mixed:

- **Simple examples** teach the basic BenchCI model with minimal YAML.
- **Moderate examples** include more realistic hardware resources, flashing, power, measurement, or reset flows.
- **Traceability examples** show requirement IDs, test case IDs, risk IDs, release IDs, and tags for Evidence Reports.
- **Resource examples** show the newer BenchCI resource model where `bench.yaml` hides hardware/vendor details and `suite.yaml` stays focused on test intent.

Start simple, then add traceability, power resources, and measurement resources when a run should support QA, release, or compliance-style evidence.

---

## Current public example set

```text
examples/
├── 01-esp32-esptool-uart-traceable/
│   ├── bench.yaml
│   └── suite.yaml
├── 02-modbus-rtu-plc-simple/
│   ├── bench.yaml
│   └── suite.yaml
├── 03-modbus-tcp-gateway-traceable/
│   ├── bench.yaml
│   └── suite.yaml
├── 04-gateway-jlink-provisioning-moderate/
│   ├── bench.yaml
│   └── suite.yaml
├── 05-local-gpio-reset-ready-advanced/
│   ├── bench.yaml
│   └── suite.yaml
├── 06-multi-node-uart-simple/
│   ├── bench.yaml
│   └── suite.yaml
├── 07-remote-gpio-power-cycle-moderate/
│   ├── bench.yaml
│   └── suite.yaml
├── 08-can-ecu-handshake-simple/
│   ├── bench.yaml
│   └── suite.yaml
├── 09-stm32wl-boot-validation-traceable/
│   ├── bench.yaml
│   └── suite.yaml
├── 10-generic-serial-power-relay/
│   ├── bench.yaml
│   └── suite.yaml
├── 11-http-power-relay/
│   ├── bench.yaml
│   └── suite.yaml
├── 12-mock-power-control/
│   ├── bench.yaml
│   └── suite.yaml
├── 13-http-measurement/
│   ├── bench.yaml
│   └── suite.yaml
└── 14-http-measurement-mock/
    ├── bench.yaml
    └── suite.yaml
```

---

## Example scenarios

### 1. ESP32 esptool UART Traceable

**Folder:** `examples/01-esp32-esptool-uart-traceable/`

#### Use case

Flash an ESP32 firmware image with `esptool`, then validate boot output over UART.

#### Covers

- `esptool` flashing
- UART transport
- `flash`
- `expect_uart`
- Evidence Report traceability fields

#### Traceability level

Traceable.

This example is useful for showing:

- `requirement_ids`
- `test_case_id`
- `risk_ids`
- `release_id`
- tags
- firmware/source evidence

#### When to use

- ESP32 / ESP-IDF workflows
- IoT firmware smoke tests
- demos showing Evidence Reports

---

### 2. Modbus RTU PLC Simple

**Folder:** `examples/02-modbus-rtu-plc-simple/`

#### Use case

Validate a PLC or RS-485 device using simple Modbus RTU operations.

#### Covers

- Modbus RTU transport
- `modbus_read_holding_registers`
- `modbus_write_single_register`
- simple suite structure

#### Traceability level

Simple.

This example intentionally avoids requirement/risk/test-case metadata so new users can focus on Modbus basics.

#### When to use

- industrial devices
- RS-485 bring-up
- Modbus smoke tests
- first-time BenchCI users

---

### 3. Modbus TCP Gateway Traceable

**Folder:** `examples/03-modbus-tcp-gateway-traceable/`

#### Use case

Validate an Ethernet-connected industrial gateway over Modbus TCP.

#### Covers

- Modbus TCP transport
- IP-based device access
- register validation
- Evidence Report traceability fields

#### Traceability level

Traceable.

This example demonstrates how networked device tests can be connected to requirements, risks, and release evidence.

#### When to use

- gateways
- PLC-over-Ethernet validation
- QA/release evidence for field communication

---

### 4. Gateway J-Link Provisioning Moderate

**Folder:** `examples/04-gateway-jlink-provisioning-moderate/`

#### Use case

Provision or flash a gateway device using SEGGER J-Link, then verify basic startup behavior.

#### Covers

- `jlink` flash backend
- UART validation
- moderate production-style flow

#### Traceability level

Moderate.

This example is more realistic than a minimal smoke test but does not need to show every Evidence Report field.

#### When to use

- production flashing
- SEGGER-based lab setups
- gateway firmware validation

---

### 5. Local GPIO Reset Ready Advanced

**Folder:** `examples/05-local-gpio-reset-ready-advanced/`

#### Use case

Control reset lines and observe ready/interrupt signals using Linux GPIO on the same hardware-connected machine.

#### Covers

- `local_gpio`
- GPIO output control
- GPIO input expectations
- `gpio_set`
- `gpio_expect`
- `gpio_wait_edge`
- advanced reset/ready sequencing
- Evidence Report traceability fields

#### Traceability level

Advanced / traceable.

This example is useful for showing how hardware control signals can become part of release evidence.

#### When to use

- hardware bring-up
- boards without reliable debugger reset
- reset/ready/interrupt validation
- Raspberry Pi based benches

---

### 6. Multi-Node UART Simple

**Folder:** `examples/06-multi-node-uart-simple/`

#### Use case

Coordinate two UART-connected nodes in a simple system-level test.

#### Covers

- multiple nodes
- multiple UART transports
- cross-device interaction
- simple suite structure

#### Traceability level

Simple.

This example intentionally keeps traceability metadata out so users can focus on the multi-node model.

#### When to use

- DUT + controller setups
- board-to-board smoke tests
- simple system-level validation

---

### 7. Remote GPIO Power Cycle Moderate

**Folder:** `examples/07-remote-gpio-power-cycle-moderate/`

#### Use case

Control reset, power, or ready signals through a remote GPIO service rather than local `/dev/gpiochipX` access.

#### Covers

- `remote_gpio`
- split deployments
- remote GPIO host/port configuration
- token-based remote GPIO access
- power/reset style workflows

#### Traceability level

Moderate.

This example focuses on the distributed hardware control pattern.

#### Important note

A real `remote_gpio` example should include remote connection fields such as:

```yaml
backend: remote_gpio
host: 192.168.1.60
port: 8090
token_env: BENCHCI_REMOTE_GPIO_TOKEN
```

A `local_gpio` example does **not** need an IP address because it runs on the same Linux machine as `/dev/gpiochipX`.

#### When to use

- CI runner is not the hardware GPIO machine
- remote labs
- shared hardware infrastructure
- Raspberry Pi GPIO service controlling another bench

---

### 8. CAN ECU Handshake Simple

**Folder:** `examples/08-can-ecu-handshake-simple/`

#### Use case

Validate request/response behavior on a CAN bus.

#### Covers

- CAN transport
- SocketCAN interface
- `send_can`
- `expect_can`
- simple ECU handshake

#### Traceability level

Simple.

This example avoids traceability metadata so users can focus on CAN setup and frame validation.

#### When to use

- automotive ECUs
- CAN-connected embedded devices
- bus-level smoke tests

---

### 9. STM32WL Boot Validation Traceable

**Folder:** `examples/09-stm32wl-boot-validation-traceable/`

#### Use case

Flash an STM32WL target and validate that the firmware boots and prints expected UART output.

#### Covers

- OpenOCD flashing
- ST-Link / SWD style workflow
- UART boot validation
- Evidence Report traceability fields

#### Traceability level

Traceable.

This is a good example for showing how a standard firmware boot test can become structured release evidence.

#### When to use

- STM32 / NUCLEO validation
- real-hardware CI demos
- QA/release smoke tests
- Evidence Report demos

---

### 10. Generic Serial Power Relay

**Folder:** `examples/10-generic-serial-power-relay/`

#### Use case

Control DUT power through a serial relay board using user-provided ON/OFF command bytes.

#### Covers

- `resources.dut_power`
- `type: usb_relay_serial`
- `vendor: generic`
- `model: command_map`
- `power_set`
- `power_cycle`
- UART boot validation after power restore

#### Traceability level

Moderate.

This example demonstrates the preferred Power v2 philosophy: the suite says `power_cycle`, while `bench.yaml` contains the vendor-specific serial commands.

#### When to use

- LCUS-style serial relay boards
- low-cost USB relay modules
- internal relay controllers with serial command protocols
- teams that want to add relay support without changing BenchCI code

#### Important note

Generic serial command-map relays may not support reliable state readback. Use `power_expect` only when your relay has a supported query/readback behavior.

---

### 11. HTTP Power Relay

**Folder:** `examples/11-http-power-relay/`

#### Use case

Control DUT power through an HTTP-accessible relay, smart PDU, LAN relay, or internal lab controller.

#### Covers

- `resources.dut_power`
- `type: http_relay`
- HTTP ON/OFF URLs
- optional HTTP state readback
- `power_set`
- `power_cycle`
- `power_expect` when readback is configured

#### Traceability level

Moderate.

This example is useful for lab setups where a relay or power controller exposes an HTTP API.

#### When to use

- LAN relay boards
- smart lab controllers
- simple internal REST services
- shared benches where power hardware is controlled over the network

---

### 12. Mock Power Control

**Folder:** `examples/12-mock-power-control/`

#### Use case

Exercise Power v2 suite logic without real power hardware.

#### Covers

- `resources.dut_power`
- `type: mock_power`
- `power_set`
- `power_cycle`
- `power_expect`
- local/demo validation of suite behavior

#### Traceability level

Simple / development.

This example is intended for docs, CI dry-runs, local development, and testing BenchCI itself.

#### When to use

- learning Power v2 syntax
- validating suite structure before wiring hardware
- demo mode
- automated tests of BenchCI behavior

---

### 13. HTTP Measurement

**Folder:** `examples/13-http-measurement/`

#### Use case

Read a real measurement value from an HTTP-accessible instrument, lab controller, or measurement service and assert it against a threshold.

#### Covers

- `resources.supply_current` or similar measurement resource
- `type: http_measurement`
- `measure`
- `record_as`
- `assert_metric`
- metrics in `results.json` and `evidence.json`

#### Traceability level

Moderate / QA-oriented.

This example shows Measurement v1 with a real external data source. It is useful when a lab controller exposes values such as current, voltage, temperature, pressure, or other physical measurements over HTTP.

#### When to use

- low-power current checks
- voltage rail checks
- external sensor/instrument readings
- lab controllers that expose JSON measurement endpoints
- QA evidence where measured values matter

---

### 14. HTTP Measurement Mock

**Folder:** `examples/14-http-measurement-mock/`

#### Use case

Demonstrate Measurement v1 behavior with mock-style measurement data and HTTP-style structure.

#### Covers

- measurement resource configuration
- `measure`
- `record_as`
- `assert_metric`
- evidence metrics
- development/demo workflow before connecting a real instrument

#### Traceability level

Simple / development.

This example is useful for learning the measurement model and verifying that metrics appear in generated artifacts and evidence reports.

#### When to use

- learning Measurement v1 syntax
- testing dashboard/evidence display
- CI dry-runs
- developing a future real measurement backend

---

## How to use these examples

1. Copy an example folder:

```bash
cp -r examples/09-stm32wl-boot-validation-traceable my-test
cd my-test
```

2. Adjust hardware-specific values:

- serial ports, for example `/dev/ttyUSB0`, `/dev/ttyACM0`, or `/dev/cu.usbmodem...`
- IP addresses, for example Modbus TCP hosts, HTTP relay hosts, HTTP measurement hosts, or remote GPIO hosts
- GPIO chips and lines, for example `/dev/gpiochip0`, line `17`
- relay commands, for example serial ON/OFF hex command maps
- measurement URLs and JSON fields
- probe serials
- CAN interfaces, for example `can0`
- firmware paths, for example `build/fw.elf` or `build/firmware.bin`
- expected UART/CAN/Modbus responses
- current/voltage/temperature thresholds

3. Run doctor to inspect your machine:

```bash
benchci doctor
benchci doctor --ports
benchci doctor --usb
benchci doctor --bench bench.yaml
```

4. Validate the config:

```bash
benchci validate --bench bench.yaml --suite suite.yaml
```

5. Run locally:

```bash
benchci run --bench bench.yaml --suite suite.yaml --artifact build/fw.elf --verbose
```

For examples that define the firmware artifact path inside `bench.yaml`, `--artifact` may be optional. Passing `--artifact` from the CLI is still useful in CI because it makes the tested firmware explicit.

---

## Evidence Reports, measurements, and traceability

Traceability examples may include fields like:

```yaml
suite:
  name: stm32wl-boot-validation
  version: "1.0.0"
  release_id: "demo-fw-0.1.0"
  requirement_ids:
    - REQ-BOOT-001
  risk_ids:
    - RISK-BOOT-001
  tags:
    - smoke
    - hardware-ci

tests:
  - name: firmware boots and prints ready
    test_case_id: TC-BOOT-001
    requirement_ids:
      - REQ-BOOT-001
    risk_ids:
      - RISK-BOOT-001
    tags:
      - boot
      - uart
    steps:
      - flash:
          node: dut
      - expect_uart:
          node: dut
          transport: console
          contains: "READY"
          within_ms: 5000
```

Measurement examples may include steps like:

```yaml
- measure:
    resource: supply_current
    record_as: sleep_current_a
    unit: A
    expect_less_than: 0.150

- assert_metric:
    name: sleep_current_a
    expect_less_than_or_equal: 0.150
```

These fields help BenchCI connect a run to:

```text
requirement -> test case -> hardware run -> evidence artifact -> measured behavior
```

After a run, BenchCI can produce artifacts such as:

```text
benchci-results/
├── results.json
├── evidence.json
├── evidence.html
├── manifest.json
├── metadata.json
├── inputs/
│   ├── bench.yaml
│   └── suite.yaml
├── resources/
│   └── dut_power/
│       └── power.log
└── nodes/
    └── dut/
        ├── flash.log
        └── transport-console.log
```

Use `evidence.html` for a human-readable report, `evidence.json` for machine-readable traceability and metrics, and `manifest.json` for artifact integrity hashes.

---

## Important notes

### These are templates

You must adapt:

- ports
- IP addresses
- GPIO lines
- relay commands
- HTTP URLs
- measurement JSON fields
- hardware wiring
- expected responses
- firmware artifact paths
- flashing tool configuration
- measurement thresholds

### Bench resources hide vendor details

Power and measurement examples use the newer resource model:

```text
bench.yaml  -> how the lab hardware works
suite.yaml  -> what the test wants to prove
```

For example, a suite should say:

```yaml
- power_cycle:
    resource: dut_power
    outlet: main
```

The suite should not need to know whether the outlet is controlled by GPIO, an HTTP relay, a generic serial relay, or a future SCPI power supply backend.

### One GPIO backend per node

Currently, a node should use one GPIO backend consistently.

Avoid mixing these in the same node:

- `local_gpio`
- `remote_gpio`
- `mock_gpio`

Use a separate node if you need to model different GPIO control locations.

### Local GPIO vs remote GPIO

Use `local_gpio` when the BenchCI runner/Agent is running on the same Linux machine that owns the GPIO device:

```yaml
backend: local_gpio
chip: /dev/gpiochip0
line: 17
```

Use `remote_gpio` when GPIO operations are delegated to another BenchCI-compatible service:

```yaml
backend: remote_gpio
host: 192.168.1.60
port: 8090
token_env: BENCHCI_REMOTE_GPIO_TOKEN
chip: /dev/gpiochip0
line: 17
```

### CAN examples need SocketCAN setup

Before running CAN examples, make sure your CAN interface exists and is up, for example:

```bash
sudo ip link set can0 up type can bitrate 500000
ip link show can0
```

### Use smaller benches in practice

Real setups usually start with:

- one DUT
- one flashing method
- one UART or fieldbus transport
- one or two GPIO lines
- one power resource if power cycling is needed
- one measurement resource if physical behavior needs to be verified

Examples can show more capability than a first production setup should use.

---

## Recommended learning path

If you are new to BenchCI:

1. Start with a simple communication example:
   - `02-modbus-rtu-plc-simple`
   - `06-multi-node-uart-simple`
   - `08-can-ecu-handshake-simple`

2. Try a flashing example:
   - `09-stm32wl-boot-validation-traceable`
   - `01-esp32-esptool-uart-traceable`

3. Try GPIO control:
   - `05-local-gpio-reset-ready-advanced`
   - `07-remote-gpio-power-cycle-moderate`

4. Try Power v2:
   - `10-generic-serial-power-relay`
   - `11-http-power-relay`
   - `12-mock-power-control`

5. Try Measurement v1:
   - `13-http-measurement`
   - `14-http-measurement-mock`

6. Try a more production-like provisioning flow:
   - `04-gateway-jlink-provisioning-moderate`

7. Try Cloud execution after local validation.

---

## Cloud Mode example path

After validating an example locally, you can run the same suite through Cloud Mode if the bench is connected through a cloud Agent.

```bash
benchci login

benchci benches list

benchci run \
  --cloud \
  --bench-id my-cloud-bench \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --verbose
```

Use the dashboard to inspect:

- run status
- evidence summary
- traceability
- metrics and measurements
- failure classification
- events
- artifacts

Dashboard:

```text
https://app.benchci.dev
```

---

## Summary

These examples demonstrate that BenchCI supports:

- multiple flashing backends
- UART, Modbus RTU, Modbus TCP, and CAN
- GPIO automation, both local and remote
- Power v2 resources for generic serial relay, HTTP relay, and mock power control
- Measurement v1 resources for HTTP and mock-style measurement workflows
- multi-node orchestration
- CI-friendly execution through Agent and Cloud Mode
- structured results, logs, Evidence Reports, traceability metadata, measurements, metrics, and artifact integrity manifests

BenchCI scales from:

```text
single-board debugging
        ↓
repeatable local hardware tests
        ↓
shared cloud-connected benches
        ↓
traceable hardware validation evidence
```

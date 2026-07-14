# BenchCI Examples

Use these examples as starting templates for real embedded workflows such as boot validation, GPIO reset, Modbus, CAN, I2C, SPI, bounded protocol fuzzing, ESP32, J-Link, remote GPIO, power resources, measurement resources, and multi-node testing.

---

This page contains **realistic example scenarios** showing how to use BenchCI in different setups.

Each example folder includes:

- `bench.yaml` → hardware configuration
- `suite.yaml` → test logic

Some examples are intentionally simple. Others show optional traceability fields used by Evidence Reports, such as requirement IDs, test case IDs, risk IDs, release IDs, and tags.

For a smaller starting point, run `benchci init --list-presets` and generate editable starter files with `benchci init --preset <preset-id>`. The dashboard Config Builder can export the same preset-based `bench.yaml` and `suite.yaml` pairs from the browser.

---

## Start here

If you are new to BenchCI, begin with one of the simple communication examples:

- `examples/02-modbus-rtu-plc-simple/`
- `examples/06-multi-node-uart-simple/`
- `examples/08-can-ecu-handshake-simple/`

If you want to see Evidence Reports and traceability metadata, start with:

- `examples/01-esp32-esptool-uart-traceable/`
- `examples/09-stm32wl-boot-validation-traceable/`
- `examples/18-traceable-release-smoke/`

If you want to try the resource model, start with:

- `examples/10-generic-serial-power-relay/`
- `examples/11-http-power-relay/`
- `examples/12-http-measurement/`
- `examples/13-scpi/`
- `examples/14-low-power-current/`

If you want a bounded robustness-testing template, start with:

- `examples/15-protocol-fuzzing/`

If you want board-level bus checks, start with:

- `examples/16-i2c-spi-registers/`
- `examples/17-station-i2c-spi-smoke/`

If you want a release-review traceability walkthrough, start with:

- `examples/18-traceable-release-smoke/`

If you want test design technique templates, start with:

- `examples/19-boundary-value-threshold/`
- `examples/20-state-transition-update-flow/`
- `examples/21-decision-table-safety-update/`

These examples are templates. You must adapt ports, IP addresses, GPIO lines, firmware paths, expected responses, relay commands, measurement URLs, and flashing tool settings for your hardware.

<!-- Unreleased hardware examples are intentionally hidden until release. -->

---

## Example difficulty levels

Not every example needs traceability metadata. Public examples are intentionally mixed:

- **Simple examples** teach the basic BenchCI model with minimal YAML.
- **Moderate examples** include more realistic hardware resources, flashing, power, measurement, or reset flows.
- **Traceability examples** show requirement IDs, test case IDs, risk IDs, release IDs, and tags for Evidence Reports.
- **Resource examples** show the BenchCI resource model where `bench.yaml` hides hardware/vendor details and `suite.yaml` stays focused on test intent.

Start simple, then add traceability, power resources, and measurement resources when a run should support QA or release evidence.

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
├── 12-http-measurement/
│   ├── bench.yaml
│   └── suite.yaml
├── 13-scpi/
│   ├── bench.yaml
│   ├── suite.yaml
│   ├── bench_owon_sp_serial.yaml
│   └── suite_owon_sp.yaml
├── 14-low-power-current/
│   ├── bench.yaml
│   └── suite.yaml
├── 15-protocol-fuzzing/
│   ├── bench.yaml
│   └── suite.yaml
├── 16-i2c-spi-registers/
│   ├── bench.yaml
│   └── suite.yaml
├── 17-station-i2c-spi-smoke/
│   ├── README.md
│   ├── bench.yaml
│   ├── i2c-smoke.suite.yaml
│   └── spi-smoke.suite.yaml
├── 18-traceable-release-smoke/
│   ├── README.md
│   ├── bench.yaml
│   └── suite.yaml
├── 19-boundary-value-threshold/
│   ├── README.md
│   ├── bench.yaml
│   └── suite.yaml
├── 20-state-transition-update-flow/
│   ├── README.md
│   ├── bench.yaml
│   └── suite.yaml
└── 21-decision-table-safety-update/
    ├── README.md
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
- classic CAN and CAN FD frame syntax
- optional filters and masked expectations
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

This example demonstrates the preferred Power resource pattern: the suite says `power_cycle`, while `bench.yaml` contains the vendor-specific serial commands.

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

### 12. HTTP Measurement

**Folder:** `examples/12-http-measurement/`

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

This example shows Measurement with a real external data source. It is useful when a lab controller exposes values such as current, voltage, temperature, pressure, or other physical measurements over HTTP.

#### When to use

- low-power current checks
- voltage rail checks
- external sensor/instrument readings
- lab controllers that expose JSON measurement endpoints
- QA evidence where measured values matter

### 13. SCPI Measurement

**Folder:** `examples/13-scpi/`

#### Use case

Read current and voltage from a SCPI simulator or a SCPI-capable power supply, then record those readings as BenchCI metrics.

#### Covers

- `type: scpi_measurement` for raw SCPI queries
- `type: scpi_power_supply_measurement` for common power-supply current/voltage readback
- TCP/IP SCPI with `tcp://host:port`
- serial/RS232 SCPI with `serial:///dev/ttyUSB0` or `serial://COM3`
- USB/VISA-style SCPI resource strings where supported by PyVISA
- `benchci measure` one-off measurement debugging
- `measure`, `record_as`, and metric threshold assertions
- measurement logs and dashboard metric cards

#### Traceability level

Moderate / QA-oriented.

This example is useful for teams that want electrical evidence such as current draw or supply voltage to appear in CI logs, run artifacts, and dashboard run detail.

#### Start with the simulator

```bash
python tools/scpi_simulator.py --mode tcp --host 127.0.0.1 --port 5025

benchci measure --bench examples/13-scpi/bench.yaml supply_current

benchci run   --bench examples/13-scpi/bench.yaml   --suite examples/13-scpi/suite.yaml   --skip-flash
```

#### OWON SP serial/RS232 example

Use the OWON example as a starting point for SP/SPE/SPS-style serial SCPI supplies:

```bash
benchci measure   --bench examples/13-scpi/bench_owon_sp_serial.yaml   supply_current
```

Adjust the serial path before running:

```yaml
address: serial:///dev/tty.usbserial-XXXX
```

#### When to use

- low-power current checks
- voltage rail checks
- programmable power supply readback
- RS232/USB/LAN instrument debugging
- QA evidence where measured electrical values matter

---

### 14. Low-Power Current

**Folder:** `examples/14-low-power-current/`

#### Use case

Boot a DUT, send it to sleep mode, then measure current draw over the supply rail and assert a low-power threshold.

#### Covers

- `power_cycle` to power the DUT
- `expect_uart` and `send_uart` for boot and command sequencing
- `type: scpi_power_supply_measurement` or `type: i2c_power_monitor` for supply current readback
- `measure` with `record_as` and `expect_less_than`
- `assert_metric` to re-assert a recorded value
- current measurement in `evidence.json` and `evidence.html`

#### Traceability level

Moderate / QA-oriented.

This example shows a complete low-power validation flow: power cycle, boot, command to enter sleep, measure, and assert. It is useful for any board where sleep current is a product requirement.

#### When to use

- low-power IoT devices
- sleep-current validation in CI
- power budget regression testing
- QA evidence where measured current values must appear in artifacts

---

<!-- Unreleased hardware example section is intentionally hidden until release. -->

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
└── logs/
    ├── nodes/
    │   └── dut/
    │       ├── flash.log
    │       └── transport-console.log
    └── resources/
        └── dut_power/
            └── power.log
```

Use `evidence.html` for a human-readable report, `evidence.json` for machine-readable traceability and metrics, and `manifest.json` for artifact integrity hashes.

---

## Test design technique examples

Examples 19–21 show how Chapter 4-style test analysis and design can appear in BenchCI without adding new schema fields.

| Example | Technique | What it demonstrates |
| --- | --- | --- |
| `examples/19-boundary-value-threshold/` | Boundary value analysis | Measurement checks around a 3.0 V to 4.2 V safety range using mock measurement resources. |
| `examples/20-state-transition-update-flow/` | State transition testing | A firmware update flow with valid transitions, invalid transition rejection, and recovery behavior. |
| `examples/21-decision-table-safety-update/` | Decision table testing | Update eligibility rules for battery state, firmware signature, and device idle/busy state. |

These examples use tags such as `black-box`, `boundary-value`, `state-transition`, `decision-table`, `negative-test`, `safety`, and `acceptance`. They are evidence-friendly templates, not proof that the selected technique coverage is complete.

See [Test Design Techniques for Embedded Hardware](test_design_techniques.md) for the conceptual mapping.

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

Power and measurement examples use the resource model:

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

For CAN FD, configure the interface for FD before running BenchCI:

```bash
sudo ip link set can0 up type can bitrate 500000 dbitrate 2000000 fd on
ip -details link show can0
```

Optional `vcan0` integration tests can be enabled on privileged Linux test hosts:

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
BENCHCI_ENABLE_VCAN_TESTS=1 python -m pytest tests/test_can_transport.py -k vcan0
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

4. Try Power:
   - `10-generic-serial-power-relay`
   - `11-http-power-relay`

5. Try Measurement:
   - `12-http-measurement`
   - `13-scpi`
   - `14-low-power-current`

6. Try bounded protocol fuzzing:
   - `15-protocol-fuzzing`

7. Try test design technique templates:
   - `19-boundary-value-threshold`
   - `20-state-transition-update-flow`
   - `21-decision-table-safety-update`

8. Try a more production-like provisioning flow:
   - `04-gateway-jlink-provisioning-moderate`

9. Try Cloud execution after local validation.

---

## Protocol fuzzing example

`examples/15-protocol-fuzzing/` shows `fuzz_uart`, `fuzz_can`, and `fuzz_modbus` steps with fixed seeds, conservative iteration limits, and artifact-friendly case logs.

Use it when you already have smoke/regression checks working and want a bounded robustness gate that records enough metadata to replay the first failing case.

## Station I2C/SPI smoke example

`examples/17-station-i2c-spi-smoke/` contains separate I2C and SPI smoke
suites for a Linux-based Station or Agent host. Update the real
`/dev/i2c-*` bus, `/dev/spidev*.*` bus/device, DUT identity, expected register
values, and expected SPI response before use.

Run the suites locally:

```bash
benchci run --bench examples/17-station-i2c-spi-smoke/bench.yaml \
  --suite examples/17-station-i2c-spi-smoke/i2c-smoke.suite.yaml \
  --skip-flash

benchci run --bench examples/17-station-i2c-spi-smoke/bench.yaml \
  --suite examples/17-station-i2c-spi-smoke/spi-smoke.suite.yaml \
  --skip-flash
```

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
- UART, Modbus RTU, Modbus TCP, CAN, I2C, and SPI
- bounded UART, CAN, and Modbus protocol fuzzing
- GPIO automation, both local and remote
- Power resources for generic serial relay, HTTP relay, and GPIO power
- Measurement resources for HTTP, SCPI, I2C power monitors, script, and serial backends
- multi-node orchestration
- CI-friendly execution through Agent and Cloud Mode
- structured results, logs, Evidence Reports, traceability metadata, fuzz summaries, measurements, metrics, and artifact integrity manifests

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

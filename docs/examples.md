# BenchCI Examples

This page contains **realistic example scenarios** showing how to use BenchCI in different setups.

Each example includes:
- `bench.yaml` → hardware configuration
- `suite.yaml` → test logic

These are not artificial “all-in-one” examples — they reflect **real-world use cases**.

---

## 📦 Example Scenarios

---

### 1. Device Boot Validation

**Folder:** `examples/device_boot_validation/`

#### Use Case

Validate that firmware:
- boots correctly
- prints expected logs
- responds to commands over UART

#### Covers

- OpenOCD flashing
- UART transport
- `flash`, `reset`, `send_uart`, `expect_uart`

#### When to use

- firmware smoke tests
- CI validation after build
- basic bring-up

---

### 2. Local GPIO Reset & Ready Monitoring

**Folder:** `examples/local_gpio_reset_and_ready/`

#### Use Case

Control reset lines and verify device readiness using Linux GPIO.

#### Covers

- `local_gpio`
- `gpio_set`, `gpio_expect`, `gpio_wait_edge`
- manual reset sequencing

#### When to use

- hardware bring-up
- boards without reliable debugger reset
- interrupt validation

---

### 3. Remote GPIO Power Cycling

**Folder:** `examples/remote_gpio_power_cycle/`

#### Use Case

Control power and signals from a **different machine** via Agent.

#### Covers

- `remote_gpio`
- distributed setups
- power cycling DUT

#### When to use

- CI runner ≠ hardware machine
- remote labs
- shared hardware infrastructure

---

### 4. Modbus RTU PLC Validation

**Folder:** `examples/modbus_rtu_plc_validation/`

#### Use Case

Validate a PLC or RS-485 device.

#### Covers

- Modbus RTU transport
- register + coil operations

#### When to use

- industrial devices
- embedded fieldbus testing

---

### 5. Modbus TCP Gateway Validation

**Folder:** `examples/modbus_tcp_gateway_validation/`

#### Use Case

Test Ethernet-connected industrial devices.

#### Covers

- Modbus TCP
- network-based communication

#### When to use

- gateways
- PLC over Ethernet
- integration tests

---

### 6. CAN ECU Handshake

**Folder:** `examples/can_ecu_handshake/`

#### Use Case

Validate request/response behavior on CAN bus.

#### Covers

- CAN transport
- `send_can`, `expect_can`

#### When to use

- automotive ECUs
- multi-node embedded systems

---

### 7. CubeProgrammer Helper Board

**Folder:** `examples/helper_board_cubeprog/`

#### Use Case

Flash STM32 device using CubeProgrammer.

#### Covers

- `cubeprog` backend
- UART validation

#### When to use

- STM32 production workflows
- environments without OpenOCD

---

### 8. J-Link Gateway Provisioning

**Folder:** `examples/gateway_jlink_provisioning/`

#### Use Case

Provision firmware using SEGGER J-Link.

#### Covers

- `jlink` backend
- high-speed flashing

#### When to use

- production flashing
- Segger-based setups

---

### 9. ESP32 esptool Workflow

**Folder:** `examples/esp32_esptool_wifi_probe/`

#### Use Case

Flash ESP32 firmware and validate startup.

#### Covers

- `esptool` backend
- UART validation

#### When to use

- ESP32 / ESP-IDF projects
- IoT devices

---

### 10. Mock GPIO Simulation

**Folder:** `examples/mock_gpio_simulation/`

#### Use Case

Test logic without real hardware.

#### Covers

- `mock_gpio`
- GPIO logic testing

#### When to use

- development without hardware
- CI pipelines without devices

---

### 11. Multi-Node System Test

**Folder:** `examples/multi_node_system_smoke/`

#### Use Case

Coordinate multiple devices in one test.

#### Covers

- multiple nodes
- cross-device interaction

#### When to use

- system-level testing
- DUT + controller setups

---

## 🧠 How to Use These Examples

1. Copy an example folder:

cp -r examples/device_boot_validation my-test
cd my-test

2. Adjust hardware-specific values:
- serial ports (e.g. `/dev/ttyUSB0`)
- IP addresses
- GPIO lines
- probe serials
- firmware paths

3. Run:

benchci run -b bench.yaml -s suite.yaml -a build/fw.elf

---

## ⚠️ Important Notes

### These are templates

You MUST adapt:
- ports
- addresses
- hardware wiring
- expected responses

---

### One GPIO backend per node

Currently:
- a node can use **only one GPIO backend**

Do NOT mix:
- `local_gpio` and `remote_gpio` in the same node

---

### Use smaller benches in practice

Real setups typically:
- use 1–2 nodes
- use 1–2 transports

These examples show **capability coverage**, not minimal setups.

---

## 🚀 Recommended Learning Path

If you’re new to BenchCI:

1. Start with:
   - `device_boot_validation`

2. Then try:
   - `local_gpio_reset_and_ready`

3. Then explore:
   - Modbus or CAN examples

4. Finally:
   - multi-node setups
   - remote GPIO

---

## 🎯 Summary

These examples demonstrate that BenchCI supports:

- multiple flashing backends
- multiple transport protocols
- GPIO automation (local and remote)
- multi-node orchestration
- CI-friendly execution

BenchCI scales from:

single board debugging  
→ to  
distributed hardware validation systems

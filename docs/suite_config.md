# Suite Configuration

BenchCI test suites define automated hardware tests.

Suites are written in YAML.

---

## Structure

```
name
tests
```

Each test contains steps.

---

## Example

```
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

---

## Step Types

**sleep_ms**

Pause execution.

**send_uart**

Send text to UART.

**expect_uart**

Validate UART output.

**modbus_read_holding_registers**

Read Modbus holding registers.

**modbus_write_single_register**

Write Modbus holding registers.

**modbus_read_coils**

Read Modbus coil values.

**modbus_write_single_coil**

Write a Modbus coil.

**reset**

Reset the device.
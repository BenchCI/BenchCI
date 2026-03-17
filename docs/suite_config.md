# Suite Configuration

BenchCI test suites define automated hardware tests.

---

## Structure

```
name
tests
```

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
```

---

## Core Steps

### reset

Reset the device.

```
- reset
```

---

### sleep_ms

Pause execution.

```
- sleep_ms: 100
```

---

### send_uart

```
- send_uart: "PING\n"
```

---

### expect_uart

```
- expect_uart:
    contains: "PONG"
    within_ms: 1000
```

---

## Modbus Steps

* modbus_read_holding_registers
* modbus_write_single_register
* modbus_read_coils
* modbus_write_single_coil

---

## GPIO Steps

### gpio_set

```
- gpio_set:
    line: reset_n
    value: true
```

---

### gpio_get

```
- gpio_get:
    line: ready
```

---

### gpio_expect

```
- gpio_expect:
    line: ready
    value: true
    within_ms: 3000
```

---

### gpio_wait_edge

```
- gpio_wait_edge:
    line: irq
    edge: rising
    within_ms: 2000
```

Notes:

* GPIO lines must be defined in `board.yaml`
* edge detection requires `edge` configuration

# Board Configuration

Board configuration describes how BenchCI interacts with hardware.

Defined in `board.yaml`.

---

## Structure

```
name
flash
reset
transport
gpio
```

---

## Flash Configuration

```
flash:
  backend: openocd
  interface_cfg: interface/stlink.cfg
  target_cfg: target/stm32f4x.cfg
```

Supported:

* openocd
* cubeprog
* jlink

---

## Reset Configuration

```
reset:
  method: openocd
```

Options:

* openocd
* cubeprog
* jlink
* none

---

## Transport Configuration

### UART

```
transport:
  backend: uart
  port: /dev/ttyUSB0
  baud: 115200
```

### Modbus RTU

```
transport:
  backend: modbus_rtu
  port: /dev/ttyUSB0
  baud: 9600
  default_slave: 1
```

### Modbus TCP

```
transport:
  backend: modbus_tcp
  host: 192.168.1.50
  port: 502
  timeout_ms: 1000
  default_slave: 1
```

---

## GPIO Configuration

```
gpio:
  ready:
    backend: local_gpio
    chip: /dev/gpiochip0
    line: 18
    direction: input
    active_high: true
    bias: pull_down

  irq:
    backend: local_gpio
    chip: /dev/gpiochip0
    line: 19
    direction: input
    active_high: true
    bias: pull_down
    edge: rising
```

Fields:

* chip
* line
* direction
* active_high
* bias
* edge

GPIO lines are referenced in test steps.

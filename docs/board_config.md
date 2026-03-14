# Board Configuration

Board configuration describes how BenchCI interacts with hardware.

The configuration is defined in `board.yaml`.

---

## Structure

```
name
flash
reset
transport
```

---

## Flash Configuration

Example:

```
flash:
  backend: openocd
  interface_cfg: interface/stlink.cfg
  target_cfg: target/stm32f4x.cfg
```

Supported backends:

- openocd
- cubeprog
- jlink

---

## Reset Configuration

```
reset:
  method: openocd
```

Options:

- openocd
- cubeprog
- jlink
- none

---

## Transport Configuration

Example UART:

```
transport:
  backend: uart
  port: /dev/ttyUSB0
  baud: 115200
```

Example Modbus RTU:

```
transport:
  backend: modbus_rtu
  port: /dev/ttyUSB0
  baud: 9600
  default_slave: 1
```
# Device Boot Validation Example

This example demonstrates a realistic BenchCI workflow for validating device boot behavior using both GPIO and UART.

It shows how to:

* reset the device using configured flashing tool
* wait for a ready signal from the device
* verify a boot message over UART
* send a command after boot
* wait for an interrupt signal on a GPIO line

Notes:

* device reset is handled via the configured flash/reset backend
* GPIO lines are used for observing device state and events

---

## What this example validates

The device under test is expected to behave as follows:

1. When reset is released, the device boots
2. The `ready` pin becomes active within 3 seconds
3. The device prints `[BOOT] OK` over UART
4. The device responds `PONG` to `PING`
5. The device asserts `irq` after receiving `TRIGGER_IRQ`

---

## Files

* `board.yaml` defines hardware connections and transports
* `suite.yaml` defines the boot validation test flow

---

## Example run

```
benchci run \
  -b board.yaml \
  -s suite.yaml \
  -a build/fw.elf
```

---

## Hardware mapping

Adjust the following values in `board.yaml` for your setup:

* UART port: /dev/ttyUSB0
* GPIO chip: /dev/gpiochip0
* GPIO line numbers: 17, 18, 19

---

## Notes

* `reset_n` is modeled as an active-low output
* `ready` is polled as a digital input
* `irq` is configured for rising-edge detection
* this example assumes Linux GPIO support is available on the runner machine

# Linux GPIO in BenchCI

BenchCI provides native support for controlling and observing Linux GPIO lines.

This allows you to integrate real hardware signals (reset lines, status pins, interrupts, etc.) into automated test workflows.

---

## What is Linux GPIO?

On Linux systems, GPIOs are exposed via the GPIO character device interface:

* /dev/gpiochip0
* /dev/gpiochip1

Each chip contains multiple GPIO lines (channels), which can be:

* configured as input or output
* read or driven
* monitored for edge events (rising / falling)

BenchCI uses the modern libgpiod interface (not the deprecated sysfs GPIO).

---

## Why use GPIO in BenchCI?

GPIO control is essential for real hardware validation:

* reset devices
* trigger boot modes
* simulate button presses
* monitor ready/interrupt signals
* synchronize test steps with hardware state

Instead of manual interaction, BenchCI allows you to define these behaviors declaratively in your test suite.

---

## Example Use Cases

### Reset control

```
- gpio_set:
    line: reset_n
    value: false

- sleep_ms: 100

- gpio_set:
    line: reset_n
    value: true
```

### Wait for device ready

```
- gpio_expect:
    line: ready
    value: true
    within_ms: 3000
```

### Wait for interrupt (edge detection)

```
- gpio_wait_edge:
    line: irq
    edge: rising
    within_ms: 2000
```

---

## Board Configuration

GPIO lines are defined in board.yaml.

Example:

```
gpio:
  reset_n:
    backend: local_gpio
    chip: /dev/gpiochip0
    line: 17
    direction: output
    active_high: false

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

---

## Configuration Fields

### Common

* backend: must be local_gpio
* chip: GPIO chip device (e.g. /dev/gpiochip0)
* line: line number within the chip

---

### Direction

direction: output

or

direction: input

---

### Active Level

active_high: true

or

active_high: false

This defines the logical meaning of the signal:

* true → ACTIVE state
* false → INACTIVE state

BenchCI automatically maps this to the correct electrical level.

Example:

active_high: true  → value true = GPIO HIGH
active_high: false → value true = GPIO LOW

---

### Bias (input only)

bias: pull_up
bias: pull_down
bias: disabled

Used for stabilizing input lines.

---

### Edge Detection (input only)

edge: rising
edge: falling
edge: both

Required for gpio_wait_edge.

---

## Test Suite Steps

### Set output

```
- gpio_set:
    line: reset_n
    value: true
```

### Read input

```
- gpio_get:
    line: ready
```

### Wait for value

```
- gpio_expect:
    line: ready
    value: true
    within_ms: 1000
```

### Wait for edge

```
- gpio_wait_edge:
    line: irq
    edge: rising
    within_ms: 2000
```

---

## Logical vs Physical Values

BenchCI uses logical values, not raw voltage levels.

This means:

* value: true → signal is ACTIVE
* value: false → signal is INACTIVE

The actual electrical level depends on active_high.

This makes tests portable and easier to understand.

---

## Requirements

To use Linux GPIO:

* Linux system with /dev/gpiochipX
* libgpiod installed
* Python gpiod bindings available
* appropriate permissions to access GPIO devices

---

## Permissions

You may need to run:

```
sudo usermod -aG gpio $USER
```

or run BenchCI with sufficient privileges.

---

## Notes

* GPIO lines are requested exclusively by BenchCI during execution
* Make sure no other process is using the same GPIO lines
* Edge detection requires proper hardware configuration (pull-ups/downs)

---

## Summary

BenchCI allows you to:

* control GPIO outputs
* read input states
* wait for signal changes
* integrate real hardware signals into CI workflows

This enables reliable, repeatable hardware validation without manual interaction.

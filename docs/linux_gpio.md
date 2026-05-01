# Linux GPIO in BenchCI

Use this page when your bench needs reset lines, ready signals, interrupts, trigger pins, or relay control through Linux GPIO.

---

BenchCI supports Linux GPIO through the `local_gpio` backend and also supports split deployments through `remote_gpio`.

## What BenchCI uses

BenchCI uses the Linux GPIO character device model, for example:

- `/dev/gpiochip0`
- `/dev/gpiochip1`

It uses libgpiod-style access rather than the deprecated sysfs GPIO interface.

## Why GPIO matters

GPIO lets BenchCI automate hardware signals such as:

- reset lines
- boot mode pins
- ready/status outputs
- interrupt lines
- trigger lines between nodes

## Local GPIO example

```yaml
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

## Remote GPIO example

```yaml
gpio:
  reset_n:
    backend: remote_gpio
    host: 192.168.1.60
    port: 8090
    token_env: BENCHCI_AGENT_TOKEN
    chip: /dev/gpiochip0
    line: 17
    direction: output
    active_high: false
```

`remote_gpio` delegates GPIO operations to a BenchCI-compatible remote service, typically a BenchCI Agent running on a Linux machine with GPIO access.

## Logical vs physical values

BenchCI uses **logical** values in suites:

- `true` means active
- `false` means inactive

The actual electrical level depends on `active_high`.

Examples:

- `active_high: true` → logical `true` maps to physical high
- `active_high: false` → logical `true` maps to physical low

This keeps test logic readable and hardware-agnostic.

## GPIO suite steps

### Set output

```yaml
- gpio_set:
    node: dut
    line: reset_n
    value: false
```

### Read input

```yaml
- gpio_get:
    node: dut
    line: ready
```

### Wait for value

```yaml
- gpio_expect:
    node: dut
    line: ready
    value: true
    within_ms: 3000
```

### Wait for edge

```yaml
- gpio_wait_edge:
    node: dut
    line: irq
    edge: rising
    within_ms: 2000
```

## Input options

Input lines can define:

- `bias: disabled`
- `bias: pull_up`
- `bias: pull_down`

For edge-based waits, the line should also define:

- `edge: rising`
- `edge: falling`
- `edge: both`

## Requirements for `local_gpio`

You need:

- Linux
- `/dev/gpiochipX` devices
- Python `gpiod` bindings
- permission to access the GPIO device

Useful diagnostic commands:

```bash
benchci doctor --ports
benchci doctor --usb
benchci doctor --bench bench.yaml
```

Doctor can list GPIO chips such as `/dev/gpiochip0` and warn when a bench references a GPIO chip that is not available on the current machine.

## Notes

- BenchCI requests GPIO lines exclusively during use
- do not let another process hold the same lines
- edge waits depend on correct hardware wiring and pull configuration
- `remote_gpio` still uses logical line names in tests; only the control path changes


## Agent and Cloud Mode

`local_gpio` is used by the machine physically connected to the GPIO device.

In Direct Agent Mode, that machine is usually the Agent host.

In Cloud Mode, the cloud-connected Agent executes `run_local(...)` near the hardware, so GPIO access still happens locally on the Agent machine. The user or CI runner does not need direct access to `/dev/gpiochipX`.
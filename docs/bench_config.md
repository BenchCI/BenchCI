# Bench Configuration

BenchCI bench configuration is stored in `bench.yaml`. It describes the real execution environment: nodes, transports, GPIO, flashing, reset behavior, defaults, and artifact settings.

## Top-level structure

A bench file uses these main sections:

```yaml
version: "1"

bench:
  name: my_bench
  description: Optional description

defaults:
  node: dut
  timeouts:
    within_ms: 1000

nodes:
  dut:
    kind: mcu
    role: target
    transports: {}
    gpio: {}

resources: {}

artifacts:
  root_dir: benchci-results
  per_node_dirs: true
```

## Main sections

### `version`

Schema version string.

### `bench`

Bench-level metadata.

```yaml
bench:
  name: my_bench
  description: Example hardware bench
```

### `defaults`

Optional defaults used by suites and the runner.

```yaml
defaults:
  node: dut
  timeouts:
    within_ms: 1000
```

- `defaults.node` is used when a suite step omits `node`
- `defaults.timeouts.within_ms` is used when a wait/expect step omits an explicit timeout

### `nodes`

The core of the bench. Each node is a named participant such as `dut`, `controller`, `gateway`, or `peer`.

Each node may define:

- `kind`
- `role`
- `tags`
- `flash`
- `reset`
- `transports`
- `gpio`

A node must define at least one of:

- `flash`
- `transports`
- `gpio`

### `resources`

Optional bench-level shared resources reserved for expansion.

### `artifacts`

Output behavior for generated artifacts.

```yaml
artifacts:
  root_dir: benchci-results
  per_node_dirs: true
```

## Full example

```yaml
version: "1"

bench:
  name: stm32_can_lab
  description: DUT plus helper node with UART, CAN, and GPIO

defaults:
  node: dut
  timeouts:
    within_ms: 1000

nodes:
  dut:
    kind: mcu
    role: target
    tags: [stm32, can]

    flash:
      backend: openocd
      interface_cfg: interface/stlink.cfg
      target_cfg: target/stm32wlx.cfg
      adapter_speed_khz: 500
      artifact: build/firmware.elf

    reset:
      method: openocd

    transports:
      console:
        backend: uart
        port: /dev/ttyUSB0
        baud: 115200
        timeout_ms: 100

      bus:
        backend: can
        interface: can0
        bitrate: 500000
        timeout_ms: 500

    gpio:
      ready:
        backend: local_gpio
        chip: /dev/gpiochip0
        line: 18
        direction: input
        active_high: true
        bias: pull_down

      reset_n:
        backend: local_gpio
        chip: /dev/gpiochip0
        line: 19
        direction: output
        active_high: false

  helper:
    kind: controller
    role: peer

    transports:
      plc:
        backend: modbus_tcp
        host: 192.168.1.50
        port: 502
        timeout_ms: 1000
        default_slave: 1

artifacts:
  root_dir: benchci-results
  per_node_dirs: true
```

## Flash configuration

A node can define one flash backend.

### OpenOCD

```yaml
flash:
  backend: openocd
  interface_cfg: interface/stlink.cfg
  target_cfg: target/stm32f4x.cfg
  extra_args: []
  adapter_speed_khz: 4000
  probe_serial: "123456789"
  artifact: build/fw.elf
```

### STM32CubeProgrammer

```yaml
flash:
  backend: cubeprog
  port: SWD
  serial: "003A002233445566778899AA"
  artifact: build/fw.elf
```

### J-Link

```yaml
flash:
  backend: jlink
  device: STM32F407VG
  interface: SWD
  speed_khz: 4000
  serial: "12345678"
  artifact: build/fw.elf
```

### esptool

```yaml
flash:
  backend: esptool
  port: /dev/ttyUSB0
  baud: 921600
  chip: esp32
  offset: "0x10000"
  artifact: build/fw.bin
```

## Reset configuration

Reset is configured separately from flashing.

```yaml
reset:
  method: openocd
```

Supported methods are:

- `openocd`
- `cubeprog`
- `jlink`
- `esptool`
- `none`

BenchCI warns when `reset.method` and `flash.backend` are mismatched in ways that may be confusing.

## Transport configuration

Each node can define multiple named transports.

### UART

```yaml
transports:
  console:
    backend: uart
    port: /dev/ttyUSB0
    baud: 115200
    timeout_ms: 100
```

### Modbus RTU

```yaml
transports:
  fieldbus:
    backend: modbus_rtu
    port: /dev/ttyUSB1
    baud: 9600
    timeout_ms: 500
    default_slave: 1
```

### Modbus TCP

```yaml
transports:
  plc:
    backend: modbus_tcp
    host: 192.168.1.50
    port: 502
    timeout_ms: 1000
    default_slave: 1
```

### CAN

```yaml
transports:
  bus:
    backend: can
    interface: can0
    bitrate: 500000
    timeout_ms: 500
```

## GPIO configuration

GPIO lines are defined by logical name under a node.

### Local Linux GPIO

```yaml
gpio:
  irq:
    backend: local_gpio
    chip: /dev/gpiochip0
    line: 23
    direction: input
    active_high: true
    bias: pull_down
    edge: rising
```

### Remote GPIO

```yaml
gpio:
  reset_n:
    backend: remote_gpio
    host: 192.168.1.60
    port: 8090
    token_env: BENCHCI_AGENT_TOKEN
    chip: /dev/gpiochip0
    line: 19
    direction: output
    active_high: false
```

### Mock GPIO

```yaml
gpio:
  ready:
    backend: mock_gpio
    channel: 1
    direction: input
    active_high: true
```

## GPIO fields

Common GPIO fields:

- `backend`
- `direction`
- `active_high`
- optional `bias`
- optional `edge`

Backend-specific fields:

- `local_gpio`: `chip`, `line`
- `remote_gpio`: `host`, `port`, `token_env`, `chip`, `line`
- `mock_gpio`: `channel`

## Notes

- GPIO lines are referenced from suite steps by logical line name, not by raw chip line number
- `gpio_wait_edge` requires the input line to be configured with `edge`
- `remote_gpio` expects a compatible BenchCI Agent API on the remote machine


## Cloud Mode notes

When a bench is used with `benchci agent cloud`, BenchCI exports a summary of the bench to the backend.

The backend-visible summary includes:

- bench ID
- name and description
- tags
- status
- transports
- flash backends
- GPIO availability
- power resource availability
- node count
- node names

This summary is used by the scheduler, CLI, and dashboard.

Example cloud Agent startup:

```bash
benchci agent cloud \
  --backend https://api.benchci.dev \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --tag uart \
  --agent-name "Lab Agent 01"
```

Keep `bench.yaml` hardware-specific. Workspace ownership, access grants, and plan limits are managed by the backend, not inside the bench file.

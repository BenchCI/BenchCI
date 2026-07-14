# Bench Configuration

Use this page when you are ready to describe a real bench: DUTs, transports, GPIO, flash tools, reset behavior, and artifacts.

---

BenchCI bench configuration is usually named `bench.yaml` in examples, but the filename is not required. Pass the file path with `--bench`; it describes the real execution environment: nodes, transports, GPIO, flashing, reset behavior, defaults, and artifact settings.

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

Schema version field. Use `1` or `"1"` in new bench files.

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
- `dut`
- `flash`
- `reset`
- `transports`
- `gpio`

A node must define at least one of:

- `flash`
- `transports`
- `gpio`

### `dut`

Optional DUT identity metadata ties a run to the exact physical device or fixture slot used during execution.

```yaml
nodes:
  dut:
    kind: mcu
    role: target
    dut:
      hardware_revision: "pcb-rev-b"
      serial_number: "SN-1042"
      asset_id: "QA-DUT-17"
      fixture_slot: "station-a-slot-1"
```

BenchCI copies these fields into `evidence.json`, `evidence.html`, cloud run indexes, dashboard filters, and release coverage matrices.

Optionally, BenchCI can query identity over UART before the first test:

```yaml
    dut:
      hardware_revision: "pcb-rev-b"
      serial_number: "SN-1042"
      self_identification:
        transport: console
        query: "BENCHCI_ID?\n"
        within_ms: 2000
        required: true
```

See [UART DUT Self-Identification](dut-self-identification.md) for the response contract, mismatch behavior, and evidence fields.

### `safety.fault_injection`

Experimental fault steps require explicit bench-owner opt-in and per-target limits. The policy is deny-by-default:

```yaml
safety:
  fault_injection:
    enabled: true
    power:
      - resource: dut_power
        outlet: main
        max_off_ms: 500
    gpio:
      - node: dut
        line: fault
        max_duration_ms: 100
    uart:
      - node: dut
        transport: console
        max_total_bytes: 64
```

See [Controlled Fault Injection](fault-injection.md). Fault injection remains experimental until supported real-bench validation is complete.

### `safety.external`

External simulator and HIL orchestration requires explicit bench-owner opt-in. Use this when BenchCI should trigger a rig you already operate through a wrapper command or HTTP controller.

```yaml
safety:
  external:
    enabled: true
    targets:
      canoe_smoke:
        work_root: /opt/benchci/external/canoe
        output_root: /opt/benchci/external/canoe/out
        argv_prefix:
          - /opt/benchci/wrappers/run-canoe-smoke
        arg_patterns:
          - "[A-Za-z0-9_.-]+"
        max_timeout_ms: 1800000
        max_poll_interval_ms: 10000
        max_logs: 20
        max_artifacts: 50
        max_artifact_total_bytes: 5242880
        lock_key: external:canoe-rig-1
```

- `work_root` is required and must be absolute.
- `output_root` is optional and must be absolute when set; collection defaults to the effective cwd.
- `argv_prefix` is the bench-owned command prefix. Suite args are appended and cannot replace it.
- `arg_patterns` is a list of full-match regexes for suite-supplied args. With no patterns, suite args are rejected.
- `base_url` and `methods` configure HTTP targets. Trigger and poll URLs must stay under `base_url`.
- `lock_key` defaults to `external:<target>`.

Prefer wrapper scripts over bare `ssh` or `curl` prefixes. For SSH-to-Windows HIL hosts, the wrapper should trigger the Windows run and copy reports/artifacts back to the Agent before exiting.

See [HIL Orchestration](hil-orchestration.md).

### `resources`

Optional bench-level shared resources such as power controllers and measurement sources.

Resources keep suite logic hardware-agnostic. For example, a suite can use `power_cycle` without knowing whether the actual implementation is a GPIO relay, HTTP relay, or serial relay command map. A suite can use `measure` without knowing whether the value comes from a SCPI-supported power supply, I2C power monitor, or lab-controller HTTP endpoint.

Common resource kinds:

- `power_controller`
- `measurement`

See [Power Resources](power_resources.md) and [Measurement Resources](measurement_resources.md) for complete examples.

### `artifacts`

Output behavior for generated artifacts.

```yaml
artifacts:
  root_dir: benchci-results
  per_node_dirs: true
```

For local runs, `root_dir` controls where timestamped result directories are written. The CLI `--results-dir` option overrides this value for a specific run.

## Using doctor while editing `bench.yaml`

Before guessing ports or GPIO paths, inspect the machine:

```bash
benchci doctor
```

After editing `bench.yaml`, cross-check it:

```bash
benchci doctor --bench bench.yaml
```

Doctor can help identify:

- serial ports and likely device types
- ST-Link or other USB debug probes
- USB-UART / USB-RS485 adapters
- USB relay devices
- `/dev/gpiochipX` devices
- missing modules needed by resource backends such as `serial`, `gpiod`, or `httpx`
- missing tools such as OpenOCD, STM32CubeProgrammer, J-Link, or esptool

`benchci validate` checks schema and suite/bench compatibility. `benchci doctor --bench` checks the current machine and hardware environment.

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


## Bench-level resources

Bench-level resources describe shared hardware that is not naturally a DUT node transport, such as power controllers and measurement sources.

### Power controller resource

```yaml
resources:
  dut_power:
    kind: power_controller
    driver:
      type: gpio_power
      chip: /dev/gpiochip0
      outlets:
        main: 17
      active_high: true
      initial_state: false
      on_settle_ms: 1000
      off_settle_ms: 250
```

The suite can then use:

```yaml
- power_cycle:
    resource: dut_power
    outlet: main
    off_ms: 1000
    on_settle_ms: 2000
```

### Measurement resource

HTTP measurement example:

```yaml
resources:
  sleep_current:
    kind: measurement
    driver:
      type: http_measurement
      quantity: current
      url: "http://192.168.1.60/measurements/sleep_current"
      value_field: value
      unit_field: unit
```

Raw SCPI measurement example:

```yaml
resources:
  supply_current_raw:
    kind: measurement
    driver:
      type: scpi_measurement
      address: tcp://127.0.0.1:5025
      query: "MEAS:CURR?"
      quantity: current
      unit: A
      timeout_ms: 1000
```

SCPI power-supply measurement example:

```yaml
resources:
  supply_current:
    kind: measurement
    driver:
      type: scpi_power_supply_measurement
      preset: generic
      address: tcp://127.0.0.1:5025
      quantity: current
      timeout_ms: 1000
```

Serial/RS232 instruments can use addresses such as:

```yaml
address: serial:///dev/ttyUSB0
address: serial://COM3
```

USB/VISA-style instruments can use resource strings such as:

```yaml
address: USB0::0x1234::0x5678::INSTR
```

The suite can then use:

```yaml
- measure:
    resource: supply_current
    record_as: sleep_current_a
    unit: A
    expect_less_than: 0.150
```

The important rule is: put hardware implementation details in `bench.yaml`; keep test intent in `suite.yaml`.

## Evidence impact of `bench.yaml`

BenchCI hashes the bench configuration and stores a snapshot in the evidence package:

```text
evidence.json -> bench.config_sha256
inputs/bench.yaml
```

This means a run can later prove which bench definition was used, even if `bench.yaml` changes afterward.

## Flash configuration

A node can define one flash backend.

`.elf` and `.hex` artifacts usually contain their own load addresses. Raw `.bin`
artifacts do not, so configure `flash.address` explicitly when downloading a
binary image.

| Backend | Tool/interface | Downloadable file types | Address handling |
| --- | --- | --- | --- |
| `openocd` | OpenOCD `program` | `.elf`, `.hex`, `.bin` | `.elf`/`.hex` use embedded addresses; `.bin` requires `address`. |
| `cubeprog` | `STM32_Programmer_CLI -w` | `.elf`, `.hex`, `.bin` | `.elf`/`.hex` use embedded addresses; `.bin` requires `address`. |
| `jlink` | SEGGER J-Link Commander | `.elf`, `.hex`, `.bin` | `.elf`/`.hex` use `loadfile`; `.bin` requires `address` and uses `loadbin`. |
| `esptool` | `esptool.py write_flash` | `.bin` single-image downloads | `.bin` requires `address`. |

### OpenOCD

```yaml
flash:
  backend: openocd
  interface_cfg: interface/stlink.cfg
  target_cfg: target/stm32f4x.cfg
  extra_args: []
  adapter_speed_khz: 4000
  probe_serial: "123456789"
  address: "0x08000000"  # Only required for raw .bin artifacts.
  artifact: build/fw.elf
```

### STM32CubeProgrammer

```yaml
flash:
  backend: cubeprog
  port: SWD
  serial: "003A002233445566778899AA"
  address: "0x08000000"  # Only required for raw .bin artifacts.
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
  address: "0x08000000"  # Only required for raw .bin artifacts.
  artifact: build/fw.elf
```

### esptool

```yaml
flash:
  backend: esptool
  port: /dev/ttyUSB0
  baud: 921600
  chip: esp32
  address: "0x10000"
  artifact: build/fw.bin
```

For esptool, `address` is the SPI flash address passed to `write_flash`.

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

BenchCI supports raw classic CAN and CAN FD frames over Linux SocketCAN. BenchCI validates
the interface but does not bring it up or change host bitrate settings.
Setting `fd: true` declares that the interface is configured for CAN FD; individual
suite frames still choose classic CAN or CAN FD with their own `frame.fd` value.

```yaml
transports:
  canbus:
    backend: can
    interface: can0
    bitrate: 500000
    fd: true
    data_bitrate: 2000000
    timeout_ms: 500
    filters:
      - id: 0x500
        mask: 0x700
        extended: false
```

Filters are passed to `python-can` as SocketCAN receive filters when the transport opens.

### I2C

I2C transports use the optional `smbus2` package and are imported lazily, so installations that do not use I2C do not need the dependency.

```yaml
transports:
  board_i2c:
    backend: i2c
    bus: 1
    timeout_ms: 1000
```

Use a stable Linux I2C bus number and confirm wiring before running write steps.

### SPI

SPI transports use the optional `spidev` package and are imported lazily.

```yaml
transports:
  flash_spi:
    backend: spi
    bus: 0
    device: 0
    max_speed_hz: 1000000
    mode: 0
    bits_per_word: 8
```

Set speed and mode conservatively until the fixture wiring and target timing are known.

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
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --tag uart
```

Keep `bench.yaml` hardware-specific. Workspace ownership, access grants, and
usage limits are managed by the backend, not inside the bench file.

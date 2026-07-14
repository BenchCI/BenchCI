# Measurement Resources

Use this page when your test needs to measure physical behavior such as current, voltage, temperature, pressure, timing, or values exposed by a lab controller.

---

BenchCI Measurement adds a simple model:

```text
bench.yaml  -> defines where a measurement comes from
suite.yaml  -> measures it, records it as a metric, and optionally asserts thresholds
```

This moves a run from “the UART log looked correct” toward “the hardware behavior was measured and recorded as evidence.”

## Supported Measurement backends

Current Measurement resource drivers include:

- `http_measurement` for lab controllers, HTTP-enabled instruments, or custom measurement gateways
- `scpi_measurement` for raw SCPI queries over TCP/IP, serial/RS232, or USB/VISA-style instruments
- `scpi_power_supply_measurement` for common SCPI power-supply current and voltage readback
- `i2c_power_monitor` for board-mounted I2C voltage/current monitors such as INA226 and INA260
- `script_measurement` for any local command that outputs a numeric or JSON value
- `serial_measurement` for simple non-SCPI serial sensors

The suite syntax stays the same for all of these backends. The suite says `measure`; the bench file decides where the value comes from.

## Quick decision guide

Use this backend when:

| Backend | Use it for |
|---|---|
| `http_measurement` | Lab controllers or instruments exposed through HTTP/JSON. |
| `scpi_measurement` | Direct raw SCPI queries where you know the command. |
| `scpi_power_supply_measurement` | Common power-supply current/voltage readback without writing raw SCPI. |
| `i2c_power_monitor` | Board-mounted I2C voltage/current monitors (INA226, INA260) on a Raspberry Pi or Linux host. |
| `script_measurement` | Any sensor or tool that can be queried from a shell command and returns a number. |
| `serial_measurement` | Simple serial sensors where you send an optional command and parse a numeric response. |

## HTTP measurement

Use `http_measurement` when a lab controller exposes a measured value over HTTP.

```yaml
resources:
  supply_current:
    kind: measurement
    driver:
      type: http_measurement
      quantity: current
      url: "http://192.168.1.60/measurements/supply_current"
      value_field: value
      unit_field: unit
      unit: A
      timeout_ms: 2000
```

A typical response could be:

```json
{
  "value": 0.042,
  "unit": "A"
}
```

## Raw SCPI measurement

Use `scpi_measurement` when you want BenchCI to send a specific SCPI query and parse the first numeric value from the response.

### TCP/IP SCPI

Use this form for LAN instruments or the local SCPI simulator:

```yaml
resources:
  supply_current:
    kind: measurement
    driver:
      type: scpi_measurement
      address: tcp://127.0.0.1:5025
      query: "MEAS:CURR?"
      quantity: current
      unit: A
      timeout_ms: 1000
```

Start the development simulator:

```bash
python tools/scpi_simulator.py --mode tcp --host 127.0.0.1 --port 5025
```

Then test a single measurement resource:

```bash
benchci measure --bench examples/13-scpi/bench.yaml supply_current
```

### Serial / RS232 SCPI

Use this form for instruments such as affordable programmable power supplies that expose SCPI over RS232 or a USB-to-serial adapter:

```yaml
resources:
  supply_current:
    kind: measurement
    driver:
      type: scpi_measurement
      address: serial:///dev/ttyUSB0
      query: "MEAS:CURR?"
      quantity: current
      unit: A
      timeout_ms: 1000
      baudrate: 9600
      bytesize: 8
      parity: N
      stopbits: 1
```

On macOS, serial devices often look like:

```text
/dev/tty.usbserial-XXXX
/dev/cu.usbserial-XXXX
/dev/tty.usbmodemXXXX
/dev/cu.usbmodemXXXX
```

Example macOS address:

```yaml
address: serial:///dev/tty.usbserial-XXXX
```

On Windows, use:

```yaml
address: serial://COM3
```

To test the serial path without hardware on macOS/Linux:

```bash
python tools/scpi_simulator.py --mode serial-pty
```

The simulator prints a pseudo-terminal path such as:

```text
serial:///dev/ttys004
```

Use that path in `bench.yaml`.

### USB / VISA / USBTMC SCPI

Use this form for USBTMC/VISA instruments supported by PyVISA:

```yaml
resources:
  supply_current:
    kind: measurement
    driver:
      type: scpi_measurement
      address: USB0::0x1234::0x5678::INSTR
      query: "MEAS:CURR?"
      quantity: current
      unit: A
      timeout_ms: 1000
```

Install the optional SCPI dependencies when using USB/VISA-style resources:

```bash
pip install "benchci[scpi]"
```

Common VISA-style addresses include:

```text
USB0::0x1234::0x5678::INSTR
USB::0x1234::0x5678::INSTR
TCPIP0::192.168.1.50::INSTR
ASRL/dev/ttyUSB0::INSTR
ASRL3::INSTR
```

Important: USB/VISA support depends on the operating system, PyVISA backend, permissions, and the instrument's USBTMC/VISA behavior. Validate the exact instrument model before relying on it in production.

## SCPI power-supply measurement

Use `scpi_power_supply_measurement` when you want common power-supply readings without writing raw SCPI queries.

```yaml
resources:
  supply_current:
    kind: measurement
    driver:
      type: scpi_power_supply_measurement
      address: tcp://127.0.0.1:5025
      quantity: current
      timeout_ms: 1000
```

Supported quantities:

```text
current -> MEAS:CURR? -> A
voltage -> MEAS:VOLT? -> V
```

Voltage example:

```yaml
resources:
  supply_voltage:
    kind: measurement
    driver:
      type: scpi_power_supply_measurement
      address: tcp://127.0.0.1:5025
      quantity: voltage
      timeout_ms: 1000
```

## Power-supply presets

Presets provide conservative readback mappings for common power-supply command styles.

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

Supported presets:

```text
generic
owon_sp
rigol_dp_basic
keysight_basic
keysight_e36300_basic
```

Preset behavior is readback-only:

```text
generic current        -> MEAS:CURR?
generic voltage        -> MEAS:VOLT?
owon_sp current        -> MEAS:CURR?
owon_sp voltage        -> MEAS:VOLT?
rigol_dp_basic current -> :MEAS:CURR? CH1
rigol_dp_basic voltage -> :MEAS:VOLT? CH1
keysight_basic current -> MEAS:CURR? CH1
keysight_basic voltage -> MEAS:VOLT? CH1
```

For channel-aware presets, configure `channel`:

```yaml
resources:
  supply_ch1_current:
    kind: measurement
    driver:
      type: scpi_power_supply_measurement
      preset: rigol_dp_basic
      address: tcp://192.168.1.50:5025
      channel: 1
      quantity: current
      timeout_ms: 1000
```

When no channel is configured, channel-aware presets omit the channel argument and query the currently selected output where the instrument supports that behavior.

Use raw `scpi_measurement` when your instrument needs a command not covered by the conservative preset mapping.

## I2C power monitor

Use `i2c_power_monitor` for board-mounted monitors such as INA226 or INA260 connected to the agent host over I2C.

```yaml
resources:
  dut_voltage:
    kind: measurement
    driver:
      type: i2c_power_monitor
      chip: ina260
      bus: 1
      address: 0x40
      quantity: voltage
      unit: V
```

For INA226 current measurements, the calibration LSB must be provided because the scaling depends on the external shunt resistor:

```yaml
resources:
  dut_current:
    kind: measurement
    driver:
      type: i2c_power_monitor
      chip: ina226
      bus: 1
      address: 0x40
      quantity: current
      unit: A
      current_lsb_a: 0.001
```

Supported `chip` values: `ina226`, `ina228`, `ina260`, `generic_i2c_power_monitor`.

Supported `quantity` values: `voltage`, `current`, `power`.

This driver imports `smbus2` (or `smbus`) on use. If the package is not installed or the I2C bus is unavailable, BenchCI fails with an actionable error. Install smbus2 and enable the I2C bus on the host before using this backend.

```bash
benchci doctor --bench bench.yaml
```

Doctor checks for smbus2 and reports if it is missing.

## Script measurement

Use `script_measurement` when a sensor, tool, or data source can be queried from a shell command.

The command must exit with code 0 and write a numeric value or a JSON object to stdout.

**Plain numeric output:**

```yaml
resources:
  board_temp:
    kind: measurement
    driver:
      type: script_measurement
      command: "./read_temp.py"
      quantity: temperature
      unit: C
      timeout_ms: 2000
```

The command can output `23.5` or `23` directly.

**JSON output:**

```yaml
resources:
  sensor:
    kind: measurement
    driver:
      type: script_measurement
      command: "./sensor.py --json"
      value_json_path: value
      unit_json_path: unit
      quantity: voltage
      timeout_ms: 2000
```

If the command outputs `{"value": 3.29, "unit": "V"}`, BenchCI reads the `value` field and uses `unit` from the response.

`value_json_path` and `unit_json_path` support dot notation for nested objects, for example `data.measurements.voltage`.

## Serial measurement

Use `serial_measurement` for simple non-SCPI serial sensors where you send an optional command and read a numeric response line.

```yaml
resources:
  flow_sensor:
    kind: measurement
    driver:
      type: serial_measurement
      port: /dev/ttyUSB3
      baud: 115200
      command: "READ?\n"
      response_regex: "VALUE=([0-9.]+)"
      quantity: flow
      unit: L/min
      timeout_ms: 1000
```

If no `response_regex` is provided, BenchCI parses the first floating-point number in the response line.

For named capture groups, use `(?P<value>...)` in the regex and BenchCI reads the `value` group.

This backend requires `pyserial`, which is included in the standard BenchCI installation.

## Measure step

Use `measure` to read a measurement resource, store the value, and optionally check a threshold.

```yaml
- measure:
    resource: supply_current
    record_as: sleep_current_a
    unit: A
    expect_less_than: 0.150
```

The recorded metric can appear in `results.json`, `evidence.json`, `evidence.html`, CLI output, and dashboard run detail where supported.

## Assert metric step

Use `assert_metric` when you want to check a metric captured earlier in the same run.

```yaml
- assert_metric:
    name: sleep_current_a
    expect_less_than_or_equal: 0.100
```

Supported assertion styles include:

```yaml
expect_less_than: 0.150
expect_less_than_or_equal: 0.150
expect_greater_than: 3.0
expect_greater_than_or_equal: 3.0
expect_equal: 3.3
tolerance: 0.05
```

Use `tolerance` with `expect_equal` when exact equality is unrealistic.

## One-off measurement debugging

Use `benchci measure` before writing full suite thresholds:

```bash
benchci measure --bench bench.yaml supply_current
benchci measure --bench bench.yaml supply_current --json
benchci measure --bench bench.yaml supply_current --repeat 10 --interval-ms 500
```

This checks whether BenchCI can open the instrument, send the query, parse the response, and write the measurement log.

## Example: boot then verify sleep current

```yaml
version: "1"

suite:
  name: low_power_smoke

tests:
  - name: boot_and_sleep_current
    steps:
      - power_cycle:
          resource: dut_power
          outlet: main
          off_ms: 1000
          on_settle_ms: 2000

      - expect_uart:
          node: dut
          transport: console
          contains: "READY"
          within_ms: 5000

      - send_uart:
          node: dut
          transport: console
          data: "SLEEP
"

      - measure:
          resource: supply_current
          record_as: sleep_current_a
          unit: A
          expect_less_than: 0.150

      - assert_metric:
          name: sleep_current_a
          expect_less_than_or_equal: 0.150
```

## Logs and evidence

Measurement resources write logs under the resource artifact directory:

```text
benchci-results/<run>/logs/resources/<resource>/measurement.log
```

For SCPI-backed measurements, the log can include:

```text
SCPI_MEASURE_BEGIN
SCPI_TX
SCPI_RX
SCPI_PARSE_OK
SCPI_MEASURE_END
SCPI_ERROR
```

SCPI measurement payloads can include:

```json
{
  "resource": "supply_current",
  "value": 0.042,
  "unit": "A",
  "quantity": "current",
  "backend": "scpi_power_supply_measurement",
  "preset": "generic",
  "address": "tcp://127.0.0.1:5025",
  "query": "MEAS:CURR?",
  "raw_response": "0.042\n"
}
```

Measurements are especially useful for QA and release review because the evidence can show not only pass/fail but also the measured value.

Example:

```text
sleep_current_a = 0.042 A
limit           = 0.150 A
result          = passed
```

That is more useful than a generic “low power test passed” message.

## Scope and limitations

SCPI support focuses on measurement readback:

```text
query -> raw response -> parsed float -> metric -> assertion/evidence
```

It does not yet provide full instrument control for every model. In particular, current model does not attempt to provide universal support for:

- output on/off control
- voltage setpoint control
- current-limit configuration
- protection setup
- waveform capture
- model autodetection

SCPI command sets vary by vendor and model. Presets are intended as practical starting points, not as a guarantee that every command on every instrument behaves identically.

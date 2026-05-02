# Measurement Resources

Use this page when your test needs to measure physical behavior such as current, voltage, temperature, pressure, timing, or values exposed by a lab controller.

---

BenchCI Measurement v1 adds a simple model:

```text
bench.yaml  -> defines where a measurement comes from
suite.yaml  -> measures it, records it as a metric, and optionally asserts thresholds
```

This moves a run from “the UART log looked correct” toward “the hardware behavior was measured and recorded as evidence.”

## Supported Measurement v1 backends

Current Measurement v1 resource drivers include:

- `mock_measurement` for examples, demos, and tests
- `http_measurement` for lab controllers, HTTP-enabled instruments, or custom measurement gateways

Future backends can add direct SCPI power supplies, USB multimeters, oscilloscopes, logic analyzers, or company-specific lab tools without changing suite syntax.

## Mock measurement

```yaml
resources:
  sleep_current:
    kind: measurement
    driver:
      type: mock_measurement
      quantity: current
      value: 0.042
      unit: A
```

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
          data: "SLEEP\n"

      - measure:
          resource: sleep_current
          record_as: sleep_current_a
          unit: A
          expect_less_than: 0.150

      - assert_metric:
          name: sleep_current_a
          expect_less_than_or_equal: 0.150
```

## Evidence value

Measurements are especially useful for QA and release review because the evidence can show not only pass/fail but also the measured value.

Example:

```text
sleep_current_a = 0.042 A
limit           = 0.150 A
result          = passed
```

That is more useful than a generic “low power test passed” message.

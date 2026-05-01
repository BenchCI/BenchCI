# Suite Configuration

Use this page when you are ready to define the actual hardware test logic: steps, expectations, protocols, GPIO checks, power cycles, and validation rules.

---

BenchCI test suites are stored in `suite.yaml`. A suite defines named tests and ordered steps.

## Top-level structure

```yaml
version: "1"

suite:
  name: smoke
  description: Optional suite description

tests:
  - name: boot_ok
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "BOOT OK"
          within_ms: 3000
```

## Main sections

### `version`

Schema version string.

### `suite`

Suite metadata.

```yaml
suite:
  name: smoke
  description: First working suite
```

### `tests`

Ordered list of test cases.

Each test has:

- `name`
- `steps`

## Example suite

```yaml
version: "1"

suite:
  name: stm32_smoke

tests:
  - name: boot_ok
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "[BOOT] OK"
          within_ms: 3000

  - name: ping
    steps:
      - send_uart:
          node: dut
          transport: console
          data: "PING\n"

      - expect_uart:
          node: dut
          transport: console
          contains: "PONG"
          within_ms: 1000

  - name: irq_test
    steps:
      - gpio_wait_edge:
          node: dut
          line: irq
          edge: rising
          within_ms: 2000
```

## Optional traceability metadata

Traceability fields are optional. Keep simple suites simple. Add these fields when a test should be connected to requirements, test cases, risks, releases, or evidence reports.

Suite-level metadata can include:

```yaml
suite:
  name: stm32_smoke
  description: Basic real-hardware smoke test
  version: "1.0.0"
  release_id: "fw-0.3.5"
  requirement_ids:
    - REQ-BOOT-001
  risk_ids:
    - RISK-BOOT-001
  tags:
    - smoke
    - hardware-ci
```

Each test can include:

```yaml
tests:
  - name: boot_ok
    test_case_id: TC-BOOT-001
    requirement_ids:
      - REQ-BOOT-001
    risk_ids:
      - RISK-BOOT-001
    tags:
      - boot
      - uart
    steps:
      - expect_uart:
          node: dut
          transport: console
          contains: "BOOT OK"
          within_ms: 3000
```

These fields are copied into `results.json`, `evidence.json`, and `evidence.html` so a run can show which requirements, test cases, and risks were covered.

A useful mental model is:

```text
Risk -> Requirement -> Test case -> BenchCI run evidence
```

Recommended simple ID format:

```text
REQ-BOOT-001
TC-BOOT-001
RISK-BOOT-001
```

## Step types

BenchCI currently supports these step types:

- `reset`
- `sleep_ms`
- `flash`
- `send_uart`
- `expect_uart`
- `modbus_read_holding_registers`
- `modbus_write_single_register`
- `modbus_read_coils`
- `modbus_write_single_coil`
- `gpio_set`
- `gpio_get`
- `gpio_expect`
- `gpio_wait_edge`
- `send_can`
- `expect_can`
- `power_set`
- `power_cycle`

## Reset step

```yaml
- reset:
    node: dut
```

Resets the selected node using the node’s configured `reset.method`.

## Sleep step

```yaml
- sleep_ms: 100
```

Pauses execution for the requested number of milliseconds.

## Flash step

```yaml
- flash:
    node: dut
```

Optional step-level artifact override:

```yaml
- flash:
    node: dut
    artifact: build/alternate.elf
```

Artifact resolution order is:

1. step artifact override
2. CLI `--artifact`
3. `node.flash.artifact` from `bench.yaml`

## UART steps

### Send text

```yaml
- send_uart:
    node: dut
    transport: console
    data: "PING\n"
```

### Expect text by substring

```yaml
- expect_uart:
    node: dut
    transport: console
    contains: "PONG"
    within_ms: 1000
```

### Expect text by regex

```yaml
- expect_uart:
    node: dut
    transport: console
    regex: "FW:[0-9.]+"
    within_ms: 1000
```

`expect_uart` must define exactly one of:

- `contains`
- `regex`

## Modbus steps

### Read holding registers

```yaml
- modbus_read_holding_registers:
    node: plc
    transport: fieldbus
    slave: 1
    address: 100
    count: 2
    expect: [123, 456]
```

### Write single register

```yaml
- modbus_write_single_register:
    node: plc
    transport: fieldbus
    slave: 1
    address: 100
    value: 42
```

### Read coils

```yaml
- modbus_read_coils:
    node: plc
    transport: fieldbus
    slave: 1
    address: 0
    count: 2
    expect: [true, false]
```

### Write single coil

```yaml
- modbus_write_single_coil:
    node: plc
    transport: fieldbus
    slave: 1
    address: 0
    value: true
```

## GPIO steps

### Set logical output value

```yaml
- gpio_set:
    node: dut
    line: reset_n
    value: false
```

### Read logical input value

```yaml
- gpio_get:
    node: dut
    line: ready
```

With expectation:

```yaml
- gpio_get:
    node: dut
    line: ready
    expect: true
```

### Wait for logical value

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

Allowed edges are:

- `rising`
- `falling`
- `both`

## CAN steps

### Send frame

```yaml
- send_can:
    node: dut
    transport: bus
    frame:
      id: 257
      extended: false
      data: "01 02 0A FF"
```

### Expect frame

```yaml
- expect_can:
    node: dut
    transport: bus
    frame:
      id: 513
      extended: false
      data: "AA BB"
    within_ms: 1000
```

## Timeout behavior

Steps that need a timeout can either define `within_ms` explicitly or inherit it from:

```yaml
defaults:
  timeouts:
    within_ms: 1000
```

## Validation rules

BenchCI cross-validates the suite against the bench before execution. For example:

- referenced nodes must exist
- referenced transports must exist on the selected node
- transport backend must match the step type
- referenced GPIO logical line names must exist
- flashing requires the node to define a flash backend

This catches many configuration mistakes before hardware execution starts.


## Power steps

If your bench defines a supported power resource, suites can control outlets.

### Set power state

```yaml
- power_set:
    resource: dut_power
    outlet: dut
    state: true
```

### Power cycle

```yaml
- power_cycle:
    resource: dut_power
    outlet: dut
    off_ms: 500
    on_settle_ms: 2000
```

Power steps are useful for realistic hardware reset, boot recovery, and CI smoke tests.
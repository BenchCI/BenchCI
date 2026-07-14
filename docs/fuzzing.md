# Protocol Fuzzing

BenchCI supports bounded protocol fuzzing as normal `suite.yaml` steps.

Current version is intentionally scoped to hardware CI robustness checks, not open-ended fuzz farms. A fuzz step runs a fixed number of generated cases, or stops at a duration limit, records the seed and every case, then writes replayable evidence into the normal run artifacts.

Supported protocols:

- UART
- CAN / CAN FD over SocketCAN
- Modbus RTU
- Modbus TCP

---

## When to Use It

Use fuzzing after your smoke or regression flow already works.

Good uses:

- exercise a command parser with unexpected UART payloads
- send bounded CAN frame ranges to check ECU robustness
- probe Modbus register/address ranges without losing replayability
- add a short robustness gate to nightly or pre-release hardware runs

Avoid using fuzzing as a replacement for regression tests. Keep explicit checks for known behavior, then add fuzzing to find parser lockups, crashes, resets, watchdog trips, or transport failures.

---

## Evidence and Replay

Each fuzz step records:

- protocol
- seed
- test index
- step index
- configured iterations
- cases executed
- first failing case
- JSONL fuzz log path

The data appears in:

- `results.json` under `fuzz`
- each test result under `fuzz`
- `evidence.json` under `fuzz`
- `evidence.html`
- artifact ZIPs and `manifest.json`

Fuzz case logs are written under:

```text
logs/fuzz/<test-name>-step<step-index>-<protocol>.jsonl
```

To replay a failure, copy the recorded `seed`, `step_index`, and `case_index` from `results.json` or `evidence.json`, then rerun the same suite with the same seed and a tight iteration window. For example, if case 37 failed:

```yaml
- fuzz_uart:
    node: dut
    transport: console
    seed: 12648430
    iterations: 37
    stop_on_failure: true
    mode: ascii
    min_length: 0
    max_length: 64
    fail_contains: "ASSERT"
```

The generated sequence is deterministic for a given step configuration and seed. Keep the same generator-relevant fields when replaying: protocol, ranges, mode, dictionary, payload lengths, IDs, addresses, operations, and seed.

---

## UART Fuzzing

```yaml
- fuzz_uart:
    node: dut
    transport: console
    seed: 12648430
    iterations: 200
    max_duration_ms: 30000
    mode: ascii
    min_length: 0
    max_length: 64
    dictionary:
      - PING
      - STATUS
      - HELP
    suffix: "\n"
    fail_contains: "ASSERT"
    stop_on_failure: true
```

Useful fields:

- `mode`: `ascii` or `hex`
- `min_length` / `max_length`: generated payload byte or character bounds
- `dictionary`: known commands mixed into generated ASCII payloads
- `suffix`: appended to ASCII payloads, commonly `"\n"`
- `fail_contains` / `fail_regex`: recent UART output that marks a failed case
- `heartbeat_command`: optional command sent after each fuzz payload
- `heartbeat_expect_contains` / `heartbeat_expect_regex`: optional liveness oracle
- `heartbeat_within_ms`: heartbeat timeout

Heartbeat example:

```yaml
- fuzz_uart:
    node: dut
    transport: console
    seed: 222
    iterations: 50
    mode: ascii
    min_length: 1
    max_length: 32
    suffix: "\n"
    heartbeat_command: "PING\n"
    heartbeat_expect_contains: "PONG"
    heartbeat_within_ms: 1000
```

---

## CAN Fuzzing

```yaml
- fuzz_can:
    node: ecu
    transport: canbus
    seed: 49374
    iterations: 200
    max_duration_ms: 30000
    id_min: 0x100
    id_max: 0x1ff
    extended: false
    fd: false
    min_data_length: 0
    max_data_length: 8
    stop_on_failure: true
```

For CAN FD:

```yaml
- fuzz_can:
    node: ecu
    transport: canbus
    seed: 88
    iterations: 100
    fd: true
    bitrate_switch: true
    min_data_length: 0
    max_data_length: 64
```

You can add a response oracle with the same frame matching fields used by `expect_can`:

```yaml
- fuzz_can:
    node: ecu
    transport: canbus
    seed: 77
    iterations: 25
    id_min: 0x500
    id_max: 0x50f
    expect_response:
      id: 0x580
      data: "AA"
      allow_extra_data: true
    response_within_ms: 100
```

---

## Modbus Fuzzing

Modbus fuzzing treats BenchCI Modbus transport exception responses as recordable protocol outcomes when `allow_protocol_exceptions` is `true`. This uses BenchCI's typed `ModbusProtocolException`, raised by the RTU/TCP transports when a pymodbus response reports `isError()`. Arbitrary string matching is not used for new transports.

```yaml
- fuzz_modbus:
    node: gateway
    transport: api
    slave: 1
    seed: 195936478
    iterations: 200
    max_duration_ms: 30000
    operations:
      - read_holding_registers
      - write_single_register
    address_min: 0
    address_max: 127
    count_min: 1
    count_max: 4
    value_min: 0
    value_max: 65535
    allow_protocol_exceptions: true
```

Supported operations:

- `read_holding_registers`
- `write_single_register`
- `read_coils`
- `write_single_coil`

`allow_protocol_exceptions: true` records normal Modbus exception responses as fuzz outcomes instead of failing the step. Transport errors, unexpected client failures, and disallowed protocol exceptions still fail the fuzz campaign.

---

## Presets

The CLI and dashboard Config Builder include starter fuzz presets:

```bash
benchci init --preset uart-fuzz
benchci init --preset can-fuzz
benchci init --preset modbus-rtu-fuzz
benchci init --preset modbus-tcp-fuzz
```

These are conservative templates. Adjust ranges, iterations, seeds, and oracles for your firmware and bench.

---

## CI Guidance

Keep fuzzing bounded:

- use explicit `iterations`
- set `max_duration_ms`
- start with narrow payload, ID, or address ranges
- keep `stop_on_failure: true` for CI gates
- record a fixed seed for release evidence or use generated seeds for exploratory runs

A practical pattern is:

```text
pull request: smoke/regression only
nightly: regression + short fuzz campaigns
release candidate: regression + focused fuzz campaigns with fixed seeds
```

Fuzzing finds robustness issues. It does not prove protocol correctness by itself; keep explicit regression tests for required behavior.

# Power Resources

Use this page when your bench needs to turn DUT power on/off, power-cycle a board, or hide relay/vendor details behind stable BenchCI suite steps.

---

BenchCI treats power as a **bench-level resource**. The suite says what should happen, such as `power_cycle`, while `bench.yaml` describes how the lab hardware performs it.

```text
suite.yaml  -> power_cycle dut_power.main
bench.yaml  -> GPIO relay, HTTP relay, USB serial relay, or another backend
```

This keeps test logic readable and avoids writing vendor-specific relay commands directly in test suites.

## Supported Power v2 backends

Current Power v2 resource drivers include:

- `mock_power` for demos, tests, and dry-runs
- `gpio_power` for local Linux GPIO controlled relays or load switches
- `http_relay` for LAN relays, Shelly-style devices, or internal lab controllers
- `usb_relay_serial` with `vendor: generic` and `model: command_map` for serial relay boards

BenchCI intentionally avoids exposing one-off relay brands as top-level suite concepts. For example, an LCUS-style relay should be configured as a generic serial command map in `bench.yaml`, while the suite still uses `power_set` or `power_cycle`.

## Power resource shape

Power resources live under `resources` in `bench.yaml`:

```yaml
resources:
  dut_power:
    kind: power_controller
    driver:
      type: mock_power
      outlets:
        main: false
```

The resource name is `dut_power`; the outlet name is `main`. Suite steps reference those logical names.

## Mock power

Use `mock_power` for examples, tests, and demos where no real relay is connected.

```yaml
resources:
  dut_power:
    kind: power_controller
    driver:
      type: mock_power
      outlets:
        main: false
```

## GPIO power

Use `gpio_power` when a Linux machine, Raspberry Pi, or similar controller drives a relay, MOSFET, or load switch through `/dev/gpiochipX`.

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

Use `active_high: false` when the relay input is active-low. Suites always use logical states: `true` means power should be on/active, regardless of the electrical level.

## HTTP relay

Use `http_relay` for relay boards or lab controllers that expose simple HTTP endpoints.

```yaml
resources:
  dut_power:
    kind: power_controller
    driver:
      type: http_relay
      outlets:
        main: "1"
      on_url: "http://192.168.1.50/relay/{channel}/on"
      off_url: "http://192.168.1.50/relay/{channel}/off"
      get_url: "http://192.168.1.50/relay/{channel}/state"
      method: GET
      timeout_ms: 2000
```

`{channel}` is replaced with the outlet mapping value. In the example above, `main` maps to channel `1`.

If the backend cannot read state, omit `get_url` and avoid `power_expect`.

## Generic serial relay command map

Use `usb_relay_serial` with `vendor: generic` and `model: command_map` for serial relay boards where the ON/OFF commands are known.

```yaml
resources:
  dut_power:
    kind: power_controller
    driver:
      type: usb_relay_serial
      vendor: generic
      model: command_map
      port: /dev/ttyUSB1
      baud: 9600
      timeout_ms: 500
      outlets:
        main: "1"
      on_commands:
        "1": "A0 01 01 A2"
      off_commands:
        "1": "A0 01 00 A1"
      on_settle_ms: 1000
      off_settle_ms: 250
```

This is also how LCUS-style relay boards should be represented. BenchCI does not need a separate LCUS-specific suite step or first-class backend.

## Suite steps

### Set power

```yaml
- power_set:
    resource: dut_power
    outlet: main
    state: true
```

### Power-cycle

```yaml
- power_cycle:
    resource: dut_power
    outlet: main
    off_ms: 1000
    on_settle_ms: 2000
```

### Expect/read power state

```yaml
- power_expect:
    resource: dut_power
    outlet: main
    state: true
```

`power_expect` requires a backend that supports readback or safe state tracking. If a serial relay cannot report state, BenchCI should fail clearly instead of pretending to know the hardware state.

## Why this model matters

The test suite should say:

```yaml
- power_cycle:
    resource: dut_power
    outlet: main
```

It should not say:

```text
send A0 01 00 A1 to /dev/ttyUSB1, sleep, then send A0 01 01 A2
```

Vendor-specific details belong in `bench.yaml`. Test intent belongs in `suite.yaml`.

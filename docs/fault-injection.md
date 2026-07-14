# Controlled Fault Injection (Experimental)

BenchCI 1.4 adds experimental power, GPIO, and malformed-UART-byte fault steps. These steps reuse configured bench controllers and require an explicit bench-owner safety policy.

Do not describe these steps as precision electrical fault generation. Relay latency, GPIO scheduling, USB adapters, operating-system timing, and DUT circuitry affect the physical fault observed by the device.

General availability requires BenchCI validation on a supported power controller, Linux GPIO output, and UART recovery workflow. Until that validation is recorded, treat this surface as experimental.

## Bench safety policy

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

Every fault target must be listed explicitly. Suite validation rejects disabled, unknown, or over-limit targets before hardware execution.

Absolute limits are:

- 60 seconds for power-off or GPIO pulse duration
- five minutes for recovery observation
- 4 KiB total malformed UART bytes

## UART recovery oracle

Each fault step requires a bounded UART recovery check:

```yaml
recovery:
  type: uart
  node: dut
  transport: console
  send: "PING\n"
  expect_contains: "PONG"
  within_ms: 5000
  retry_interval_ms: 250
  watchdog_contains: "WATCHDOG"
```

BenchCI repeats the health command until the expected response appears or the recovery window expires. `watchdog_contains` records whether an observable watchdog message appeared; it does not infer watchdog behavior when firmware emits no such signal.

## Power glitch

```yaml
- fault_inject_power_glitch:
    resource: dut_power
    outlet: main
    off_ms: 100
    recovery:
      type: uart
      node: dut
      transport: console
      send: "PING\n"
      expect_contains: "PONG"
      within_ms: 5000
      retry_interval_ms: 250
```

BenchCI always attempts to restore power in a `finally` path.

## GPIO glitch

```yaml
- fault_inject_gpio_glitch:
    node: dut
    line: fault
    pulse_value: true
    restore_value: false
    duration_ms: 20
    recovery:
      type: uart
      node: dut
      transport: console
      send: "PING\n"
      expect_contains: "PONG"
```

The GPIO line must be configured as an output. An explicit `restore_value` is required, and BenchCI attempts restoration even when injection or recovery fails.

## Malformed UART byte injection

```yaml
- fault_inject_uart_noise:
    node: dut
    transport: console
    data: "00 FF 55 AA"
    repeat: 1
    inter_write_delay_ms: 0
    recovery:
      type: uart
      node: dut
      transport: console
      send: "PING\n"
      expect_contains: "PONG"
```

This sends malformed or unexpected bytes through the UART transport. It does not generate analog noise, framing errors, voltage disturbances, or precision waveforms.

## Results and failures

Evidence records the fault type, target, bounded parameters, injection/restoration timestamps, recovery result, recovery time, watchdog observation, and related logs.

Failure categories are:

- `FAULT_INJECTION_FAILED`
- `FAULT_RESTORE_FAILED`
- `FAULT_RECOVERY_FAILED`

Fault summaries appear in per-test results, `evidence.json`, `evidence.html`, dashboard run detail, JUnit/CTRF exports, and release reports.

CAN bus-off injection is not included. It remains deferred until BenchCI has a privileged, adapter-aware SocketCAN design with reliable interface restoration.

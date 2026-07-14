# UART DUT Self-Identification

BenchCI can ask a DUT to report its identity once after bench transports start and before the first test executes. This supplements the static `dut` fields in `bench.yaml`; it does not replace fixture or asset-management controls.

## Bench configuration

```yaml
nodes:
  dut:
    kind: mcu
    dut:
      hardware_revision: rev-b
      serial_number: SN-42
      self_identification:
        transport: console
        query: "BENCHCI_ID?\n"
        within_ms: 2000
        required: true
    transports:
      console:
        backend: uart
        port: /dev/ttyUSB0
        baud: 115200
```

The selected transport must use `backend: uart`.

## Firmware response

The firmware must return one line prefixed with `BENCHCI_ID:` followed by a JSON object:

```text
BENCHCI_ID:{"schema_version":"1","hardware_revision":"rev-b","serial_number":"SN-42","asset_id":"A-17","fixture_slot":"slot-2"}
```

Recognized fields are:

- `hardware_revision`
- `serial_number`
- `asset_id`
- `fixture_slot`

At least one recognized field must be non-empty. The complete response line is limited to 4 KiB.

When a field exists in both `bench.yaml` and the DUT response, the values must match exactly after surrounding whitespace is removed. A mismatch fails the run before test execution with `DUT_IDENTITY_MISMATCH`.

If the response is missing or malformed:

- `required: true` fails the run with `DUT_IDENTITY_QUERY_FAILED`.
- `required: false` continues with configured identity and records an evidence warning.

## Evidence handling

BenchCI records:

- merged configured and observed identity fields
- identity source and verification status
- selected transport and query timestamp
- configured and observed recognized fields
- SHA256 of the response line

BenchCI does not persist the raw response line in the structured identity evidence. UART transport logs may still contain firmware output and should be handled as internal engineering artifacts.

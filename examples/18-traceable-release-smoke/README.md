# Traceable Release Smoke Example

This example is designed for release and QA conversations. It shows how a BenchCI suite can connect:

```text
Risk -> Requirement -> Test case -> Firmware build -> Physical DUT -> Real run -> Evidence -> Release review
```

Use it when you want a small, realistic template for:

- release-candidate smoke testing;
- requirement/test/risk metadata in `suite.yaml`;
- SDLC/test-intent tags such as `regression`, `system`, `acceptance`, `confirmation`, and `maintenance`;
- DUT identity metadata in `bench.yaml`;
- evidence reports and release bundles;
- explaining traceability to QA, validation, or regulated embedded teams.

Before running, replace the flashing backend, firmware path, serial port, expected UART strings, and DUT identity fields for your hardware.

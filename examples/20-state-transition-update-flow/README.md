# State Transition Update Flow Example

This example shows how to express firmware state transition testing in a BenchCI suite.

The scenario is a firmware update flow:

```text
IDLE -> DOWNLOADING -> VERIFYING -> INSTALLING -> REBOOTING -> READY
```

The suite uses UART commands and expected responses as placeholders. `/dev/null` is used in `bench.yaml` so the files can be validated without a physical device; replace it with your DUT UART and real command protocol before running.

Use this example when you want to explain:

- valid transition coverage;
- invalid transition checks;
- state-oriented test case IDs and tags;
- release evidence for update or provisioning workflows.

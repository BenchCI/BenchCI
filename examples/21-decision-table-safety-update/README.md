# Decision Table Safety Update Example

This example shows how to express decision table testing in a BenchCI suite.

The scenario is firmware update eligibility. The update should be allowed only when:

- battery is OK;
- firmware is signed;
- device is idle.

Each test case represents a decision rule. The UART commands and responses are placeholders; replace them with your product's real update eligibility command before running.

Use this example when you want to explain:

- black-box test design from combinations of conditions;
- negative and positive rule coverage;
- safety or release-gate evidence;
- why decision tables are useful for firmware logic with multiple inputs.

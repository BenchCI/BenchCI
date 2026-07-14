# Boundary Value Threshold Example

This example shows how to express boundary value analysis in a BenchCI suite.

The scenario is a DUT voltage safety range of **3.0 V to 4.2 V**. The suite uses deterministic mock measurement resources so the YAML can be validated without physical instruments. On a real bench, replace the mock resources with an SCPI, HTTP, I2C power-monitor, script, or serial measurement resource.

The example demonstrates 3-value BVA around both boundaries:

```text
2.9, 3.0, 3.1, 4.1, 4.2, 4.3
```

Use this example when you want to explain:

- black-box test design from acceptance thresholds;
- boundary value tags in `suite.yaml`;
- measurement evidence for safety or non-functional checks;
- how BenchCI records representative test cases without proving the test design is complete.

Before running on hardware, adapt the measurement resource, voltage stimulus/control method, thresholds, and acceptance criteria for your DUT.

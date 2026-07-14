# JUnit XML and CTRF Import Guide

BenchCI can export run results as standard JUnit XML or CTRF JSON so you can import them into your existing test reporting and defect-tracking tools.

## GitHub Actions Integration

Export results with the CLI and publish them to any JUnit-aware action:

```yaml
- name: Export JUnit results
  if: always()
  run: |
    benchci runs export $RUN_ID --format junit-xml --output benchci-results.xml

- name: Publish test results
  if: always()
  uses: mikepenz/action-junit-report@v4
  with:
    report_paths: benchci-results.xml
    check_name: BenchCI Hardware Tests
```

To export CTRF JSON instead:

```bash
benchci runs export $RUN_ID --format ctrf --output benchci-results.ctrf.json
```

---

## Jira Xray

Export the CTRF JSON and convert to Xray's import format using the [ctrf-xray-reporter](https://github.com/ctrf-io/ctrf-xray-reporter), or import the JUnit XML directly via Xray's **Import Execution Results** endpoint:

```bash
curl -H "Authorization: Bearer $XRAY_TOKEN" \
  -H "Content-Type: application/xml" \
  --data-binary @benchci-results.xml \
  "https://xray.cloud.getxray.app/api/v1/import/execution/junit"
```

Each exported JUnit file includes BenchCI `benchci.measurement.*` properties on the `<testsuite>`, while each `<testcase>` carries `test_case_id` / `requirement_ids` from the evidence trace so Xray can link results to existing test issues automatically.

---

## TestRail

TestRail's JUnit importer reads `<testcase classname="..." name="..."/>`. BenchCI sets `classname` to the suite name and `name` to the test case name. Map them to TestRail cases manually or via the TestRail CLI:

Import via the TestRail CLI:

```bash
trcli -y -h https://your-instance.testrail.io \
  --username $TESTRAIL_USER --key $TESTRAIL_KEY \
  parse_junit --project-id 1 \
  --file benchci-results.xml
```

---

## Azure DevOps Test Plans

Use the **Publish Test Results** task:

```yaml
- task: PublishTestResults@2
  inputs:
    testResultsFormat: JUnit
    testResultsFiles: benchci-results.xml
    testRunTitle: "BenchCI Hardware CI"
    mergeTestResults: true
  condition: always()
```

---

## Allure

Save the JUnit XML to the `allure-results/` directory and Allure will pick it up automatically on the next report generation:

```bash
cp benchci-results.xml allure-results/benchci-$(date +%s).xml
allure generate allure-results --clean
```

---

## Measurement Properties in JUnit

BenchCI embeds hardware measurement data as `<property>` elements on the `<testsuite>` node:

```xml
<testsuite name="BenchCI run-abc123">
  <properties>
    <property name="benchci.measurement.0.name" value="supply_current"/>
    <property name="benchci.measurement.0.resource" value="psu"/>
    <property name="benchci.measurement.0.value" value="142.5"/>
    <property name="benchci.measurement.0.unit" value="mA"/>
    <property name="benchci.measurement.0.assertion" value="pass"/>
    <!-- … more measurements … -->
  </properties>
  <!-- testcases … -->
</testsuite>
```

These properties survive round-trip import into tools that preserve JUnit properties (Allure, Xray, most CI dashboards).

# BenchCI Documentation

BenchCI is a hardware validation platform for embedded systems.

Run real hardware tests from CI using the same workflow software teams use for automated pipelines.

BenchCI lets you define a bench in `bench.yaml`, define tests in `suite.yaml`, and execute those tests locally, through your own BenchCI Agent, or through BenchCI Cloud benches.

## What BenchCI can do today

BenchCI currently provides:

- declarative hardware testing using `bench.yaml` + `suite.yaml`
- automated firmware flashing
- protocol-aware validation over UART, Modbus RTU, Modbus TCP, and CAN
- GPIO automation through `local_gpio`, `remote_gpio`, or `mock_gpio`
- relay-backed power control workflows
- local execution on the hardware machine
- remote execution through your own BenchCI Agent
- shared/private hardware execution through BenchCI Cloud
- workspace-based users, benches, runs, and artifacts
- dashboard visibility for workspace health, benches, runs, events, failures, and artifacts
- structured artifacts such as `results.json`, transport logs, flash logs, GPIO logs, and power logs
- CI-friendly hardware execution workflows

## Product endpoints

- Website: `https://benchci.dev`
- Dashboard: `https://app.benchci.dev`
- Documentation: `https://docs.benchci.dev`

## Execution Modes

### Direct Mode

Use your own hardware bench.

- local execution on the hardware machine
- remote execution through your own BenchCI Agent
- ideal for internal labs and existing benches

### Cloud Mode

Use backend-scheduled benches.

- CLI talks to the BenchCI backend
- backend schedules work to available benches
- cloud-connected Agents poll the backend for assignments
- artifacts and events are returned automatically
- ideal for evaluations, pilots, private benches, shared benches, and remote teams

### Dashboard

Use the dashboard to inspect:

- workspace health
- benches
- runs
- run events
- failure context
- artifacts
- onboarding/setup guidance

## Typical Flow

```text
bench.yaml + suite.yaml
        ↓
   benchci run
        ↓
 local bench / Agent / Cloud bench
        ↓
 real hardware
        ↓
 logs + results
```

## New User Path

1. Create or receive access to a workspace at `https://app.benchci.dev`
2. Install BenchCI
3. Run your first local test
4. Connect a remote Agent bench
5. Trigger from CI
6. Scale to Cloud benches

## Documentation

```{toctree}
:maxdepth: 1

installation.md
quickstart.md
cloud.md
cli.md
bench_config.md
suite_config.md
agent.md
architecture.md
gitlab_ci.md
linux_gpio.md
examples.md
dashboard.md
owner_operations.md
security.md
faq.md
```

## Where to start

For first-time setup, read:

1. `installation.md`
2. `quickstart.md`
3. `cli.md`

For shared infrastructure:

4. `agent.md`
5. `cloud.md`
6. `gitlab_ci.md`

For advanced configuration:

7. `bench_config.md`
8. `suite_config.md`

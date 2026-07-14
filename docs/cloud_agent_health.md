# Cloud Agent Health, Resource Locking, and Scheduling

Use this page to understand how BenchCI decides whether a cloud-connected bench is ready to receive hardware test runs.

BenchCI includes a reliability path across the Agent, backend, scheduler, and dashboard:

```text
Agent checks bench health
        ↓
Backend stores bench health
        ↓
Scheduler avoids unhealthy benches
        ↓
Dashboard explains bench health and failure source
```

This helps users distinguish between:

- firmware failures
- test logic failures
- bench infrastructure problems
- Agent/cloud problems
- configuration problems

---

## Health states

BenchCI uses four bench health states:

| Health | Meaning | Scheduler behavior |
|---|---|---|
| `healthy` | The bench passed required health checks. | Eligible for cloud runs. |
| `degraded` | The bench has warnings or optional issues. | Eligible for cloud runs. |
| `failing` | The bench has a health problem that can make runs unreliable. | Not scheduled. |
| `unknown` | No valid health report is available. | Not scheduled. |

The scheduler assigns runs only to:

```text
healthy
degraded
```

The scheduler avoids:

```text
failing
unknown
missing health
malformed health
```

Even a specifically requested `--bench-id` cannot bypass this health filter.

---

## Agent startup self-check

When a cloud Agent starts, it can run a non-destructive self-test for the registered bench and include health in the backend sync payload.

Start a cloud Agent:

```bash
benchci agent cloud   --token YOUR_AGENT_TOKEN   --bench bench.yaml   --bench-id raspi-nucleo-demo
```

The Agent can report:

- `health`
- `health_status`
- `health_checked_at`
- `health_summary`

The backend stores those fields and exposes them through Cloud and Dashboard APIs.

---

## Agent self-test safety boundary

Agent startup health checks are non-destructive by default.

They do **not**:

- flash firmware
- reset the target
- toggle relays
- power-cycle outlets
- drive GPIO outputs
- send UART/CAN/Modbus commands
- read measurements unless explicitly enabled

This makes startup checks safe for normal Agent operation.

---

## Agent self-test controls

The startup self-test always runs and always opens/closes configured hardware interfaces. This is required so cloud scheduling can trust bench health.

Environment variables only control deeper readback checks:

```bash
BENCHCI_AGENT_SELF_TEST_READ_INPUTS=0
BENCHCI_AGENT_SELF_TEST_READ_MEASUREMENTS=0
```

Recommended starting point:

```bash
export BENCHCI_AGENT_SELF_TEST_READ_INPUTS=0
export BENCHCI_AGENT_SELF_TEST_READ_MEASUREMENTS=0
```

Enable input or measurement reads only after confirming they are safe and useful for your bench.

---

## Health report artifacts on the Agent

Health reports are written under the Agent work directory:

```text
benchci-agent-results/
  bench-health/
    <bench_id>/
      self-test.log
      self-test-summary.json
      nodes/
      resources/
```

These files help lab owners debug why a bench is marked degraded or failing.

---

## Resource locking

BenchCI locks declared hardware resources while a run is using them.

This prevents two BenchCI processes on the same Agent machine from using the same physical interface at the same time.

### Resources protected

Resource locking covers:

- serial transports such as UART and Modbus RTU ports
- CAN interfaces
- Modbus TCP endpoints
- flash/reset tools and probe/port usage
- GPIO lines
- power relay resources and outlets
- measurement resources

If a second run tries to use a locked resource, it should fail early with a resource-lock failure instead of producing confusing hardware results.

If a resource appears locked after a run has stopped, make sure no BenchCI process is still using the hardware before retrying.

---

## Backend health storage

The backend stores bench health fields in the bench inventory:

```text
health_status
health_checked_at
health_summary
health_json
```

This allows Cloud APIs, the scheduler, and the dashboard to use the same health state.

You can inspect visible benches:

```bash
benchci benches list
benchci benches show raspi-nucleo-demo
```

The dashboard also shows health fields in the Benches view.

---

## Scheduler behavior

The scheduler only assigns queued runs to benches that are:

- online
- idle
- accessible to the workspace
- matching requested tags/capabilities
- healthy or degraded

A queued run remains queued if no suitable bench is available.

This is intentional. A queued run is better than assigning a run to a bench that is known to be unhealthy.

---

## Dashboard behavior

The dashboard shows health on bench cards:

```text
Healthy
Degraded
Failing
Unknown
```

The bench health panel can show:

- health summary
- last checked timestamp
- scheduling eligibility message
- pass/warn/fail/skip counts
- failing or warning diagnostic checks
- categories and suggested fixes

The Runs view can also show failure source labels such as:

```text
Firmware
Test logic
Bench infrastructure
Agent / cloud
Configuration
Unknown
```

Example failure explanation:

```text
Likely source: Bench infrastructure
Category: Transport Open Failed
The physical bench, wiring, instrument, or local interface likely needs attention.
```

---

## Troubleshooting unhealthy benches

### Bench is `unknown`

Common causes:

- Agent has not synced health yet
- Agent is too old to publish bench health
- startup self-test has not completed yet
- backend has not received a new bench sync
- Agent token/workspace mismatch

Try:

```bash
benchci benches list
```

Then restart the Agent and check its startup logs:

```bash
benchci agent cloud   --token YOUR_AGENT_TOKEN   --bench bench.yaml   --bench-id raspi-nucleo-demo
```

### Bench is `failing`

Run self-test manually on the hardware machine:

```bash
benchci benches self-test   --bench bench.yaml   --open-hardware   --log-dir bench-health
```

Then inspect:

```text
bench-health/self-test.log
bench-health/self-test-summary.json
bench-health/nodes/
bench-health/resources/
```

Typical fixes include:

- reconnecting USB-UART adapters
- correcting `/dev/ttyUSB*` paths
- fixing GPIO chip/line numbers
- installing missing flash tools
- checking relay power and permissions
- checking HTTP relay or measurement controller URLs
- confirming the correct Agent token/workspace/bench ID

### Bench is `degraded`

A degraded bench can still receive runs.

Review warnings before relying on results, especially for release evidence or customer demos.

Possible causes:

- optional measurement resource unavailable
- optional readback unsupported
- non-critical tool warning
- resource warning that is not required by the current suite

---

## Reference demo bench

A practical starter bench for real embedded validation can be:

```text
Raspberry Pi Zero 2 W
Nucleo F072RB
powered USB hub
USB relay
TTL-USB adapter
TTL-RS485 adapter
RS485-USB adapter
2 GPIO lines from Raspberry Pi to Nucleo
```

This type of bench can demonstrate:

- UART boot validation
- RS-485/Modbus tests
- GPIO ready/reset checks
- relay-based power cycling
- Cloud Agent scheduling
- dashboard health visibility
- run evidence and failure classification

Start simple with UART and flashing, then add power, GPIO, RS-485, and measurements as the bench becomes more professional.

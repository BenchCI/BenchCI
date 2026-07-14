# HIL Orchestration

Use `run_external` when you already own a simulator or HIL rig and want BenchCI to trigger it from CI, collect its reports, and preserve the results in normal BenchCI evidence.

BenchCI v1 does not include vendor-native adapters for dSPACE, NI VeriStand, Vector CANoe, Speedgoat, ASAM XIL, ControlDesk, CANoe COM automation, or Windows/.NET APIs. The supported integration surface is deliberately simple:

- run a bench-owner-approved wrapper command on the Agent, or
- call an allow-listed HTTP API and poll for completion.

The wrapper or HTTP service talks to the rig you already operate.

## Bench policy

External orchestration is denied by default. The bench owner must opt in and define targets under `safety.external`.

```yaml
safety:
  external:
    enabled: true
    targets:
      canoe_smoke:
        work_root: /opt/benchci/external/canoe
        output_root: /opt/benchci/external/canoe/out
        argv_prefix:
          - /opt/benchci/wrappers/run-canoe-smoke
        arg_patterns:
          - "[A-Za-z0-9_.-]+"
        max_timeout_ms: 1800000
        max_logs: 20
        max_log_bytes: 262144
        max_log_total_bytes: 1048576
        max_artifacts: 50
        max_artifact_bytes: 1048576
        max_artifact_total_bytes: 5242880
        lock_key: external:canoe-rig-1
```

`argv_prefix` is controlled by `bench.yaml`. Suite authors can only append `args`; they cannot replace the command prefix.

Prefer a wrapper that accepts a small positional argument set. Avoid bare prefixes such as `ssh hil@host` or `curl` because suite args could become tool options. For an SSH-to-Windows rig, make the wrapper own the SSH command, fixed options, remote script path, and copy-back behavior.

## Suite step

```yaml
tests:
  - name: canoe HIL smoke
    steps:
      - run_external:
          target: canoe_smoke
          cwd: runs/pr-142
          args: ["smoke"]
          timeout_ms: 900000
          source: canoe
          framework: hil
          junit: reports/junit.xml
          logs:
            - logs/canoe.log
          artifacts:
            - captures
```

All suite-controlled local paths are relative. BenchCI rejects absolute paths, `..` traversal, and symlinks that resolve outside the allowed collection root.

## HTTP targets

HTTP targets must define `base_url`. BenchCI enforces the base URL for both trigger and poll requests, disables redirects, fails on 3xx, URL-encodes `{job_id}`, and redacts header values in evidence.

```yaml
safety:
  external:
    enabled: true
    targets:
      rig_api:
        work_root: /opt/benchci/external/rig-api
        base_url: http://rig-controller.local/api
        methods: [POST, GET]
        max_poll_interval_ms: 10000
```

```yaml
- run_external:
    target: rig_api
    timeout_ms: 600000
    http:
      method: POST
      url: runs
      headers_env:
        Authorization: RIG_API_AUTH
      json:
        suite: smoke
      job_id_json_path: job_id
      poll:
        method: GET
        url: runs/{job_id}
        interval_ms: 1000
        status_json_path: status
        success_values: [passed]
        failure_values: [failed, error]
    junit: reports/junit.xml
```

`poll.interval_ms` must be at least 500 ms.

## Agent-local collection

Collection is Agent-local. After the trigger finishes, BenchCI reads JUnit, CTRF, logs, and artifacts from the Agent filesystem.

For a Windows HIL host reached over SSH, the wrapper must copy reports and artifacts back to the Agent before it exits. A common pattern is:

1. Agent wrapper creates an Agent-local run directory.
2. Wrapper triggers the Windows host over SSH or HTTP.
3. Windows-side script writes JUnit/CTRF and captures.
4. Wrapper copies those files back to the Agent run directory.
5. Wrapper exits only after copy-back is complete.

## Evidence

BenchCI writes `external-results.json`, adds `evidence.external_results`, merges parsed external tests into `evidence.traceability.tests`, and records the exact effective command argv or HTTP method/URL with headers redacted.

The step fails when declared reports are missing, parsing fails, reports contain zero tests, parsed tests include failed/error statuses, a command exits nonzero, HTTP reports failure, or the timeout is reached.

## Locking boundary

External targets use BenchCI resource locks. By default, target `canoe_smoke` locks `external:canoe_smoke`; set `lock_key` when multiple targets address the same rig.

Locks are per Agent host in v1. If one physical rig is reachable from two different Agents, BenchCI does not serialize across those Agents. Use one physical rig with one Agent, or route all triggers for that rig through a single Agent-controlled target.

## Artifact caps

Agent-side caps are enforced before files are read and uploaded. Defaults mirror the external-result API limits. Bench policy can raise per-target caps for real HIL captures, bounded by the backend deployment’s configured hard limits.

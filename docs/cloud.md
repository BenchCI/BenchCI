# BenchCI Cloud

BenchCI Cloud lets you run real hardware tests through the BenchCI backend instead of connecting directly to a bench machine.

Cloud Mode is now workspace-aware: users see benches, runs, and artifacts that belong to their workspace or have been explicitly granted to their workspace.

## Why Cloud Mode

Use Cloud Mode when you want:

* shared hardware access
* private customer benches
* centralized scheduling
* CI-driven execution
* no direct access to hardware machines
* managed demo benches
* dashboard visibility for runs, benches, events, and artifacts

## Typical Flow

```text
CI / Developer
↓
BenchCI CLI
↓
BenchCI Backend
↓
Queue / Scheduler
↓
BenchCI Agent
↓
Real hardware bench
↓
Artifacts + results
↓
Dashboard + CLI
```

Dashboard:

```text
https://app.benchci.dev
```

## Login

```bash
benchci login
```

## List Available Benches

```bash
benchci benches list
```

## Run on Specific Bench

```bash
benchci run --cloud --bench-id demo-bench --suite suite.yaml --artifact build/fw.elf
```

## Run by Capability

```bash
benchci run --cloud --tag uart --transport uart --suite suite.yaml --artifact build/fw.elf
```

Other useful selectors include:

```bash
benchci run --cloud --flash-backend openocd --suite suite.yaml --artifact build/fw.elf
benchci run --cloud --has-gpio --suite suite.yaml --artifact build/fw.elf
benchci run --cloud --has-power --suite suite.yaml --artifact build/fw.elf
```

## Inspect Runs

```bash
benchci runs list
benchci runs show <RUN_ID>
benchci runs events <RUN_ID>
benchci runs artifacts <RUN_ID>
```

The same runs can be inspected from the dashboard.

## Bench Types

BenchCI Cloud can expose:

* shared benches
* reserved benches
* private customer benches
* managed demo benches

Typical meanings:

- `private` → owned by one workspace
- `managed_shared` → owned by BenchCI/internal workspace and shared by grants
- `managed_reserved` → reserved for a specific customer workspace
- `public_demo` → demo/evaluation bench where enabled

## Cloud Agent

A cloud-connected Agent polls the backend for assignments.

Example:

```bash
benchci agent cloud \
  --backend https://benchci-backend.fly.dev \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --agent-name "Lab Agent 01"
```

Cloud Agents make outbound requests to the backend, so lab machines do not need to expose public inbound ports.

## Good Use Cases

* evaluate BenchCI quickly
* run nightly smoke tests
* use hardware without building a full lab first
* support distributed engineering teams
* connect private customer-owned benches to a central backend
* share managed benches across pilot customers

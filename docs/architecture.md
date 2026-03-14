# BenchCI Architecture

BenchCI is designed to enable automated testing of firmware on real hardware.

The system separates responsibilities between a CLI, remote agents, and a licensing backend.

---

## Components

**BenchCI CLI**

The CLI is used by developers and CI systems.

Responsibilities:

- load configuration
- authenticate with backend
- submit runs to agents
- collect artifacts

**BenchCI Agent**

The agent executes hardware tests on machines connected to physical devices.

Responsibilities:

- receive test jobs
- flash firmware
- communicate with devices
- produce artifacts

**BenchCI Backend**

The backend manages licensing and authentication.

Responsibilities:

- validate license keys
- issue sessions
- enforce access control

---

## Execution Flow

```
Developer / CI
      │
      ▼
BenchCI CLI
      │
      ▼
BenchCI Agent
      │
      ▼
Hardware Device
```

---

## Artifacts

BenchCI produces structured artifacts.

```
transport.log
flash.log
results.json
```

These artifacts are stored in:

```
benchci-results/
```

and may be collected by CI systems.
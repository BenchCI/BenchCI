# BenchCI Documentation

BenchCI provides infrastructure for **continuous integration testing on real embedded hardware**.

This documentation describes how to install BenchCI, configure hardware boards, define test suites, and integrate tests into CI pipelines.

---

## Documentation Structure

```{toctree}
:maxdepth: 1

installation.md
quickstart.md
cli.md
board_config.md
suite_config.md
agent.md
architecture.md
gitlab_ci.md
```

---

## Core Components

BenchCI consists of three main components.

**BenchCI CLI**

The command-line interface used by developers and CI pipelines.

**BenchCI Agent**

A service running on machines connected to hardware benches.

**BenchCI Backend**

A licensing and authentication service.

---

## Typical Workflow

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

The CLI submits test jobs, the agent executes them on the hardware, and results are returned to the CLI.

---

## Getting Started

To begin using BenchCI, read the quickstart guide:

[quickstart.md](quickstart.md)
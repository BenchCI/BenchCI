# BenchCI Agent

BenchCI Agent runs on machines connected to hardware devices.

The agent receives test jobs and executes them locally.

---

## Starting the Agent

Start the agent:

```
benchci agent serve
```

Default configuration:

```
host: 0.0.0.0
port: 8080
```

---

## Authentication

Agents should normally require an access token.

Example:

```
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

---

## Health Check

Verify the agent:

```
curl http://localhost:8080/health
```

---

## Artifacts

Agents generate artifacts including:

```
transport.log
flash.log
results.json
```
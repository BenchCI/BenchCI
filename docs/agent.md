# BenchCI Agent

BenchCI Agent runs on machines connected to hardware devices.

---

## Start Agent

```
benchci agent serve
```

Default:

```
host: 0.0.0.0
port: 8080
```

---

## Authentication

```
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

---

## Health Check

```
curl http://localhost:8080/health
```

---

## Artifacts

```
transport.log
flash.log
gpio.log
results.json
```

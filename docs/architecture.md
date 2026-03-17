# BenchCI Architecture

BenchCI enables automated testing on real hardware.

---

## Components

### CLI

* load configuration
* authenticate
* submit runs
* collect artifacts

### Agent

* execute tests
* flash firmware
* communicate with devices

### Backend

* license validation
* session management

---

## Flow

```
Developer / CI
      ↓
BenchCI CLI
      ↓
BenchCI Agent
      ↓
Hardware Device
```

---

## Artifacts

```
benchci-results/
├── transport.log
├── flash.log
├── gpio.log
└── results.json
```

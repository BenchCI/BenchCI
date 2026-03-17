# BenchCI CLI

The BenchCI CLI is the primary interface for running hardware tests.

---

## Commands

### validate

Validate configuration files.

```
benchci validate -b board.yaml -s suite.yaml
```

---

### run

Execute a test suite.

```
benchci run -b board.yaml -s suite.yaml -a build/fw.elf
```

---

### doctor

Run environment diagnostics.

```
benchci doctor
```

---

### login

Authenticate with BenchCI backend.

```
benchci login
```

---

### logout

Remove stored authentication session.

```
benchci logout
```

---

### whoami

Show current authentication status.

```
benchci whoami
```

---

### agent serve

Start a BenchCI Agent.

```
benchci agent serve
```

---

## Artifacts

BenchCI stores results in:

```
benchci-results/
├── transport.log
├── flash.log
├── gpio.log
└── results.json
```

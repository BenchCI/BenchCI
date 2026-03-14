# BenchCI CLI

The BenchCI CLI is the primary interface for running hardware tests.

---

## Commands

**validate**

Validate configuration files.

```
benchci validate --board board.yaml --suite suite.yaml
```

**run**

Execute a test suite.

```
benchci run -b board.yaml -s suite.yaml -a build/fw.elf
```

**doctor**

Run environment diagnostics.

```
benchci doctor
```

**login**

Authenticate with the BenchCI backend.

```
benchci login
```

**logout**

Remove stored authentication session.

```
benchci logout
```

---

## Running Tests

Example:

```
benchci run \
  -b board.yaml \
  -s suite.yaml \
  -a build/fw.elf
```

This command:

1. flashes firmware
2. executes the test suite
3. collects results

---

## Artifacts

BenchCI stores results in:

```
benchci-results/
```

Files include:

```
transport.log
flash.log
results.json
```
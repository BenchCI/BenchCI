# Quickstart

This guide shows how to run your first BenchCI test.

BenchCI workflows consist of three parts:

1. board configuration
2. test suite definition
3. test execution

---

## Step 1 — Create board configuration

Create `board.yaml`

Example:

```yaml
name: nucleo_f4

flash:
  backend: openocd
  interface_cfg: interface/stlink.cfg
  target_cfg: target/stm32f4x.cfg

reset:
  method: openocd

transport:
  backend: uart
  port: /dev/ttyUSB0
  baud: 115200
  timeout_ms: 100
```

---

## Step 2 — Create test suite

Create `suite.yaml`

```yaml
name: firmware_tests

tests:

  - name: boot_ok
    steps:
      - expect_uart:
          contains: "[BOOT] OK"
          within_ms: 3000

  - name: ping
    steps:
      - send_uart: "PING\n"
      - expect_uart:
          contains: "PONG"
          within_ms: 1000
```

---

## Step 3 — Run BenchCI

```
benchci run \
  -b board.yaml \
  -s suite.yaml \
  -a build/fw.elf
```

BenchCI will:

- flash firmware
- run tests
- collect logs

Artifacts are stored in:

```
benchci-results/
```

Files include:

```
transport.log  
flash.log  
results.json
```
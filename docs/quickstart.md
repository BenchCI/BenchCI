# Quickstart

This guide walks you through running your first BenchCI test on real hardware.

By the end, you will:

* flash firmware to your device
* run an automated test suite
* validate device behavior via UART
* collect structured test results

---

## 🧠 How BenchCI Works

BenchCI uses two configuration files:

* **`board.yaml`** → describes how to connect to your hardware
* **`suite.yaml`** → defines what to test and how to validate behavior

You then run everything with a single command:

```
benchci run -b board.yaml -s suite.yaml -a build/fw.elf
```

---

## ⚙️ Prerequisites

* Python 3.11+
* A development board (e.g. STM32 Nucleo)
* Firmware that prints messages over UART
* Flashing tool installed (e.g. OpenOCD)

---

## 📦 Step 1 — Install BenchCI

BenchCI CLI is provided to licensed users.

Follow the installation instructions provided with your access.

Verify your setup:

```
benchci doctor
```

Authenticate:

```
benchci login
```

---

## 🔌 Step 2 — Create Board Configuration

Create `board.yaml`:

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

This file tells BenchCI:

* how to flash your firmware
* how to reset the device
* how to communicate with it

---

## 🧪 Step 3 — Create Test Suite

Create `suite.yaml`:

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

This suite verifies:

* the device boots correctly
* it responds to a simple command

You can validate your configuration before running:

```
benchci validate -b board.yaml -s suite.yaml
```

---

## 🚀 Step 4 — Run the Test

```
benchci run \
  -b board.yaml \
  -s suite.yaml \
  -a build/fw.elf
```

BenchCI will:

1. flash the firmware
2. reset the device
3. read UART output
4. execute test steps
5. validate results

---

## 📊 Step 5 — Inspect Results

After the run, results are stored in:

```
benchci-results/
```

Example contents:

```
transport.log   # raw communication logs  
flash.log       # flashing output  
gpio.log        # GPIO activity (if used)
results.json    # structured test results  
```

---

## ✅ Expected Behavior

If everything is working:

* the firmware prints `[BOOT] OK`
* the device responds `PONG` to `PING`
* all tests pass

---

## ❌ Troubleshooting

If something fails:

* check `transport.log` for UART output
* verify correct serial port (`/dev/ttyUSB0`)
* ensure your firmware prints expected messages
* run `benchci doctor` to validate your setup

---

## 🔜 Next Steps

Now that you have a working setup:

* explore GPIO control
* test Modbus devices
* integrate BenchCI into CI pipelines

See:

* `examples/uart_basic`
* `examples/modbus_rtu_device`
* `examples/modbus_tcp_device`
* `examples/ci/gitlab`

---

BenchCI scales from local debugging to fully automated hardware CI.

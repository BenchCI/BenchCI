# Installation

Install BenchCI on the machines that need to run the CLI:

- your development machine
- a hardware-connected lab machine
- a CI runner
- a self-hosted runner

For local tests, the machine running BenchCI must be connected to the hardware.

For Cloud Mode, CI only needs the CLI. The hardware-connected Agent executes the test near the device.

---

## Install BenchCI

```bash
pip install benchci
```

Verify the CLI:

```bash
benchci --help
```

Upgrade:

```bash
pip install --upgrade benchci
```

---

## Log in

BenchCI access is tied to a BenchCI account and workspace.

```bash
benchci login
```

Check your active account and workspace:

```bash
benchci whoami
```

Log out:

```bash
benchci logout
```

Create or access your workspace from:

```text
https://app.benchci.dev
```

For early access customers, BenchCI workspace activation and billing are currently handled manually.

---

## Verify your environment

Run diagnostics:

```bash
benchci doctor
```

Check a specific bench file:

```bash
benchci doctor --bench bench.yaml
```

Check an Agent:

```bash
benchci doctor --agent http://192.168.1.50:8080
```

If the Agent requires authentication:

```bash
benchci doctor --agent http://192.168.1.50:8080 --token "$BENCHCI_AGENT_TOKEN"
```

---

## Install on a hardware-connected machine

This is the machine physically connected to the DUT, debugger, UART/CAN/Modbus adapters, GPIO lines, relays, or power control hardware.

```bash
pip install benchci
```

For direct Agent mode:

```bash
benchci agent serve
```

To protect Agent endpoints:

```bash
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

For Cloud Mode:

```bash
benchci agent cloud \
  --backend https://api.benchci.dev \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench \
  --agent-name "Lab Agent 01"
```

---

## Install on CI runner machines

A CI runner usually does not need direct hardware access when using Cloud Mode.

```bash
pip install benchci
```

Cloud Mode run:

```bash
benchci login

benchci run --cloud \
  --bench-id my-cloud-bench \
  --suite suite.yaml \
  --artifact build/fw.elf
```

Direct Agent run:

```bash
benchci run \
  --agent "$BENCHCI_AGENT_URL" \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

Registered-bench direct Agent run:

```bash
benchci run \
  --agent "$BENCHCI_AGENT_URL" \
  --bench-id my-bench \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

---

## External tools

BenchCI is installed through Python, but your bench may require external system tools depending on what you automate.

Common tools include:

- OpenOCD for many STM32 and ARM workflows
- STM32CubeProgrammer for STM32 workflows
- SEGGER J-Link tools for J-Link workflows
- esptool for ESP32 workflows
- Linux GPIO access through `/dev/gpiochipX`
- CAN tools and SocketCAN configuration for CAN workflows
- serial device permissions for UART workflows

Example Ubuntu packages for a basic STM32/OpenOCD workflow:

```bash
sudo apt-get update
sudo apt-get install -y openocd gcc-arm-none-eabi make
```

For GPIO, make sure the user running BenchCI can access `/dev/gpiochipX`.

For serial, make sure the user can access `/dev/ttyUSBX` or `/dev/ttyACMX`.

---

## Next step

Continue with:

[Quickstart](quickstart.md)

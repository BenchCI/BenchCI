# Installation

BenchCI is distributed to licensed users as a Python wheel package.

BenchCI is not installed directly from the public GitHub repository.

---

## What You Receive

Licensed users receive:

* BenchCI license key
* BenchCI CLI package (.whl)

---

## Installing BenchCI

Install the provided wheel file:

```
pip install benchci-0.1.0-py3-none-any.whl
```

Verify installation:

```
benchci --help
```

---

## Activate Your License

```
benchci login
```

Check status:

```
benchci whoami
```

Logout:

```
benchci logout
```

---

## Verify Environment

```
benchci doctor
```

---

## Installing on Bench Machines

Install CLI on hardware-connected machine:

```
pip install benchci-0.1.0-py3-none-any.whl
```

Start agent:

```
benchci agent serve
```

---

## Agent Authentication

```
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

---

## Installing in CI

```
pip install benchci-0.1.0-py3-none-any.whl

benchci login --license-key "$BENCHCI_LICENSE"

benchci run \
  -b board.yaml \
  -s suite.yaml \
  -a build/fw.elf \
  --agent "$BENCHCI_AGENT_URL" \
  --token "$BENCHCI_AGENT_TOKEN"
```

---

## External Tools

BenchCI depends on external tools:

* OpenOCD
* STM32CubeProgrammer
* SEGGER J-Link

Check with:

```
benchci doctor
```

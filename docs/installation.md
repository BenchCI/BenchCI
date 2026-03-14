# Installation

BenchCI is distributed to licensed users as a Python wheel package.

BenchCI is **not installed directly from the public GitHub repository**.

---

## What You Receive

Licensed users receive:

- BenchCI license key
- BenchCI CLI package (.whl)

---

## Installing BenchCI

Install the provided wheel file.

```
pip install benchci-0.1.0-py3-none-any.whl
```

Verify installation:

```
benchci --help
```

---

## Activate Your License

Activate your license using:

```
benchci login
```

The CLI stores a session locally:

```
~/.benchci/session.json
```

Check license status:

```
benchci whoami
```

Logout:

```
benchci logout
```

---

## Installing on Bench Machines

Install the CLI package on the machine connected to hardware.

```
pip install benchci-0.1.0-py3-none-any.whl
```

Start the agent:

```
benchci agent serve
```

---

## Agent Authentication

Agents should normally require authentication.

Example:

```
export BENCHCI_AGENT_TOKEN=secure-token

benchci agent serve
```

---

## Installing in CI

Example CI commands:

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

BenchCI may rely on external tools depending on board configuration.

Examples:

- OpenOCD
- STM32CubeProgrammer
- SEGGER J-Link

Check environment:

```
benchci doctor
```
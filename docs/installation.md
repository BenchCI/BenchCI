# Installation

BenchCI is distributed to licensed users as a Python wheel. It is not installed directly from the public repository.

## What you receive

Licensed users receive:

- a BenchCI wheel package
- a BenchCI license key

## Install BenchCI

Install the wheel you received:

```bash
pip install benchci-0.1.0-py3-none-any.whl
```

Verify the CLI is available:

```bash
benchci --help
```

## Activate your license

Activate BenchCI with your license key:

```bash
benchci login
```

Or provide the key directly:

```bash
benchci login --license-key "YOUR_LICENSE_KEY"
```

Check the stored session:

```bash
benchci whoami
```

Remove the session:

```bash
benchci logout
```

## Verify your environment

Run diagnostics:

```bash
benchci doctor
```

You can also check a specific bench file:

```bash
benchci doctor --bench bench.yaml
```

Check agent reachability:

```bash
benchci doctor --agent http://192.168.1.50:8080
```

If the agent requires authentication:

```bash
benchci doctor --agent http://192.168.1.50:8080 --token "$BENCHCI_AGENT_TOKEN"
```

## Install on a hardware-connected machine

Install BenchCI on the machine that has direct access to the DUT, flasher, serial device, CAN interface, or Linux GPIO hardware:

```bash
pip install benchci-0.1.0-py3-none-any.whl
```

Start the Agent:

```bash
benchci agent serve
```

To require authentication:

```bash
export BENCHCI_AGENT_TOKEN=secure-token
benchci agent serve
```

## Install on CI or runner machines

A CI runner only needs the BenchCI CLI and network access to the Agent. It does **not** need direct hardware access for remote runs.

Example remote run:

```bash
benchci run \
  --agent "$BENCHCI_AGENT_URL" \
  --bench bench.yaml \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

Example registered-bench remote run:

```bash
benchci run \
  --agent "$BENCHCI_AGENT_URL" \
  --bench-id my-bench \
  --suite suite.yaml \
  --artifact build/fw.elf \
  --token "$BENCHCI_AGENT_TOKEN"
```

## External tools

BenchCI uses Python packages and, depending on your bench, external system tools.

Common Python dependencies include:

- `pydantic`
- `pyyaml`
- `typer`
- `httpx`
- `fastapi`
- `uvicorn`

Transport and GPIO dependencies include:

- `pyserial`
- `pymodbus`
- `python-can`
- `gpiod` on Linux

Flashing tools may include:

- `openocd`
- `STM32_Programmer_CLI`
- `JLinkExe` or `JLink.exe`
- `esptool.py`

Use `benchci doctor` to verify what your current bench needs.

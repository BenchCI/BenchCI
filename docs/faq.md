# FAQ

## What is BenchCI?

BenchCI is continuous integration for real embedded hardware.

It lets you flash firmware, execute tests on real devices, and return logs/results to CI automatically.

---

## Do I need hardware locally?

No.

You can use BenchCI in three ways:

- local bench on your machine
- remote Agent on a hardware-connected machine
- BenchCI Cloud bench through backend scheduling

For the first local quickstart, you do need access to a board connected to your machine.

---

## Can CI trigger real hardware tests?

Yes.

BenchCI is designed for CI workflows such as GitHub Actions and GitLab CI.

The recommended flow is Cloud Mode:

```text
CI → BenchCI backend → cloud-connected Agent → real hardware
```

---

## Can I use Raspberry Pi as an Agent?

Yes.

A Raspberry Pi is a common deployment target for small benches, especially when it controls:

- UART adapters
- GPIO lines
- relays
- USB-connected debuggers
- RS-485 or CAN adapters

---

## Can I use my own existing lab bench?

Yes.

BenchCI can run against customer-owned hardware.

Start by making local execution work with `bench.yaml` and `suite.yaml`, then connect the bench through Agent or Cloud Mode.

---

## What protocols are supported?

BenchCI currently supports:

- UART
- Modbus RTU
- Modbus TCP
- CAN

---

## What flashing tools are supported?

BenchCI currently supports:

- OpenOCD
- STM32CubeProgrammer
- SEGGER J-Link
- esptool

---

## Is BenchCI only for STM32?

No.

BenchCI is hardware-agnostic.

STM32 is a common first workflow because OpenOCD, CubeProgrammer, ST-Link, and NUCLEO boards are widely used.

---

## What artifacts do I get?

Typical outputs include:

- `results.json`
- flash logs
- transport logs
- GPIO logs
- power logs
- per-node logs

The exact artifacts depend on your bench and suite.

---

## Can multiple engineers share benches?

Yes.

BenchCI supports queued shared execution models.

Cloud Mode is workspace-aware and can show private, shared, reserved, or demo benches depending on access.

---

## Do I need a license key?

The main user flow uses BenchCI accounts and workspaces:

```bash
benchci login
```

---

## Where do I log in?

Dashboard:

```text
https://app.benchci.dev
```

CLI:

```bash
benchci login
```

---

## How is BenchCI billed?

BenchCI is currently early access.

Paid access is handled through manual onboarding and monthly invoicing.

Contact:

```text
tech@benchci.dev
```

---

## Can I connect my own private bench to Cloud Mode?

Yes.

A cloud-connected Agent can sync a private workspace bench to the backend so runs can be scheduled centrally while execution still happens on your hardware.

---

## How do I connect my hardware to Cloud Mode?

Run a BenchCI Agent on the hardware-connected machine:

```bash
benchci agent cloud \
  --backend https://api.benchci.dev \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench
```

See:

[BenchCI Agent](agent.md)

---

## Should I start with Cloud Mode immediately?

Usually no.

Recommended order:

1. make local execution work
2. start a cloud-connected Agent
3. verify the bench appears in the dashboard
4. run through Cloud Mode
5. connect CI

This avoids debugging hardware, CI, and cloud setup at the same time.

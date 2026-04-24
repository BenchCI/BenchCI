# FAQ

## Do I need hardware locally?

No. You can run local benches, remote benches, or BenchCI Cloud benches.

## Can CI trigger real hardware tests?

Yes. BenchCI is designed for CI workflows.

## What protocols are supported?

BenchCI currently supports:

- UART
- Modbus RTU
- Modbus TCP
- CAN

## Can I use Raspberry Pi as an Agent?

Yes. Raspberry Pi is a common deployment target.

## Can I use my own existing lab bench?

Yes. Direct Mode is designed for customer-owned hardware.

## What artifacts do I get?

Typical outputs include:

- results.json
- flash logs
- transport logs
- GPIO logs

## Can multiple engineers share benches?

Yes. BenchCI supports queued shared execution models.

## Is BenchCI only for STM32?

No. BenchCI is hardware-agnostic and supports multiple flashing backends and transport types.

## Do I need a license key?

Current onboarding uses BenchCI accounts and workspaces. Older license/session concepts may exist internally or for compatibility, but the main user flow is:

```bash
benchci login
```

## Where do I log in?

Use the dashboard:

```text
https://app.benchci.dev
```

The CLI also uses the same account:

```bash
benchci login
```

## How is BenchCI billed?

BenchCI is currently early access. Paid access is handled through manual onboarding and monthly invoicing.

Contact:

```text
tech@benchci.dev
```

## Can I connect my own private bench to Cloud Mode?

Yes. A cloud-connected Agent can sync a private workspace bench to the backend so runs can be scheduled centrally while execution still happens on your hardware.

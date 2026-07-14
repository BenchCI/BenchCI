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
- I2C
- SPI
- bounded protocol fuzzing for UART, CAN, and Modbus
- GPIO control and observation
- bench-level power resources
- HTTP, SCPI, I2C power-monitor, script, and serial measurement resources

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
- measurement logs
- `evidence.json` and `evidence.html`
- `manifest.json` with artifact hashes
- per-node logs

The exact artifacts depend on your bench and suite.

---

## Does BenchCI support fuzzing?

Yes. BenchCI supports bounded protocol fuzzing for UART, CAN, Modbus RTU, and Modbus TCP as normal `suite.yaml` steps.

Fuzzing is meant to add robustness coverage on top of explicit smoke and regression tests. It records the seed, campaign metadata, first failing case, and JSONL case logs so a failure can be replayed from the evidence package.

See [Protocol Fuzzing](fuzzing.md).

---

## Does BenchCI support fault injection?

BenchCI 1.4 includes experimental, allow-listed power glitch, GPIO glitch, and
malformed-UART-byte steps. Each target must be enabled in the bench safety
policy, and every step requires a bounded UART recovery check.

The evidence records the requested fault, restoration, recovery time, and
watchdog observation. It does not claim precision electrical timing. See
[Controlled Fault Injection](fault-injection.md).

## Can the DUT identify itself?

Yes. BenchCI can optionally query a `BENCHCI_ID:` JSON response over UART before
the first test, compare recognized fields with the configured DUT identity, and
record the verification status and response hash. See
[DUT Self-Identification](dut-self-identification.md).


## Can BenchCI measure current or voltage?

Measurement resources support HTTP-backed lab-controller measurements, raw SCPI measurements, SCPI power-supply readback, I2C power monitors, script outputs, and simple serial measurements. This can be used to record values such as sleep current or supply voltage and assert thresholds in `suite.yaml`.

SCPI resources support TCP (`tcp://`), serial (`serial://`), and VISA/USBTMC-style addresses when the optional instrument dependencies are installed.

## Does BenchCI require a specific relay brand?

No. Power uses bench-level resources. A suite can call `power_cycle` while `bench.yaml` describes whether the implementation is GPIO, HTTP relay, or generic serial relay command maps.

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

## How do trials and commercial use work?

BenchCI starts with a 30-day trial of Team features after email verification. For
commercial usage after the trial, contact:

```text
tech@benchci.dev
```

---

## How do I report a bug or request a feature?

Use the **Requests** page in the BenchCI dashboard:

```text
https://app.benchci.dev
```

Requests are attached to your active workspace and can include severity, description, optional run ID, and optional bench ID. The dashboard shows the current triage status after BenchCI reviews the request.

---

## Can I connect my own private bench to Cloud Mode?

Yes.

A cloud-connected Agent can sync a private workspace bench to the backend so runs can be scheduled centrally while execution still happens on your hardware.

---

## How do I connect my hardware to Cloud Mode?

Run a BenchCI Agent on the hardware-connected machine:

```bash
benchci agent cloud \
  --token YOUR_AGENT_TOKEN \
  --bench bench.yaml \
  --bench-id my-bench
```

See:

[BenchCI Agent](agent.md)

---

## What are Evidence Reports?

Evidence Reports are files generated for each run:

- `evidence.json` for machines and integrations
- `evidence.html` for humans
- `metadata.json` for supporting metadata
- input snapshots of `bench.yaml` and `suite.yaml`

They capture firmware hash, Git/CI metadata, bench/suite hashes, artifacts, structured failure details, fuzz summaries when used, and optional requirement/test/risk traceability.

Evidence can also include configured or verified DUT identity, LCOV summaries,
external JUnit/CTRF source metadata, firmware assurance events, measurements,
and experimental controlled fault-injection summaries.

## What is a release evidence bundle?

A release evidence bundle packages completed cloud runs into a workspace-scoped
ZIP with per-run evidence, full and latest-result coverage matrices, LCOV and
DUT context, review history, and `HASHES.txt`.

Workspaces can move bundles through draft, under-review, approved, or rejected
states with required comments and hash-linked review events.
Approved bundles are locked against normal deletion. Review reports can be
downloaded as HTML or PDF.

These are review aids and structured verification records, not certification.
See [QA Evidence Workflow](qa_evidence_workflow.md).

## What are requirement IDs, test case IDs, and risk IDs?

They are optional labels in `suite.yaml`:

- requirement ID: what the system must do, for example `REQ-BOOT-001`
- test case ID: how the requirement is verified, for example `TC-BOOT-001`
- risk ID: what could go wrong, for example `RISK-BOOT-001`

The useful chain is:

```text
Risk -> Requirement -> Test case -> BenchCI run evidence
```

## Should I start with Cloud Mode immediately?

Usually no.

Recommended order:

1. make local execution work
2. start a cloud-connected Agent
3. verify the bench appears in the dashboard
4. run through Cloud Mode
5. connect CI

This avoids debugging hardware, CI, and cloud setup at the same time.

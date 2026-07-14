# I2C and SPI Station Wiring Guide

This guide covers electrical safety, pull-up resistors, voltage levels, and the device-tree / sysfs assumptions BenchCI makes when using the `i2c-sensor-smoke` and `spi-flash-verify` presets (and any custom bench that uses the `i2c` or `spi` transport backends).

---

## I2C Wiring

### Signal Lines

| Pin | Function |
|-----|----------|
| SDA | Bidirectional data |
| SCL | Clock (master drives) |
| GND | Common ground |
| VCC | Sensor supply (see voltage level section) |

### Pull-up Resistors

I2C requires pull-up resistors on both SDA and SCL. BenchCI does not configure pull-ups in software — they must be present on the bench hardware.

**Recommended values:**

| Bus speed | Pull-up value | Max cable length |
|-----------|--------------|-----------------|
| 100 kHz (standard) | 4.7 kΩ | ~1 m |
| 400 kHz (fast) | 2.2 kΩ | ~30 cm |
| 1 MHz (fast-plus) | 1 kΩ | ~10 cm |

Use resistors to 3.3 V for 3.3 V-tolerant sensors. Use level shifters when mixing 3.3 V and 5 V devices.

### Voltage Levels

Most modern SBCs (Raspberry Pi, BeagleBone, NVIDIA Jetson) expose I2C at **3.3 V logic**. Connecting a 5 V I2C sensor without a level shifter will damage the SBC's GPIO bank.

**Isolation:** If the DUT is connected to mains power or an untested power rail, use an I2C isolator (e.g. ISO1541, ADUM1250) between the bench agent and the DUT.

### Short-Circuit Protection

Add a 100 Ω series resistor on SDA and SCL between the bench agent and the DUT. This limits current if the DUT firmware drives a line low while BenchCI is doing a scan.

### `/dev/i2c-*` Availability

BenchCI auto-detects available I2C buses by scanning `/dev/i2c-0`, `/dev/i2c-1`, etc. at bench registration time. The detected bus numbers are reported in the `capabilities.i2c_buses` field of the bench sync payload.

Ensure the `i2c-dev` kernel module is loaded on the agent host:

```bash
sudo modprobe i2c-dev
# To persist across reboots:
echo "i2c-dev" | sudo tee /etc/modules-load.d/i2c-dev.conf
```

The `smbus2` Python package must be installed in the BenchCI agent environment:

```bash
pip install smbus2
```

Grant the agent user access to I2C devices without sudo:

```bash
sudo usermod -aG i2c $USER
# Log out and back in, or:
sudo chmod a+rw /dev/i2c-*
```

---

## SPI Wiring

### Signal Lines

| Pin | Function |
|-----|----------|
| MOSI | Master Out Slave In |
| MISO | Master In Slave Out |
| SCLK | Clock |
| CS/CE | Chip Select (active low) |
| GND | Common ground |

### Voltage Levels

SPI signals are **not** open-drain — they are push-pull. Connecting 5 V SPI to a 3.3 V SBC without a level shifter will latch-up or destroy the SBC's SPI controller.

Use a bidirectional level shifter (e.g. TXS0108E, 74LVC245) for mixed-voltage setups.

### Short-Circuit Protection

Unlike I2C, SPI lines are driven both ways. Do not add series resistors > 47 Ω — they cause signal integrity issues at speeds above 1 MHz.

### `/dev/spidev*.*` Availability

BenchCI auto-detects SPI devices by scanning `/dev/spidev0.0`, `/dev/spidev0.1`, etc. at bench registration time. Detected devices are reported in `capabilities.spi_devices`.

Enable the SPI interface on Raspberry Pi:

```bash
# Via raspi-config → Interface Options → SPI → Enable
# Or add to /boot/config.txt:
dtparam=spi=on
```

The `spidev` Python package must be installed:

```bash
pip install spidev
```

Grant the agent user access to SPI devices:

```bash
sudo usermod -aG spi $USER
sudo usermod -aG gpio $USER
```

---

## Bench Config Reference

### I2C Transport (`bench.yaml`)

```yaml
nodes:
  dut:
    kind: mcu
    role: target
    transports:
      board_i2c:
        backend: i2c
        bus: 1           # corresponds to /dev/i2c-1
        timeout_ms: 3000
```

### SPI Transport (`bench.yaml`)

```yaml
nodes:
  dut:
    kind: mcu
    role: target
    transports:
      flash_spi:
        backend: spi
        bus: 0           # corresponds to /dev/spidev0.X
        device: 0        # corresponds to /dev/spidevX.0
        max_speed_hz: 1000000
        mode: 0
        bits_per_word: 8
```

Generate a validated starter config with:

```bash
benchci init --preset i2c-sensor-smoke
benchci init --preset spi-flash-verify
```

## Station Smoke Suites

The repository includes Station-oriented smoke suites under `examples/17-station-i2c-spi-smoke/`:

```bash
benchci run --bench examples/17-station-i2c-spi-smoke/bench.yaml \
  --suite examples/17-station-i2c-spi-smoke/i2c-smoke.suite.yaml \
  --skip-flash

benchci run --bench examples/17-station-i2c-spi-smoke/bench.yaml \
  --suite examples/17-station-i2c-spi-smoke/spi-smoke.suite.yaml \
  --skip-flash
```

Update the expected I2C address/register values and SPI response bytes to match the real Station fixture before recording release evidence.

# Station I2C/SPI Smoke Suites

These suites are the P0 hardware smoke path for BenchCI Station buses.

## What To Edit

- `bench.yaml`: set the real `/dev/i2c-*` bus, `/dev/spidev*.*` bus/device, DUT identity, and fixture slot for the Station.
- `i2c-smoke.suite.yaml`: set the expected I2C sensor address and identity register bytes.
- `spi-smoke.suite.yaml`: set the expected SPI response bytes for the Station fixture.

## Run Locally On The Station Agent

```bash
benchci run --bench bench.yaml --suite i2c-smoke.suite.yaml --skip-flash
benchci run --bench bench.yaml --suite spi-smoke.suite.yaml --skip-flash
```

## Run Through BenchCI Cloud

```bash
benchci run --cloud --transport i2c --suite i2c-smoke.suite.yaml --skip-flash
benchci run --cloud --transport spi --suite spi-smoke.suite.yaml --skip-flash
```

Store the resulting run IDs in the release bundle used for P0 sign-off.

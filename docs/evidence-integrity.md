# Release Evidence Bundle Integrity

BenchCI release evidence bundles include integrity metadata that can be checked
without a BenchCI account, login, network connection, or cloud session.

## Integrity files

Each newly generated bundle contains:

- `MANIFEST.json`: a canonical JSON inventory of the bundle's evidence files
  and their SHA256 hashes.
- `SIGNATURE.json`: an Ed25519 signature over the exact `MANIFEST.json` bytes,
  plus the signing key ID and manifest SHA256. This file is present when bundle
  signing is configured.
- `PUBLIC_KEY.pem`: the corresponding Ed25519 public key in PEM format. This
  file is present with a signed bundle.

`HASHES.txt` remains in the bundle for compatibility with earlier BenchCI
releases.

## Verify a bundle offline

Run:

```bash
benchci releases verify bundle.zip
```

Verification checks every file listed in the manifest, reports missing,
changed, or unexpected files, and verifies the Ed25519 signature when one is
present. The command works fully offline and does not require an account.

For machine-readable output, add `--json`.

## Use the BenchCI public key as the trust anchor

The copy of `PUBLIC_KEY.pem` inside a bundle can prove only that its manifest,
signature, and embedded key are internally consistent. An attacker who could
replace the whole bundle could also replace all three.

For identity verification, download the BenchCI public key from its stable
publication URL and pass it explicitly:

```bash
curl -O https://benchci.dev/.well-known/benchci-signing-key.pem
benchci releases verify bundle.zip --public-key benchci-signing-key.pem
```

The explicit `--public-key` takes precedence over the key embedded in the ZIP.

## Scope

A successful verification proves that the files covered by the manifest are
unaltered since BenchCI generated and signed the bundle. It is not a
timestamping authority or a certification, and it does not attest that the
tests, test design, test environment, or reported conclusions were themselves
correct.

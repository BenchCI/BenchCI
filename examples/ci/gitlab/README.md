# GitLab CI example

This example shows how to run BenchCI from GitLab CI using a remote BenchCI Agent connected to real hardware.

## Files

- `.gitlab-ci.yml` — example GitLab CI pipeline
- `board.yaml` — BenchCI board configuration used by the agent
- `suite.yaml` — BenchCI test suite

## Required GitLab CI/CD variables

Configure these variables in your GitLab project:

- `BENCHCI_LICENSE`
- `BENCHCI_AGENT_URL`
- `BENCHCI_AGENT_TOKEN`

Example values:

- `BENCHCI_LICENSE=BCI-XXXXXXXX-XXXXXXXX`
- `BENCHCI_AGENT_URL=http://bench-agent.local:8080`
- `BENCHCI_AGENT_TOKEN=your-agent-token`

## Flow

1. GitLab runner installs BenchCI
2. BenchCI activates the license with `benchci login`
3. BenchCI submits the test run to the remote BenchCI Agent
4. BenchCI Agent flashes the board and runs the suite
5. GitLab stores the generated artifacts

## Notes

- The transport port in `board.yaml` refers to the machine running BenchCI Agent, not the GitLab runner.
- Replace `build/fw.elf` with your actual firmware artifact path.
- Replace the example board and suite files with your own tested configuration.

## Artifacts

BenchCI stores artifacts under:

```text
benchci-results/
```

Typical output includes:

- `results.json`
- `transport.log`
- `flash.log`
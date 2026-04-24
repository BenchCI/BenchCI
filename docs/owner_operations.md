# Owner Operations

This document describes the manual operations model for early BenchCI customers.

BenchCI currently uses manual onboarding and monthly invoicing rather than self-serve payment automation.

## Typical customer onboarding

1. Customer requests access through the website or email.
2. Customer creates a workspace at `https://app.benchci.dev`.
3. BenchCI owner reviews the customer request.
4. Invoice/payment is handled manually.
5. Owner activates the workspace plan/limits.
6. Owner creates or provides an Agent token if the customer will connect hardware.
7. Customer starts a cloud Agent.
8. Customer runs end-to-end validation.
9. Customer and BenchCI owner review dashboard results.

## Backend URL

Current hosted backend:

```text
https://benchci-backend.fly.dev
```

## Dashboard URL

```text
https://app.benchci.dev
```

## Manual plan activation

Workspace plan activation is handled through admin endpoints or owner tooling.

Recommended fields:

- plan
- status
- seat limit
- bench limit
- trial end date if applicable

## Agent token creation

Agent tokens should be created per customer/workspace or per lab Agent.

Keep tokens out of source control and rotate if leaked.

## First customer acceptance criteria

A customer is ready for pilot use when:

- they can register/login
- workspace is active
- Agent can connect
- bench appears in dashboard
- CLI can list benches
- Cloud Mode run can execute
- run events appear
- artifacts can be downloaded

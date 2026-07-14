# BenchCI Security Policy

BenchCI is a hardware CI and compliance-evidence platform. This policy explains how to report security vulnerabilities, what is in scope, how BenchCI handles reports, and how security updates are communicated.

This document is a public coordination policy. It is not a warranty, a certification statement, or legal advice.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately:

- Email: [tech@benchci.dev](mailto:tech@benchci.dev)
- Subject prefix: `Security:`

Include as much of the following as you safely can:

- affected component and version, if known
- steps to reproduce
- impact and likely severity
- whether customer data, firmware artifacts, Agent credentials, CI secrets, or workspace isolation may be affected
- proof-of-concept code, logs, screenshots, or packet captures
- whether the issue appears to be actively exploited
- your preferred contact details for follow-up

Do not include third-party secrets, customer firmware, personal data, or destructive exploit payloads unless BenchCI explicitly asks for a secure transfer method.

## Scope

The following BenchCI components are in scope:

- BenchCI CLI
- BenchCI Agent and Cloud Agent workflows
- BenchCI backend and cloud control plane
- BenchCI dashboard
- BenchCI public website and documentation
- BenchCI examples and configuration templates
- BenchCI Station software image, update tooling, and managed Station software configuration
- authentication, authorization, workspace isolation, Agent tokens, artifact handling, firmware handling, evidence bundles, billing integration metadata, and CI integration behavior

Out of scope for this coordinated disclosure process:

- customer-owned DUT firmware, customer test suites, or customer lab hardware
- vulnerabilities in third-party services unless they create a BenchCI-specific exposure
- denial-of-service testing against production systems without written permission
- social engineering, phishing, physical attacks, spam, and automated scanner noise without an exploitable BenchCI impact
- hardware electrical-safety or conformity issues for BenchCI Station hardware; report those to the same address, but they are triaged separately from software/cloud security

## Safe Harbor

BenchCI will not pursue legal action or account sanctions for good-faith security research that:

- stays within this policy,
- avoids privacy violations, data destruction, service disruption, and persistence,
- does not access, modify, delete, or exfiltrate data beyond what is needed to demonstrate the vulnerability,
- promptly reports the issue privately, and
- gives BenchCI a reasonable opportunity to investigate and remediate before public disclosure.

If you are unsure whether an action is safe, contact BenchCI first.

## Severity Levels

BenchCI uses the following initial severity model. Final severity may change after investigation.

| Severity | Examples |
| --- | --- |
| Critical | Cross-workspace data access; remote code execution in cloud or Agent context; theft of Agent tokens, user sessions, customer firmware, or CI secrets; active exploitation. |
| High | Authentication or authorization bypass; privilege escalation; persistent artifact exposure; significant vulnerability in update or firmware handling. |
| Medium | Limited information disclosure; scoped token misuse; security-control bypass requiring user interaction or unusual configuration. |
| Low | Hardening gaps, missing security headers, low-impact metadata exposure, documentation mistakes with limited exploitability. |

## Response Targets

BenchCI targets the following handling times for complete, reproducible reports:

| Severity | Acknowledge | Initial assessment | Target remediation |
| --- | ---: | ---: | ---: |
| Critical | 1 business day | 2 business days | 7 calendar days or faster when feasible |
| High | 2 business days | 5 business days | 30 calendar days |
| Medium | 5 business days | 10 business days | 90 calendar days |
| Low | 10 business days | next planned maintenance window | best-effort hardening |

Some issues require coordination with hosting, payment, email, package, operating-system, or hardware vendors. BenchCI will share status updates when a report remains open beyond its target.

## Coordinated Disclosure

Please do not publicly disclose a vulnerability until BenchCI has released a fix, mitigation, or advisory, or until a mutually agreed disclosure date.

BenchCI will normally:

1. acknowledge the report,
2. assign a tracking owner and severity,
3. reproduce and scope the issue,
4. identify affected versions, deployments, customers, and mitigations,
5. prepare and test a fix,
6. release an update or operational mitigation,
7. notify affected customers when needed, and
8. publish or share an advisory when appropriate.

BenchCI may delay public technical detail when disclosure would materially increase customer risk before customers have had a reasonable opportunity to patch or mitigate.

## Customer Notification

BenchCI will notify affected customers when a vulnerability or incident may have affected:

- workspace isolation,
- customer firmware artifacts or firmware URLs,
- evidence artifacts, logs, run metadata, or release bundles,
- user sessions, account credentials, Agent tokens, or API credentials,
- billing integration metadata, or
- availability of paid cloud services.

Notifications will include the known impact, affected components, remediation or mitigation steps, and any customer action required.

## Security Updates and Support Period

Security fixes are distributed through BenchCI CLI, Agent, backend, dashboard, website, and Station software releases as applicable.

BenchCI’s pilot-stage policy is:

- security fixes are provided for the currently supported BenchCI release line;
- customers should keep CLI, Agent, and Station software current;
- security-relevant updates are identified in release notes or direct customer advisories;
- managed customer deployments may receive direct update instructions or managed remediation from BenchCI; and
- BenchCI will publish a more formal support-period matrix before broad commercial launch.

## CRA Vulnerability Reporting Readiness

BenchCI maintains an internal Cyber Resilience Act (CRA) reporting checklist for products with digital elements. When a vulnerability may be actively exploited or may qualify as severe under applicable EU rules, BenchCI will run the CRA checklist in parallel with customer response.

The internal checklist is designed to support:

- early warning within 24 hours when required,
- vulnerability notification within 72 hours when required,
- final reporting after remediation or when the required information is available,
- SBOM and component evidence collection,
- customer mitigation communication, and
- retention of investigation records.

BenchCI’s CRA process does not change the reporting address above; security researchers should continue reporting privately to [tech@benchci.dev](mailto:tech@benchci.dev).

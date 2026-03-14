# Contributing to BenchCI

This document describes how development contributions are handled within the BenchCI project.

BenchCI source code is maintained in a private repository and developed internally.

External contributions are currently not accepted.

---

# Internal Development Guidelines

Development should follow these principles:

- keep CLI UX simple
- maintain deterministic test execution
- preserve compatibility with existing configuration files
- avoid breaking changes in test suite syntax

---

# Code Style

Python code should follow:

```
PEP8 guidelines
```

Formatting tools recommended:

```
black  
ruff  
```

Example:

```
black .
ruff check .
```

---

# Pull Requests

Internal contributors should ensure:

- code compiles
- new functionality includes tests where applicable
- documentation is updated if behavior changes

Pull requests should describe:

- the problem addressed
- the proposed solution
- any potential impact

---

# Documentation

Documentation should remain synchronized between:

public documentation repository  
private developer documentation

---

# Reporting Issues

Internal issues should be reported through the project's issue tracker.

Include:

- environment
- board configuration
- test suite
- logs

---

# Security Issues

Security-related issues must not be disclosed publicly.

Follow the guidelines in SECURITY.md.
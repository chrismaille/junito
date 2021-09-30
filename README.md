## Junito Action

[![release](https://img.shields.io/github/release/chrismaille/junito.svg)](https://github.com/chrismaille/junito/releases/latest)
[![Tests](https://github.com/chrismaille/junito/workflows/tests/badge.svg)](https://github.com/chrismaille/junito/actions)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

This Action parses and logs JUnit report results in Actions console. You can define if Action will stop for
failed and or skipped tests.

### Usage

Just Add the Action, with the name for the generated JUnit report:

```yml
- name: Check Failed Tests
  uses: chrismaille/junito@v1
  with:
    filename: my-junit-report.xml
    stop_on_errors: true     # stops at any error/failed tests found
    stop_on_skipped: false   # stops at any skipped test found
```

### Defaults

Current default settings are:

```yaml
filename: test-report.xml
stop_on_failed: true
stop_on_skipped: false
```

### Workflow Example:

```yaml
name: test

on: pull_request

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v2
      - name: Set up python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install Poetry
        uses: snok/install-poetry@v1
      - name: Install Project
      - runs: |
          poetry install
      - name: Generate XML report
      - runs: |
          poetry run pytest --cov=. --cov-report xml --junit-xml=test-report.xml || true
      # Will test against test-report.xml and stops at any failed/error test found.
      - name: Check Failed Tests
        uses: chrismaille/junito@v1
```

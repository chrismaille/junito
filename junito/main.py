"""Junito - JUnit XML Parser.

    Why check for unit test errors here and not during pytest running?

    All Pytest reports must be sent to SonarQube, regardless of success or not,
    but Pull Requests must be marked as failure, when these errors occur.

    Unfortunately SonarQube 9.0 Quality Gate did not fail the PR on unit
    test errors. So we need to check this manually on the Github Actions
    Pull Request workflow.

"""
import sys

import click
from junitparser import JUnitXml

from junito.junito import Junito


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def check(filename):
    """Check Pytest Junit Report for errors."""
    pytest_report = JUnitXml.fromfile(filename)
    click.echo(f"\nReading file: {filename}...\n")
    checker = Junito(report=pytest_report)
    checker.process()

    if checker.block_issues > 0:
        click.echo(
            click.style(
                f"\nFailure: Found {checker.block_issues} failed tests.", fg="red"
            )
        )
        sys.exit(1)
    click.echo(click.style("\nSuccess: No failed tests found.", fg="green"))

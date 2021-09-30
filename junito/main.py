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
from asbool import asbool
from junitparser import JUnitXml

from junito.junito import Junito


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.argument("stop_on_failed")
@click.argument("stop_on_skipped")
def check(filename, stop_on_failed, stop_on_skipped):
    """Check Pytest Junit Report for errors."""
    pytest_report = JUnitXml.fromfile(filename)

    click.echo(f"\nReading file:               {filename}")
    click.echo(f"Stop on Error/Failed Tests: {stop_on_failed}")
    click.echo(f"Stop on Skipped Tests:      {stop_on_skipped}\n")

    checker = Junito(report=pytest_report)
    checker.process()

    exit_code = checker.get_exit_code(asbool(stop_on_failed), asbool(stop_on_skipped))

    if exit_code:
        label = "Failure"
        color = "red"
        message = "Found {}{}{}.".format(
            f"{checker.failed_tests} failed tests" if checker.failed_tests else "",
            " and " if checker.failed_tests and checker.skipped_tests else "",
            f"{checker.skipped_tests} skipped tests" if checker.skipped_tests else "",
        )
    else:
        label = "Failure"
        color = "red"
        message = "Success: No failed tests found"

    click.echo(click.style(f"\n{label}: {message}.", fg=color))
    sys.exit(exit_code)

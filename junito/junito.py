from dataclasses import dataclass
from typing import Tuple

import click
from junitparser import JUnitXml
from junitparser.junitparser import Result


@dataclass
class Junito:
    """Process JUnit XML Report Files."""

    report: JUnitXml
    block_issues: int = 0

    def process(self):
        for suite in self.report:
            self.message_stats(suite)
            self.show_issues(suite)

    @staticmethod
    def show_message(text: str, color: str = "bright_white"):
        """Show formatted text in terminal."""
        click.echo(click.style(text, fg=color))

    def message_stats(self, suite: JUnitXml):
        """Show Report main stats per Test Suite."""
        self.block_issues += suite.errors + suite.failures
        self.show_message(f"Suite: {suite.name.title()}", "blue")
        self.show_message(f"Total Tests: {suite.tests}")
        self.show_message(f"Errors: {suite.errors}", "red" if suite.errors else "green")
        self.show_message(
            f"Failures: {suite.failures}", "red" if suite.failures else "green"
        )
        self.show_message(
            f"Skipped: {suite.skipped}", "yellow" if suite.skipped else "green"
        )
        self.show_message(f"Time: {suite.time}\n", "white")

    @staticmethod
    def get_text(result: Result) -> Tuple[str, str, str]:
        is_skip = "skip" in (getattr(result, "type") or "") or not result.message
        label_message = "REASON" if is_skip else "MESSAGE"
        message = f" ({label_message}: {result.message})" if result.message else ""
        return ("SKIPPED", message, "yellow") if is_skip else ("FAILED", message, "red")

    def show_issues(self, suite: JUnitXml):
        """Show Issues in Terminal."""
        for case in suite:
            for result in case.result:
                label, message, color = self.get_text(result)
                self.show_message(
                    f"* {label}: {case.classname}.{case.name}{message}", color
                )

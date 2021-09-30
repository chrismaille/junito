from pathlib import Path

import pytest
from click.testing import CliRunner

from junito.junito import Junito
from junito.main import check


def test_process(test_report, capfd):
    # Arrange
    instance = Junito(test_report)

    # Act
    instance.process()
    out, err = capfd.readouterr()

    # Assert
    assert (
        "* FAILED: transactional_risk.tests.test_views.test_get_transactional_risk"
        in out
    )
    assert "* SKIPPED: transactional_risk.tests.test_secrets.test_get_secrets" in out


def test_show_message(test_report, capfd):
    # Arrange
    instance = Junito(test_report)

    # Act
    instance.show_message("foo-bar", "red")
    out, err = capfd.readouterr()

    # Assert
    assert "foo-bar" in out


def test_message_stats(test_report, capfd):
    # Arrange
    instance = Junito(test_report)

    # Act
    instance.message_stats(next(iter(test_report)))
    out, err = capfd.readouterr()

    # Assert
    assert "Total Tests: 8" in out
    assert "Failures: 1" in out
    assert "Errors: 0" in out
    assert "Skipped: 2" in out
    assert "Time: 21.125" in out


def test_get_text(test_report, capfd):
    # Arrange
    instance = Junito(test_report)
    suite = next(iter(test_report))
    case_list = [case for case in suite if case.result]

    # Act
    label, message, color = instance.get_text(case_list[0].result[0])

    # Assert
    assert label == "FAILED"
    assert (
        message
        == " (MESSAGE: transactional_risk.models.TransactionalRisk.DoesNotExist: "
        "TransactionalRisk matching query does not exist.)"
    )
    assert color == "red"


def test_show_issues(test_report, capfd):
    # Arrange
    instance = Junito(test_report)
    suite = next(iter(test_report))

    # Act
    instance.show_issues(suite)
    out, err = capfd.readouterr()

    # Assert
    assert out.count("SKIPPED") == 2
    assert out.count("FAILED") == 1
    assert out.count("REASON") == 1
    assert out.count("MESSAGE") == 1


@pytest.mark.parametrize(
    "stop_on_errors, stop_on_skipped, expected_exit_code",
    [
        ("true", "false", 1),
        ("true", "true", 1),
        ("false", "true", 1),
        ("false", "false", 0),
    ],
)
def test_runner(stop_on_errors, stop_on_skipped, expected_exit_code):
    # Arrange
    runner = CliRunner()
    filename = Path().joinpath("tests", "fixtures", "test-report.xml")

    # Act
    result = runner.invoke(check, [str(filename), stop_on_errors, stop_on_skipped])

    # Assert
    assert result.exit_code == expected_exit_code

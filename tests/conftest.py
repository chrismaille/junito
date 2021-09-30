from pathlib import Path

import pytest
from junitparser import JUnitXml


@pytest.fixture
def test_report():
    filename = Path().joinpath("tests", "fixtures", "test-report.xml")
    pytest_report = JUnitXml.fromfile(str(filename))
    return pytest_report

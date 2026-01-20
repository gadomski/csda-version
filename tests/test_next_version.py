import pytest

from csda_version import get_next_csda_version, get_next_version


@pytest.mark.parametrize(
    "csda_version,tag,expected",
    [
        ["26.1.1", "v26.1.1.0", "26.1.1-1"],
        ["26.1.1", "v26.1.1.1", "26.1.1-2"],
        ["26.1.2", "v26.1.1.1", "26.1.2-0"],
        ["26.1.2", "", "26.1.2-0"],
        ["26.1.1", "v26.1.1-0", "26.1.1-1"],
        ["26.1.1", "v26.1.1-1", "26.1.1-2"],
        ["26.1.2", "v26.1.1-1", "26.1.2-0"],
    ],
)
def test_get_next_version(csda_version: str, tag: str, expected: str) -> None:
    assert get_next_version(csda_version, tag) == expected


@pytest.mark.parametrize(
    "date,csda_version,expected",
    [
        ["2026-01-25", "26.2.1", "26.2.2"],
        ["2026-10-01", "26.4.4", "27.1.0"],
        ["2027-01-01", "27.1.3", "27.2.0"],
    ],
)
def test_get_next_csda_version(date: str, csda_version: str, expected: str) -> None:
    assert get_next_csda_version(date, csda_version) == expected

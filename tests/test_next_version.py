import pytest

from csda_version import get_next_version


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

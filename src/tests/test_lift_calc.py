import pytest

from lift_calc import __version__


def test_version():
    with open("./pyproject.toml", "r") as pyproject_file:
        for line in pyproject_file:
            if "version = " in line:
                version = line.split("version = ")[-1].strip().strip('"')
                assert version == __version__
                return
        else:
            pytest.fail("No version line")

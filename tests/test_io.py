import pytest

from zippy.io import read_file, write_file


def test_read_file_ok():
    sample = read_file(path="data/sample.txt")

    assert sample == "a sample"


def test_read_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
       read_file(path="data/does_not_exist.txt")


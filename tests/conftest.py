from pytest import fixture

from pathlib import Path

import os
import pytest


@pytest.fixture
def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


@fixture
def test_board_1_text(rootdir):
    file = Path(rootdir).joinpath(Path(r"data\board_1.txt"))
    return file.resolve()

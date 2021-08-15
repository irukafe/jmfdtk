import os
from pathlib import Path
from jmfdtk.khcodegen import (
    _generate,
    _write_code,
    _write_compound,
)
from jmfdtk import JMFD_PATH
import filecmp
import pytest

DATA_DIR = os.path.join(Path(__file__).parent.parent.absolute(), 'khcoder_coding_files')


@pytest.fixture(scope='module')
def code_data():
    return _generate(jmfd_path=JMFD_PATH, exclude_general=True)


def test_code_jmf(tmpdir, code_data):
    path_ans = os.path.join(DATA_DIR, 'code_jmf.txt')

    code = code_data[0]
    f = tmpdir.join('code_jmf.txt')
    _write_code(f.strpath, code)
    assert filecmp.cmp(path_ans, f.strpath)


def test_code_jmfw(tmpdir, code_data):
    path_ans = os.path.join(DATA_DIR, 'code_jmfw.txt')

    code = code_data[1]
    f = tmpdir.join('code_jmfw.txt')
    _write_code(f.strpath, code)
    assert filecmp.cmp(path_ans, f.strpath)


def test_compound_jmf(tmpdir, code_data):
    path_ans = os.path.join(DATA_DIR, 'compound_jmf.txt')

    compound = code_data[2]
    f = tmpdir.join('compound_jmf.txt')
    _write_compound(f.strpath, compound)
    assert filecmp.cmp(path_ans, f.strpath)

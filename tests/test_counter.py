import os
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal
from jmfdtk import jmfcounter
import pytest

FOUNDATIONS = ('HarmVirtue', 'HarmVice', 'FairnessVirtue', 'FairnessVice', 'IngroupVirtue',
               'IngroupVice', 'AuthorityVirtue', 'AuthorityVice', 'PurityVirtue', 'PurityVice')

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


@pytest.fixture(scope='module')
def count_data():
    path = Path(os.path.realpath(__file__))
    kokoro = pd.read_csv(
        os.path.join(path.parent.parent.absolute(), 'kokoro', 'kokoro.csv'),
        header=0)
    texts = kokoro['text'].tolist()
    return jmfcounter(texts)


def test_dfmfw(count_data):
    dfmfw = count_data.dfmfw

    dfmfw_ans = {}
    for f in FOUNDATIONS:
        df = pd.read_csv(os.path.join(DATA_DIR, f+'.csv'), header=0, encoding='utf_8_sig')
        dfmfw_ans[f] = df

    for f in FOUNDATIONS:
        assert_frame_equal(dfmfw_ans.get(f), dfmfw.get(f))


def test_dfmf(count_data):
    dfmf = count_data.dfmf
    dfmf_ans = pd.read_csv(os.path.join(DATA_DIR, 'dfmf.csv'), index_col=0, header=0,
                           encoding='utf_8_sig')

    assert_frame_equal(dfmf_ans, dfmf)


def test_cumfw(count_data):
    cumfw = count_data.cumfw
    cumfw_ans = pd.read_csv(os.path.join(DATA_DIR, 'cumfw.csv'), header=0, encoding='utf_8_sig')

    assert_frame_equal(cumfw_ans, cumfw)

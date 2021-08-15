import os
import pandas as pd
from pandas.testing import assert_frame_equal
from jmfdtk import clustering

FOUNDATIONS = ['HarmVirtue', 'HarmVice', 'FairnessVirtue', 'FairnessVice', 'IngroupVirtue',
               'IngroupVice', 'AuthorityVirtue', 'AuthorityVice', 'PurityVirtue', 'PurityVice']

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def test_clustering():
    df_clust_ans = pd.read_csv(os.path.join(DATA_DIR, 'kokoro_clust.csv'), header=0,
                               encoding='utf_8_sig')

    df_clust_ans['clust'] = df_clust_ans['clust'].astype('int32')

    cumfw = pd.read_csv(os.path.join(DATA_DIR, 'cumfw.csv'), header=0, encoding='utf_8_sig')
    df_clust = clustering(cumfw, FOUNDATIONS)

    assert_frame_equal(df_clust_ans, df_clust[['texts', 'clust']])

"""Module to calculate document frequency of J-MFD words and moral foundations.
"""
import os
from pathlib import Path
from collections import Counter
from typing import NamedTuple
import errno

import numpy as np
import pandas as pd
import MeCab
import ipadic

from jmfdtk.utils import _display, _display_md
from jmfdtk.jmfdloader import load_jmfd
from jmfdtk.khcodegen import _generate
from jmfdtk import JMFD_PATH

# J-MFD words which are treated as compound.
# These words are compared with 2-grams and 3-grams.
_, _, JMFD_COMPOUND = _generate(jmfd_path=JMFD_PATH, exclude_general=True)

# Target POS.
# '助動詞' is for '母親らしい' in J-MFD and '助動詞' terms will be removed after morphological analysis.
TARGET_POS = ['名詞', '動詞', '形容詞', '副詞', '助動詞']


class CountData(NamedTuple):
    """Class to store counting results.
    """

    dfmfw: dict
    dfmf: pd.DataFrame
    cumfw: pd.DataFrame
    foundation: tuple

    def show_dfmfw(self):
        for foundation, df in self.dfmfw.items():
            _display_md('### Document frequency: {}'.format(foundation))
            _display(df)

    def show_dfmf(self):
        _display_md('### Document frequency of moral foundation')
        _display(self.dfmf)

    def describe_cumfw(self):
        _display_md('### Descriptibe statistics of unique moral foundation word count')
        _display(self.cumfw[self.foundation].describe())


def _load_jmfwords(jmfd_path, jmfd_excluded):
    """Loads moral foundation words and stems from J-MFD.
    """

    mfd, _ = load_jmfd(jmfd_path)

    # Removes MoralityGeneral foundation.
    mfd = mfd[~(mfd['foundation'] == 'MoralityGeneral')]

    # Removes specified words.
    if len(jmfd_excluded) > 0:
        mfd = mfd[~mfd['word'].isin(jmfd_excluded)]

    mfword = {}
    mfstem = {}
    _display_md('### Loaded JMFD words')
    for foundation, g in mfd.groupby('foundation'):
        mfstem[foundation] = g[g['stem']]['word'].tolist()
        mfword[foundation] = g[~g['stem']]['word'].tolist()
        print('{} ==> stem:{} word:{}'.format(foundation, len(mfstem[foundation]),
                                              len(mfword[foundation])))
    print()

    return mfword, mfstem


def _get_ngram(words, n):
    return [''.join(words[idx:idx + n]) for idx in range(len(words) - n + 1)]


def _find_compound(morphe, ngram, n):
    """Finds compound moral foundation words.
    """

    mfd_words = list(set(ngram).intersection(set(JMFD_COMPOUND)))

    if len(mfd_words) == 0:
        return morphe

    # Updates current morpheme list.
    for w in mfd_words:
        # Searches for indices of a word which matches n-gram words.
        indices = [i for i, x in enumerate(ngram) if w in x]

        for idx in indices:
            # Replaces the current word with a word from MFD.
            morphe[idx][0] = w

            for i in range(1, n):
                # Sets '*' for a morpheme which will be removed.
                morphe[idx+i][0] = '*'

    # Removes morphemes with '*'.
    return [m for m in morphe if m[0] != '*']


def _segment(m, texts, stop_list):
    """Morphological analysis.
    """

    low = []
    for t in texts:
        node = m.parseToNode(t)
        morphe = []
        while node:
            feature_split = node.feature.split(',')
            pos = feature_split[0]

            if pos in TARGET_POS:
                # When '*' is set as base form, the surface will be used instead.
                base_form = node.surface if feature_split[6] == '*' else feature_split[6]
                if base_form not in stop_list:
                    morphe.append([base_form, pos])

            node = node.next

        # Searches for moral foundation words which are segmented into multiple tokens.
        if len(morphe) >= 2:
            # Searches from bi-gram.
            words = [m[0] for m in morphe]
            bigram = _get_ngram(words, 2)
            morphe = _find_compound(morphe, bigram, 2)

            if len(morphe) >= 3:
                # Searches from tri-gram.
                trigram = _get_ngram(words, 3)
                morphe = _find_compound(morphe, trigram, 3)

        # Removes '助動詞'.
        words = [m[0] for m in morphe if m[1] != '助動詞']

        low.append(words)

    return low


def _get_mfword(words, mfs, stems):
    """Gets unique moral foundation words. Stems are treated as word.
    """

    # Moral foundation word list.
    mfl = mfs + stems
    mfw = list(set(words).intersection(set(mfl)))
    return Counter(mfw)


def _count(low, mfword, mfstem, texts):
    """Counts documents which contain moral foundation words.
    """

    foundations = mfword.keys()
    unm_foundation = len(mfword)

    # Document frequency of moral foundation words.
    dfmfw = {}
    for f in foundations:
        dfmfw[f] = Counter()

    # Appearance of moral foundation words.
    amfw = np.empty((0, unm_foundation), int)

    # Counts of unique moral foundation word in each document.
    cumfw = np.empty((0, unm_foundation), int)

    num_doc = len(low)
    for i, words in enumerate(low):
        print('{}/{}\r'.format(i, num_doc), end='')
        row = np.zeros(unm_foundation, int)
        row_prop = np.zeros(unm_foundation, int)
        for idx, (foundation, mfs, stems) in enumerate(zip(foundations, mfword.values(),
                                                       mfstem.values())):
            counter_res = _get_mfword(words, mfs, stems)
            dfmfw[foundation] += counter_res

            soc = sum(counter_res.values())
            row[idx] = 1 if soc > 0 else 0
            row_prop[idx] = soc

        amfw = np.append(amfw, row)
        cumfw = np.append(cumfw, row_prop)

    # Stores document frequency of moral foundation words in dict of DataFrame.
    dict_dfmfw = {}
    for foundation in foundations:
        # Sorts by key and then value
        dfmfw_sorted = dict(sorted(sorted(dfmfw[foundation].items()), key=lambda x: x[1],
                                   reverse=True))
        df = pd.DataFrame({
            'word': dfmfw_sorted.keys(),
            'count': dfmfw_sorted.values(),
            'percent': [v / num_doc * 100 for v in dfmfw_sorted.values()]})
        dict_dfmfw[foundation] = df

    # Stores document frequency of moral foundations in DataFrame.
    df_amfw = pd.DataFrame(amfw.reshape([-1, unm_foundation]), columns=foundations)
    sr_dfmf = df_amfw.sum()
    sr_dfmf.name = 'count'
    df_dfmf = sr_dfmf.to_frame()
    df_dfmf['percent'] = df_dfmf['count'] / num_doc * 100

    # Stores counts of unique moral foundation word and texts in DataFrame.
    df_cumfw = pd.DataFrame(cumfw.reshape([-1, unm_foundation]), columns=foundations)
    df_cumfw['sum'] = df_cumfw.sum(axis=1)
    df_cumfw['texts'] = texts

    # Removes data without moral foundation words.
    df_cumfw = df_cumfw[df_cumfw['sum'] > 0]
    df_cumfw.drop(columns=['sum'], inplace=True)

    print('Counting completed.')
    return CountData(dict_dfmfw, df_dfmf, df_cumfw, foundations)


def jmfcounter(texts, stop_list=[], jmfd_path=None, jmfd_excluded=[], dicdir=None):
    """
    Args:
        texts (list): List of list of word.
        stop_list (list, optional): Stop words. Defaults to [].
        jmfd_path (str, optional): Path of J-MFD file. Defaults to None.
        jmfd_excluded (list, optional): Excluded words in J-MFD. Defaults to [].
        dicdir (str, optional): Path of MeCab dictionary. Defaults to None.

    Returns:
        CountData containing results of J-MFD word counting.

    Raises:
        FileNotFoundError: Nonexistence of MeCab dictionary directory.
        FileNotFoundError: Nonexistent path of JMFD file.
    """

    print('Document number: {}'.format(len(texts)))
    if len(stop_list) > 0:
        _display_md('### Stop words')
        print(stop_list)
    if len(jmfd_excluded) > 0:
        _display_md('### Excluded moran foundation words')
        print(jmfd_excluded)

    if dicdir:
        dic = Path(dicdir)
        if not dic.is_dir():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dic)

        m = MeCab.Tagger('-d ' + dicdir + '-r /dev/null')
    else:
        m = MeCab.Tagger(ipadic.MECAB_ARGS)

    m.parse('')

    if jmfd_path is None:
        jmfd_path = JMFD_PATH
    else:
        jmfd = Path(jmfd_path)
        if not jmfd.is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), jmfd_path)

    mfword, mfstem = _load_jmfwords(jmfd_path, jmfd_excluded)
    print('Loading J-MFD completed.')

    low = _segment(m, texts, stop_list)
    print('Segmentation completed.')

    return _count(low, mfword, mfstem, texts)

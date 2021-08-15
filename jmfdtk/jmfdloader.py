"""Module to load j-MFD as Pandas DataFrame.
"""
import re
import pandas as pd


class JMFDFormatError(Exception):
    pass


def load_jmfd(jmfd_path):
    """Loads j-MFD as Pandas DataFrame.

    Args:
        jmfd_path (str): Path of J-MFD.

    Raises:
        JMFDFormatError: J-MFD format error.

    Returns:
        pandas.DataFrame: Pandas DataFrame of loaded j-MFD with word, existence of stem, foundation
                            id and foundation columns.
        dict: A dict mapping ids to the corresponding Moral foundation.
    """
    with open(jmfd_path, mode='r') as f:
        text = f.read()

    splitted = text.split('%')

    if len(splitted) != 3:
        raise JMFDFormatError('Invalid JMFD format.')

    text_cat = splitted[1].strip()
    text_dic = splitted[2].strip()

    # Creates a dict mapping ids to the corresponding Moral foundation.
    foundation = {}
    for t in text_cat.splitlines():
        fid, cat = t.strip().split('\t')
        foundation[fid] = cat

    # Gets moral foundation words and ids.
    words = []
    fids = []
    for t in text_dic.splitlines():
        text_splitted = re.split('\t+', t.strip())

        for i in range(1, len(text_splitted)):
            words.append(text_splitted[0].strip())
            fids.append(text_splitted[i].strip())

    # Creates DataFrame containing loaded J-MFD.
    df = pd.DataFrame({
        'word': [w.replace('*', '') for w in words],
        'stem': [w.endswith('*') for w in words],
        'fid': fids,
        'foundation': [foundation[i] for i in fids]
    })

    return df, foundation

from jmfdtk import load_jmfd, JMFD_PATH


def test_load_jmfd():
    df, foundation = load_jmfd(JMFD_PATH)

    f_ans = {
        'HarmVirtue': 51,
        'HarmVice': 93,
        'FairnessVirtue': 43,
        'FairnessVice': 34,
        'IngroupVirtue': 99,
        'IngroupVice': 42,
        'AuthorityVirtue': 130,
        'AuthorityVice': 52,
        'PurityVirtue': 90,
        'PurityVice': 88,
        'MoralityGeneral': 43
    }

    foundation_ans = {
        '01': 'HarmVirtue',
        '02': 'HarmVice',
        '03': 'FairnessVirtue',
        '04': 'FairnessVice',
        '05': 'IngroupVirtue',
        '06': 'IngroupVice',
        '07': 'AuthorityVirtue',
        '08': 'AuthorityVice',
        '09': 'PurityVirtue',
        '10': 'PurityVice',
        '11': 'MoralityGeneral'
    }

    for f, v in df['foundation'].value_counts().items():
        assert f_ans[f] == v, '{} count does not match.'.format(f)

    assert foundation == foundation_ans

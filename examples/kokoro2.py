"""Example of jmfdtk usage. This example shows how to merge Virtue with Vice and run clustering with
   the merged results.
"""
import os
from pathlib import Path
import pandas as pd
import jmfdtk


def kokoro2():
    # Reads segmented kokoro texts.
    path = Path(os.path.realpath(__file__))
    df = pd.read_csv(os.path.join(path.parent.parent.absolute(), 'kokoro', 'kokoro.csv'), header=0)

    # Counts JMFD words.
    texts = df['text'].tolist()
    count_data = jmfdtk.jmfcounter(texts)

    # Shows count results.
    count_data.show_dfmfw()
    count_data.show_dfmf()
    count_data.describe_cumfw()

    # Combines Virtue with Vice.
    df_mfd = count_data.cumfw.copy()
    df_mfd['Purity'] = df_mfd['PurityVirtue'] + df_mfd['PurityVice']
    df_mfd['Authority'] = df_mfd['AuthorityVirtue'] + df_mfd['AuthorityVice']
    df_mfd['Fairness'] = df_mfd['FairnessVirtue'] + df_mfd['FairnessVice']
    df_mfd['Harm'] = df_mfd['HarmVirtue'] + df_mfd['HarmVice']
    df_mfd['Ingroup'] = df_mfd['IngroupVirtue'] + df_mfd['IngroupVice']
    df_mfd.drop(columns=count_data.foundation, inplace=True)
    # df_mfd.info()

    # Runs clustering of segmented texts based on JMFD word count.
    df_clust = jmfdtk.clustering(df_mfd, ['Purity', 'Authority', 'Fairness', 'Harm', 'Ingroup'])

    # Display average word count of each moral foundation.
    groups = df_clust.groupby('clust').mean()
    ax = groups.plot.bar(linewidth=2, align='center', alpha=0.75, rot=0)
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Average word count')


if __name__ == '__main__':
    kokoro2()

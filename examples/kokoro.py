"""Example of jmfdtk usage.
"""
import os
from pathlib import Path
import csv
import pandas as pd
import jmfdtk


def write_khcsv(df, path):
    with open(path, mode='w', encoding='utf_8_sig', errors='ignore') as f:
        df[['texts', 'clust']].to_csv(f, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


def write_results(count_data):
    for foundation, df in count_data.dfmfw.items():
        df.to_csv(foundation+'.csv', index=False, header=True, encoding='utf_8_sig')

    count_data.dfmf.to_csv('./dfmf.csv', index=True, header=True, encoding='utf_8_sig')
    count_data.cumfw.to_csv('./cumfw.csv', index=False, header=True, encoding='utf_8_sig')


def kokoro():
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

    # Saves csv files of count results.
    # write_results(count_data)

    # Runs clustering of segmented texts based on JMFD word count.
    df_clust = jmfdtk.clustering(count_data.cumfw, count_data.foundation)

    # Saves a csv containing segmented texts with the clustering result.
    # This csv can be used for KH Coder.
    # write_khcsv(df_clust, './kokoro_clust.csv')

    # Display average word count of each moral foundation.
    groups = df_clust.groupby('clust').mean()
    ax = groups.plot.bar(linewidth=2, align='center', alpha=0.75, rot=0)
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Average word count')


if __name__ == '__main__':
    kokoro()

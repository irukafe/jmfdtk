"""Module to run hierarchical clustering and display the results.
"""
import sys
from collections import Counter
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt

from jmfdtk.utils import _display, _display_md


def _show_cluster_result(clust):
    counter = Counter(clust)
    _display_md('### Result of clustering')
    for c, cnt in sorted(counter.items()):
        print('Cluster {}: {}'.format(c, cnt))


def _get_cluster(Z, hclust_th):
    if hclust_th is None:
        longest_dist = Z[-1, 2]
        hclust_th = longest_dist * 0.7

    # Creates flat cluster based on distance.
    print('Threshhold: {}'.format(hclust_th))
    return fcluster(Z, hclust_th, criterion='distance')


def _show_dendrogram(Z):
    plt.figure(figsize=(14, 5))
    plt.ylabel('Distance')

    # color_threshold: default = 0.7*max(Z[:,2])
    dendrogram(
        Z,
        leaf_rotation=90.,
        leaf_font_size=8.,
        truncate_mode='lastp',
        p=100
    )

    if 'ipykernel' in sys.modules:
        _display_md('### Dendrogram')
        plt.show()
    else:
        print('Showing dendrogram skipped.')


def _hclustering(df):
    X = StandardScaler().fit_transform(df)

    return linkage(pdist(X, metric='euclidean'), method='ward')


def clustering(mfwc, foundations, hclust_th=None):
    df = mfwc.copy()
    Z = _hclustering(df[foundations])
    _show_dendrogram(Z)
    clust = _get_cluster(Z, hclust_th)
    df['clust'] = clust
    _show_cluster_result(clust)

    _display_md('### Average word counts of each moral foundation')
    groups = df.groupby('clust').mean()
    _display(groups)

    return df

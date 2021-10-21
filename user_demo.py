#!/usr/bin/env python

from testbench import Testbench
import random

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
Testbench.author('Petar Petrović')


def k_means(data: np.ndarray) -> np.ndarray:
    number_of_clusters = 5
    preprocessor = Pipeline(
        [
            ("scaler", MinMaxScaler()),
        ]
    )
    clusterer = Pipeline(
        [
            (
                "kmeans",
                KMeans(
                    n_clusters=number_of_clusters,
                    init="k-means++",
                    n_init=50,
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )
    pipe = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("clusterer", clusterer)
        ]
    )
    pipe.fit(data)
    predicted_labels = pipe["clusterer"]["kmeans"].labels_

    return predicted_labels


if __name__ == '__main__':
    Testbench(k_means)

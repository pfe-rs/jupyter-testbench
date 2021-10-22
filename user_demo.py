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


def kNN(X_test: np.ndarray, X_train: np.ndarray, Y_train: np.ndarray, k: int) -> np.ndarray:
    predictions = []

    for test_point in X_test:
        min_dist = []
        # za svaku vrednost iz seta za treniranje izračunati Euklidsku distancu od vrednosti iz test seta
        # i beležiti u nizu min_dist
        for i, point in enumerate(X_train):
            d1 = (point[0] - test_point[0]) ** 2
            d2 = (point[1] - test_point[1]) ** 2
            dist = np.sqrt(d1 + d2)
            # append the calculated distance in a list
            min_dist.append((i, dist))
        # sortiranje Euklidskih udaljenosti u nerastućem poretku
        min_dist.sort(key=lambda x: x[1])

        neighbours = min_dist[:k]
        # get index of the minimum distances
        idx = []
        for tup in neighbours:
            idx.append(tup[0])
        # check which label has majority
        output = Y_train[idx]
        values, counts = np.unique(output, return_counts=True)
        # return label with majority occurence
        max_idx = np.argmax(counts)
        predicted_label = values[max_idx]
        predictions.append(predicted_label)

    return np.array(predictions)

if __name__ == '__main__':
    Testbench(k_means)
    Testbench(kNN)

#!/usr/bin/env python

from typing import Any
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


# Helpers for logistical regression
def load_data(name: str):
    df = pd.read_csv(name)
    clean_df = pd.DataFrame()
    for col in ["PC1", "PC2"]:
        clean_df[col] = df[col]
    targets = (df["NObeyesdad"] == 3).astype(int).rename("Obese")
    return clean_df, targets
def hypothesis(X, B):
    z = np.dot(B, X.T)
    return np.clip(1/(1+np.exp(-(z))), 0.000001, 0.9999999)
def cost(y, h):
    return -(1/len(y)) * np.sum(y*np.log(h) + (1-y)*np.log(1-h))


def logistical_regression(X, y, B, alpha, epochs) -> Any:
    h = hypothesis(X, B)
    cost_history = [cost(y, h)] 
    for _ in range(0, epochs):
        h = hypothesis(X, B)
        for i in range(0, len(X.columns)):
            B[i] -= alpha * np.mean((h-y)*X.iloc[:, i])
        cost_history.append(cost(y, h))
    return cost_history, B


if __name__ == '__main__':
    Testbench(k_means)
    Testbench(kNN)
    Testbench(logistical_regression)

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


def kNN(X_test: np.ndarray, X_train: np.ndarray, Y_train: np.ndarray) -> np.ndarray:
    predictions = []

    k = 15
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


def logistical_regression(X: np.ndarray, y: np.ndarray, B: np.ndarray, alpha: float, epochs: int) -> Any:
    h = hypothesis(X, B)
    cost_history = [cost(y, h)] 
    for _ in range(0, epochs):
        h = hypothesis(X, B)
        for i in range(0, len(X.columns)):
            B[i] -= alpha * np.mean((h-y)*X.iloc[:, i])
        cost_history.append(cost(y, h))
    return cost_history, B


def classify(apriori: np.ndarray, conditional: np.ndarray, pc1: int, pc2: int) -> int:
    pc1 = int(pc1)
    pc2 = int(pc2)
    not_obs = apriori[0] * conditional[0, 0, pc1] * conditional[1, 0, pc2]
    obs = apriori[1] * conditional[0, 1, pc1] * conditional[1, 1, pc2]
    return int(np.argmax([not_obs, obs]))

def bayes_train(X: np.ndarray, Y: np.ndarray, num_of_buckets=20) -> tuple:
    # Calculate apriori probability
    apriori_prob = np.zeros(2)
    apriori_prob[0] = np.sum(Y == 0) / len(Y)
    apriori_prob[1] = np.sum(Y == 1) / len(Y)

    # Conditional probability
    conditional_prob = np.zeros((2, 2, num_of_buckets+1))
    for pc in range(2):
        features = X[:, pc]
        for i in range(2):
            cnt = np.sum(Y == i)
            for val in range(num_of_buckets+1):
                conditional_prob[pc, i, val] = (np.sum(features[Y == i] == val) + 1) / cnt

    return apriori_prob, conditional_prob

def covariance_reduce(X: pd.DataFrame, targets: pd.DataFrame, N: int = 10) -> np.ndarray:
    # Potrebno je prvo spojiti DataFrame-ove fičera i klasa u jedan, 
    # a onda izračunati korelacionu matricu (funkcija .corr() može biti korisna ovde)
    xy = pd.concat([X, targets], axis=1)
    target_cov = xy.corr().to_numpy()[:-1, -1]

    # Izdvojiti top N fičera na osnovu poslednje kolone korelacione matrice
    # Hint 1: Za pronalaženje najvećih korelacija može koristiti funkcija np.argsort,
    #         ili prolasci for petljama
    sorted_idx = np.argsort(target_cov)[::-1]
    X_new = X.to_numpy()[:, sorted_idx[: N]]
    return X_new

def pca(X: np.array, M: int) -> np.ndarray:

    # Step 1: Izračunaj kovariacionu matricu od X.T
    # Step 2: Izračunaj sopstvene vrednosti i vektore
    # Step 3: Odabrati top M sopstvenih vektora na osnovu sopstvenih vrednosti
    #         Hint: np.argsort
    # Step 4: Primeniti Transformaciju nad podacima: 
    
    # Calculate covariance matrix
    X = X - np.mean(X, axis=0)
    cov_mat = np.cov(X.T)

    # Calculate eig
    eigen_values, eigen_vectors = np.linalg.eigh(cov_mat)

    # Sort indexes
    sorted_indexes = np.argsort(eigen_values)[::-1]
    eigen_values = eigen_values[sorted_indexes]
    eigen_vectors = eigen_vectors[:, sorted_indexes]

    # Take vector subset
    eigv_subset = eigen_vectors[:, 0: M]

    # Reduce X
    X_reduced = np.dot(eigv_subset.T, X.T).T

    return X_reduced

if __name__ == '__main__':
    Testbench(covariance_reduce)
    Testbench(pca)
    Testbench(bayes_train)
    Testbench(classify)
    Testbench(kNN)
    Testbench(k_means)
    Testbench(logistical_regression)
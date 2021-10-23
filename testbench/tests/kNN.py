import numpy as np
number_of_tests = 5
import pandas as pd
from sklearn.model_selection import train_test_split

def test_kNN(bench: 'Testbench'):

    name = "testbench/tests/datasets/kNN/data_after_pca.csv"

    df = pd.read_csv(name)
    data = []

    data.append(df["PC1"])
    data.append(df["PC2"])
    data = np.array(data)
    data = np.transpose(data)

    true_labels = np.array(df["NObeyesdad"])

    X_train, X_test, y_train, y_test = train_test_split(data, true_labels, test_size=0.30)
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    predicted_labels = bench.function(X_test, X_train, y_train)

    for i in range(len(predicted_labels)):

        bench.assert_eq(predicted_labels[i], y_test[i])

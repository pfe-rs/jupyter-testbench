import numpy as np
import pandas as pd
from importlib.resources import contents, path


def load_data(name: str):
    df = pd.read_csv(name)
    clean_df = pd.DataFrame()
    
    # PC1 i PC2 kolone samo kopiramo
    for col in ["PC1", "PC2"]:
        clean_df[col] = df[col]
        
    # sa proverom jednakosti dobijamo True/False, pretvaranjem u int dobijamo 1/0 sto nam treba
    targets = (df["NObeyesdad"] == 3).astype(int).rename("Obese")

    return clean_df, targets


def hypothesis(X, theta):
    # mnozenje vrednosti featura sa tezinama i njihovo sabiranje, predstavljeno u obliku matricnog proizvoda
    z = np.dot(theta, X.T)
    # ne zelimo da dobijemo tacno 0 ili 1 jer ce nam kasnije to praviti problem u logaritmu,
    # zato se ogranicimo na opseg od 0.000001 do 0.9999999
    return np.clip(1/(1+np.exp(-(z))), 0.000001, 0.9999999)


def cost(y, h):
    # racunamo cross entropy
    return -(1/len(y)) * np.sum(y*np.log(h) + (1-y)*np.log(1-h))


def gradient_descent(X, y, theta, alpha, epochs):
    h = hypothesis(X, theta)
    cost_history = [cost(y, h)] 
    for _ in range(0, epochs):
        h = hypothesis(X, theta)
        for i in range(0, len(X.columns)):
            # TODO Popuni
            # Hint: izvod je (h-y)*X
            theta[i] -= alpha * np.mean((h-y)*X.iloc[:, i])
        cost_history.append(cost(y, h))
    return cost_history, theta


def test_logistical_regression(bench):
    # pth = "testbench/tests/datasets/logistical_regression/obesity_pca.csv"
    with path('testbench.tests.datasets.logistical_regression', "obesity_pca.csv") as pth:
        features, labels = load_data(str(pth))
    args = [features, labels, [0.5]*len(features.columns), 0.0001, 500]
    res1 = bench.function(*args)
    args[2] = [0.5]*len(features.columns) # jer je theta promenjeno
    bench.assert_eq(res1, gradient_descent(*args))

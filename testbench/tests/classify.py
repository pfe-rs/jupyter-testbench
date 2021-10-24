import numpy as np
import pandas as pd

def test_classify(bench):
    test_data_pth = "testbench/tests/datasets/naive_bayes/"

    df = pd.read_csv(test_data_pth + "bayes_test.csv")
    dfn = df.to_numpy()
    X = dfn[:, 1:3]
    Y = dfn[:, -1]

    apriori = np.load(open(test_data_pth + "apriori.npy", "rb"))
    conditional = np.load(open(test_data_pth + "conditional.npy", "rb"))
    cnt = 0
    for i in range(len(Y)):
        y_hat = bench.function(apriori, conditional, X[i, 0], X[i, 1])
        cnt += y_hat == Y[i]
    per = cnt / len(Y)
    bench.assert_expr(per > .85)
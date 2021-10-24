import numpy as np
import pandas as pd

def test_bayes_train(bench):
    test_data_pth = "testbench/tests/datasets/naive_bayes/"

    df = pd.read_csv(test_data_pth + "bayes_train.csv")
    dfn = df.to_numpy()
    X = dfn[:, 1:3]
    Y = dfn[:, -1]

    apriori_truth = np.load(open(test_data_pth + "apriori.npy", "rb"))
    conditional_truth = np.load(open(test_data_pth + "conditional.npy", "rb"))
    apriori, conditional = bench.function(X, Y)

    bench.assert_expr((apriori_truth == apriori).all())
    bench.assert_expr((conditional_truth == conditional).all())

import numpy as np
import pandas as pd
from importlib.resources import open_binary
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def test_classify(bench: 'Testbench'):
    if bench.function is None:
        return
    test_data_pth = "testbench.tests.datasets.naive_bayes"
    df = None
    apriori = None
    conditional = None
    with open_binary(test_data_pth, 'bayes_test.csv') as file:
        df = pd.read_csv(file)
    dfn = df.to_numpy()
    X = dfn[:, 1:3]
    Y = dfn[:, -1]

    with open_binary(test_data_pth, 'apriori.npy') as file:
        apriori = np.load(file)
    with open_binary(test_data_pth, 'conditional.npy') as file:
        conditional = np.load(file)
    cnt = 0
    for i in range(len(Y)):
        y_hat = bench.function(apriori, conditional, X[i, 0], X[i, 1])
        cnt += y_hat == Y[i]
    per = cnt / len(Y)
    bench.assert_expr(per > .85)

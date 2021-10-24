import numpy as np
import pandas as pd
from importlib.resources import open_binary
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def test_bayes_train(bench: 'Testbench'):
    if bench.function is None:
        return
    test_data_pth = "testbench.tests.datasets.naive_bayes"
    df = None
    apriori_truth = None
    conditional_truth = None
    with open_binary(test_data_pth, 'bayes_train.csv') as file:
        df = pd.read_csv(file)
    dfn = df.to_numpy()
    X = dfn[:, 1:3]
    Y = dfn[:, -1]

    with open_binary(test_data_pth, 'apriori.npy') as file:
        apriori_truth = np.load(file)
    with open_binary(test_data_pth, 'conditional.npy') as file:
        conditional_truth = np.load(file)
    apriori, conditional = bench.function(X, Y)

    bench.assert_expr(np.isclose(apriori_truth, apriori).all())
    bench.assert_expr(np.isclose(conditional_truth, conditional).all())

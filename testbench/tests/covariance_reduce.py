import numpy as np
import pandas as pd
from importlib.resources import open_binary
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def test_covariance_reduce(bench: 'Testbench'):
    if bench.function is None:
        return
    test_data_pth = "testbench.tests.datasets.pca"
    gt = None
    X = None
    Y = None
    with open_binary(test_data_pth, 'data_cov_red.npy') as file:
        gt = np.load(file)
    with open_binary(test_data_pth, 'clean_x.npy') as file:
        X = np.load(file)
    with open_binary(test_data_pth, 'clean_y.npy') as file:
        Y = np.load(file)

    X = pd.DataFrame(X)
    Y = pd.DataFrame(Y)

    reduced = bench.function(X, Y)

    bench.assert_expr(np.isclose(gt, reduced).all())

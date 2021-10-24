import numpy as np
from importlib.resources import open_binary

def test_pca(bench):
    test_data_pth = "testbench.tests.datasets.pca"
    gt = None
    X = None
    with open_binary(test_data_pth, 'data_pca.npy') as file:
        gt = np.load(file)
    with open_binary(test_data_pth, 'data_cov_red.npy') as file:
        X = np.load(file)
    reduced = bench.function(X, 2)
    bench.assert_expr(np.isclose(gt,reduced).all())

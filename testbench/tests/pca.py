import numpy as np
import pandas as pd


def test_pca(bench):
    test_data_pth = "testbench/tests/datasets/pca/"
    gt = np.load(open(test_data_pth + "data_pca.npy", "rb"))

    X = np.load(open(test_data_pth + "data_cov_red.npy", "rb"))

    reduced = bench.function(X, 2)

    bench.assert_expr((gt == reduced).all())

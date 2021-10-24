import numpy as np
import pandas as pd

def test_covariance_reduce(bench):
    test_data_pth = "testbench/tests/datasets/pca/"
    gt = np.load(open(test_data_pth + "data_cov_red.npy", "rb"))

    X = np.load(open(test_data_pth + "clean_x.npy", "rb"))
    Y = np.load(open(test_data_pth + "clean_y.npy", "rb"))

    X = pd.DataFrame(X)
    Y = pd.DataFrame(Y)

    reduced = bench.function(X, Y)

    bench.assert_expr((gt == reduced).all())

import numpy as np
number_of_tests = 5
from sklearn.metrics.cluster import adjusted_rand_score
from importlib.resources import open_binary
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def test_k_means(bench: 'Testbench'):
    if bench.function is None:
        return

    for i in range(1, number_of_tests+1):
        data = None
        true_labels = None
        pkg: str = 'testbench.tests.datasets.k-means'
        with open_binary(pkg, 'data{}.npy'.format(i)) as file:
            data = np.load(file)
        with open_binary(pkg, 'labels{}.npy'.format(i)) as file:
            true_labels = np.load(file)
        number_of_clusters = 4


        predicted_labels = bench.function(data)
        # for i in range(number_of_clusters):
        #     max = 0
        #     idx_i, = np.where(predicted_labels == i)
        #     data_i = data[idx_i]
        #     max_j = data_i
        #     for j in range(number_of_clusters):

        #         idx_j, = np.where(true_labels == j)

        #         data_j = data[idx_j]
        #         count = sum(x in data_i for x in data_j)
        #         if count > max:
        #             max = count
        #             max_j = data_j

        #     for j in max_j:
        #         bench.assert_eq(j in data_i, True)

        score = adjusted_rand_score(true_labels, predicted_labels)
        bench.assert_expr(score>0.85)


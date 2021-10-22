import numpy as np
number_of_tests = 5

def test_k_means(bench: 'Testbench'):

    for i in range(1, number_of_tests+1):
        data = np.load("testbench/tests/datasets/k-means/data{}.npy".format(i))
        true_labels = np.load("testbench/tests/datasets/k-means/labels{}.npy".format(i))
        number_of_clusters = 4


        predicted_labels = bench.function(data)
        for i in range(number_of_clusters):
            max = 0
            idx_i, = np.where(predicted_labels == i)
            data_i = data[idx_i]
            max_j = data_i
            for j in range(number_of_clusters):

                idx_j, = np.where(true_labels == j)

                data_j = data[idx_j]
                count = sum(x in data_i for x in data_j)
                if count > max:
                    max = count
                    max_j = data_j

            for j in max_j:
                bench.assert_eq(j in data_i, True)


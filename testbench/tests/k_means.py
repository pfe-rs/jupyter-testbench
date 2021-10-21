import random

import numpy as np
from sklearn.metrics import adjusted_rand_score
number_of_tests = 5

def generate_point(mean_x, mean_y, deviation_x, deviation_y):
    return random.gauss(mean_x, deviation_x), random.gauss(mean_y, deviation_y)



def test_k_means(bench: 'Testbench'):

    for _ in range(number_of_tests):
        cluster_mean_x = 50
        cluster_mean_y = 50
        cluster_deviation_x = 15
        cluster_deviation_y = 15
        point_deviation_x = 5
        point_deviation_y = 5

        number_of_clusters = 4
        points_per_cluster = 50

        cluster_centers = np.array([generate_point(cluster_mean_x,
                                                   cluster_mean_y,
                                                   cluster_deviation_x,
                                                   cluster_deviation_y)
                                    for _ in range(number_of_clusters)])

        points = np.array([generate_point(center_x,
                                          center_y,
                                          point_deviation_x,
                                          point_deviation_y)
                           for center_x, center_y in cluster_centers
                           for _ in range(points_per_cluster)])

        classes = np.linspace(0, number_of_clusters - 1, number_of_clusters, dtype=int)
        labels = np.repeat(classes, points_per_cluster)

        idx = np.random.permutation(len(points))
        data = points[idx]
        true_labels = labels[idx]


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


import numpy as np
from scipy.spatial import distance_matrix
from sklearn.metrics import pairwise_distances

arr = np.array(
    [
        [
            0,
            0,
        ],
        [
            1,
            1,
        ],
        [
            2,
            1,
        ],
        [
            3,
            2,
        ],
    ]
)


# Manhattan distance is the sum of the absolute differences between the coordinates of the points.
# Also known as "city block" distance.
manhattan_distance_matrix = distance_matrix(arr, arr, p=1)

# Euclidean distance is the square root of the sum of the squared differences between the coordinates of the points
# Also known as "crow-flies" distance
euclidean_distance_matrix = distance_matrix(arr, arr, p=2)

# Chebyshev distance is the maximum absolute difference between the coordinates of the points
chebyshev_distance_matrix = distance_matrix(arr, arr, p=int(np.inf))

# print(manhattan_distance_matrix)
print(euclidean_distance_matrix)
# print(chebyshev_distance_matrix)

pairwise = pairwise_distances(arr, arr, metric="euclidean")
print(pairwise)

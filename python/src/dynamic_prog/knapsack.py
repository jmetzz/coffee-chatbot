import numpy as np
from typing import List


def knapsack_recursive_with_repetition(capacity: int, weights: List, values: List):
    if capacity <= 0:
        return 0
    options = [
        (
            knapsack_recursive_with_repetition(capacity - weights[i], weights, values)
            + values[i]
        )
        for i in range(len(weights))
        if weights[i] <= capacity
    ]
    return max(options, default=0)


def knapsack_recursive_with_repetition_2(capacity: int, weights: List, values: List):
    if capacity <= 0:
        return 0
    K = np.zeros((capacity + 1, 1))
    for i in range(1, capacity + 1):
        K[i] = max(
            [
                knapsack_recursive_with_repetition_2(
                    capacity - weights[j], weights, values
                )
                + values[j]
                for j in range(len(weights))
                if weights[j] <= capacity
            ],
            default=0,
        )
    return K[capacity].squeeze()


cache = {}
def knapsack_cache_with_repetition(capacity: int, weights: List, values: List):
    if capacity in cache:
        return cache.get(capacity)

    if capacity <= 0:
        return 0
    value = max(
        [
            knapsack_cache_with_repetition(capacity - weights[j], weights, values)
            + values[j]
            for j in range(len(weights))
            if weights[j] <= capacity
        ],
        default=0,
    )
    cache[capacity] = value
    return cache[capacity]


def knapsack_dynamic_with_repetition(capacity: int, weights: List, values: List):
    K = np.zeros((capacity + 1, 1))
    for w in range(1, capacity + 1):
        K[w] = max(
            [
                K[w - weights[j]] + values[j]
                for j in range(len(weights))
                if weights[j] <= w
            ],
            default=0,
        )
    return K[capacity].squeeze()


def knapsack_memoization_no_repetition(capacity: int, weights: List, values: List):
    """Calculates the max value achievable with a knapsack of given capacity.

        The solution is encoded in a table K, 
        where K[w, j] represents the max value of a sack
        with capacity w having considered only the products 0..j
         
        Example: consider m = 4 products with respective weights and values as:
        [6, 3, 4, 2], [30, 14, 16, 9]
        K = [[ 0.  0.  0.  0.]
              [ 0.  0.  0.  0.]
              [ 0.  0.  0.  9.]
              [ 0. 14. 14. 14.]
              [ 0. 14. 16. 16.]
              [ 0. 14. 16. 23.]
              [30. 30. 30. 30.]
              [30. 30. 30. 30.]
              [30. 30. 30. 39.]
              [30. 44. 44. 44.]
              [30. 44. 46. 46.]]
        
        If we consider only the first element, only a sack with capacity 6 or more
        would be able to hold it. Thus, the max value of a sack with capacity 10, 
        would be 30 (the weight of the first product).
        Considering the first 3 elements and a sack with capactity 10, however, 
        would get the value 46 corresponding to 1 product with weight 6 (value 30) and 
        1 with weight 4 (value 16).

        Therefore, by checking the resulting value stored in K[capacity, m - 1] 
        we get the maximum possible value.

        Params:
            capacity: the max weight capacity of the sack
            weights: the products weight list
            values: the products values
        Return:
            the total value of the sack
    """
    m = len(weights)
    K = np.zeros((capacity + 1, m))
    for j in range(m):
        for w in range(capacity + 1):
            if weights[j] > w:
                K[w, j] = K[w, j - 1]
            else:
                K[w, j] = max(
                    [K[w, j - 1], K[w - weights[j], j - 1] + values[j]], default=0
                )
    return K[capacity, m - 1].squeeze()


if __name__ == "__main__":
    # capacity = 10
    # weights = [6, 3, 4, 2]
    # values = [30, 14, 16, 9]
    # optimal selection: [1, 0, 1, 0]

    # capacity = 26
    # weights = [12, 7, 11, 8, 9]
    # values = [24, 13, 23, 15, 16]
    # optimal selection: [0, 1, 1, 1, 0]

    capacity = 104
    weights = [25, 35, 45, 5, 25, 3, 2, 2 ]
    values = [350, 400, 450, 20, 70, 8, 5, 5]
    # optimal selection: [1, 0, 1, 1, 1, 0, 1, 1]

    # capacity = 6404180
    # weights = [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]
    # values = [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261]
    # optimal selection: [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1]


    from timeit import default_timer as timer
    performance = dict()
    # solution with repetition: 48
    # start = timer()
    # solution = knapsack_recursive_with_repetition(capacity, weights, values)
    # end = timer()
    # performance["recursive_with_repetition"] = {
    #     "time": end - start,
    #     "solution": solution
    # }
    
    # start = timer()
    # solution = knapsack_recursive_with_repetition_2(capacity, weights, values)
    # end = timer()
    # performance["recursive_with_repetition_2"] = {
    #     "time": end - start,
    #     "solution": solution
    # }

    start = timer()
    solution = knapsack_cache_with_repetition(capacity, weights, values)
    end = timer()
    performance["cache_with_repetition"] = {
        "time": end - start,
        "solution": solution
    }

    # start = timer()
    # solution = knapsack_dynamic_with_repetition(capacity, weights, values)
    # end = timer()
    # performance["dynamic_with_repetition"] = {
    #     "time": end - start,
    #     "solution": solution
    # }

    for k, v in sorted(performance.items(), key=lambda kv: kv[1]["time"]):
        print(f"{k} -> {v['solution']} - {v['time']}")

    # solution without repetition: 46
    # print(knapsack_memoization_no_repetition(10, weights, values))

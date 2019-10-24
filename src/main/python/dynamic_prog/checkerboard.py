"""Consider a checkerboard with n × n squares and a cost function c(i, j)
which returns a cost associated with square (i,j) (i being the row, j being
the column). Let us say there was a checker that could start at any square on
the first rank (i.e., row) and you wanted to know the shortest path 
(the sum of the minimum costs at each visited rank) to get to the last rank; 
assuming the checker could move only diagonally left forward, diagonally right 
forward, or straight forward. That is, a checker on (1,3) can move to (2,2), 
(2,3) or (2,4).

For instance (on a 5 × 5 checkerboard),

| 6	7	4	7	8 |
| 7	6	1	1	4 |
| 3	5	7	8	2 |
| –	6	7	0	– |
| –	–	*5*	–	– |


This problem is expressed by the following recursion:

for j < 1 or j > n:     q(i, j) = ∞
for i = 1:              q(i, j) = c(i, j)
otherwise:              q(i, j) = min( minCost(i-1, j-1), minCost(i-1, j), minCost(i-1, j+1) ) + c(i, j)

 """

import numpy as np
from numpy import hstack, vstack

INF = 999
cost_table_recursive = np.full((5, 5), 0) 
def checker_cost_recursive(n, costs, i, j):
    """Recursively computes the path cost.
    
    Like the naive implementation of the Fibonacci method,
    this method is horribly slow because it too exhibits the 
    overlapping sub-problems attribute. That is, it recomputes
    the same path costs over and over.


    The actual path is not formed in this method.

    """
    if j < 0 or j >= n:
        return INF
    if i == n - 1:
        return costs[i][j]
    else:
        value = min(
            checker_cost_recursive(n, costs, i+1, j-1),
            checker_cost_recursive(n, costs, i+1, j),
            checker_cost_recursive(n, costs, i+1, j+1)
        ) + costs[i][j]
        cost_table_recursive[i,j] = value
        
        return value


def checker_cost_dp(costs):
    n, m = costs.shape
    cost_table = np.full((n, m + 2), INF) # two extra columns to handle the borders of matrix costs
    path_table = np.full((n, m), -1, dtype = int)
    # The acummulated cost for all elements 
    # in the first row of costs is its own cost
    for i in range(m):
        cost_table[0, i + 1] = costs[0, i]
    
    for l in range(1, n):
        for c in range(1, m + 1):
            values = [cost_table[l - 1, c - 1],
                      cost_table[l - 1, c],
                      cost_table[l - 1, c + 1]]
            best = np.argmin(values)
            cost_table[l, c] = values[best] + costs[l, c - 1]
            path_table[l, c - 1] = c - 1 + best - 1

    # drop the extra columns in the cost_table array
    cost_table = cost_table[ : , 1:-1]
    return cost_table, path_table, np.argmin(cost_table[n - 1])

def build_path(path_table, row, column):
    if row == 1:
        return f"{path_table[row, column]}"
    else:
        predecessor = build_path(path_table, row - 1, path_table[row, column])
        return f"{predecessor} -> {path_table[row, column]}"

def solution_path(table, row, column):
    predecessor = build_path(table, row, column)
    return f"{predecessor} -> {column}"

if __name__ == "__main__":
    
    n = 5
    costs = np.array([
        [INF, INF, 5, INF, INF],
        [INF, 6, 7, 0, INF],
        [3, 5, 7, 8, 2],
        [7, 6, 1, 1, 4],
        [6, 7, 4, 7, 8]
    ])
    print("Recursive solution")
    print(f"Minimum cost: {checker_cost_recursive(costs.shape[0], costs, 0, 2)}")
    print("Cummulative costs:")
    print(cost_table_recursive)

    print("\n----------------------------")
    print("Dynamic programming solution\n")
    table, paths, solution = checker_cost_dp(np.array(costs))
    path = solution_path(paths, table.shape[0] - 1, solution)

    print(f"Minumum cost: {table[-1][solution]}")
    print(f"Solution: {path}")
    print("Cummulative costs:")
    print(table)
    print("Paths table:")
    print(paths)
    
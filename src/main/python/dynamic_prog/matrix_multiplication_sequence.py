import numpy as np

def mult(dimensions, i, k, j):
    return dimensions[i] * dimensions[k] * dimensions[j]    

def matrix_chain_cost(dimensions):
    n = len(dimensions) # number of matrices
    costs = np.full((n, n), 0)    
    for i in range(n):
        costs[i, i] = 0
    
    for subproblem_size in range(1, n - 1):
        for i in range(1, n - subproblem_size):
            j = i + subproblem_size
            options = [costs[i, k] + costs[k + 1, j] + mult(dimensions, i - 1, k, j) 
                        for k in range(i, j)]
            costs[i, j] = min(options, default=-1)
    return costs

def matrix_chain_order(dimensions):
    """Calculates the matrix chain multiplication cost.
    Also provides a optimal solution encoded in the solution array.
    Params:
        dimensions: an array with all matrices dimensions enconded.
            Each matrix A_i has i-1 lines and i columns,
            where i is an index in the dimensions array, i.e. i in [1, len(dimensions) ) interval.
    Returns:
        costs: the cost of each parenthesis split combination
        solution: the parenthesis position for the best split in the chain
            regarding the smalles cost of multiplication.
            solution[i,j] contains the index k where the parenthesis should be
            used to divide Ai..Aj multiplication into Ai..Ak and Ak+1..Aj.

    """
    n = len(dimensions) # number of matrices
    costs = np.full((n, n), 0) 
    solution = np.full((n, n), -1)   
    for i in range(n):
        costs[i, i] = 0
    
    for subproblem_size in range(1, n - 1):
        for i in range(1, n - subproblem_size):
            j = i + subproblem_size
            costs[i, j] = -1
            for k in range(i, j):
                value = costs[i, k] + costs[k + 1, j] + mult(dimensions, i - 1, k, j)
                if value < costs[i, j] or costs[i, j] == -1:
                    costs[i, j] = value 
                    solution[i, j] = k   
    return costs, solution

def print_splits(s, i, j):
    """Prints the optimal matrix multiplication order as a string

    s[i,j] contains the index k where the parenthesis should be
    used to divide Ai..Aj multiplication into Ai..Ak and Ak+1..Aj.
    Thus, we recursivelly split call this funtion adjusting
    the indexes such that a separation is add at index k.
    First line and column should no be considered.
    Example: Considering 6 matrices and the following solution table
        s = 
        [[-1 -1 -1 -1 -1 -1 -1]
        [-1 -1  1  1  3  3  3]
        [-1 -1 -1  2  3  3  3]
        [-1 -1 -1 -1  3  3  3]
        [-1 -1 -1 -1 -1  4  5]
        [-1 -1 -1 -1 -1 -1  5]
        [-1 -1 -1 -1 -1 -1 -1]]
    
    The first split for the chain [1, 6] happens at k=3.
    Thus, we can split the problem as
        [1, s[1,6]] = [1, 3]
        [s[1,6] + 1, 6] = [4, 1]

        A1 A2 A3 | A4 A5 A6

    The next step, when considering [1, 3] (which is A1 A2 A3),
    we then spli at s[1, 3] = 1. Thus, k = 1:
        
        A1 | A2 A3 
    And so on repeating the process until finished.

    The base case for the recursion is when i and j are equal, meaning
    there were no split and we can safelly print 'A_i'.

    Params:
        s: the stricly upper diagonal matrix enconding the 
            parenthesis splitting points
        i: the row index 
        j: the column index
    """
    if i == j:
        print(f" A{i} ", end='')
    else:
        print("(", end='')
        print_splits(s, i, s[i,j])
        print_splits(s, s[i,j] + 1, j)
        print(")", end='')


if __name__ == "__main__":
    """Optimal matrix multiplication chain
    Matrix multiplication is not commutative (in general, A×B != B×A), 
    but it is associative, which means for instance that A×(B×C) = (A×B)×C.
    Multiplying an m × n matrix by an n × p matrix takes mnp multiplications.

    The problem: 
        How do we determine the optimal order of matrix multiplication, 
        if we want to compute A1 × A2 × · · · × An, where the Ai’s are 
        matrices with dimensions m0 × m1, m1 × m2, . . . , mn−1 × mn, respectively? 

    We can find a particular parenthesization that reflects the optimal order.
    """

    # All matrices dimensions are condensed in the dimensions array,
    # where matrix A_i has i-1 lines and i columns, for i in [1, len(dimensions)).
    # Thus, in this example we have A_1, .. A_6 with the following dimensions:
    # A_1.shape = [30, 35]
    # A_2.shape = [35, 15]
    # A_3.shape = [15, 5]
    # A_4.shape = [5, 10]
    # A_5.shape = [10, 20]
    # A_6.shape = [20, 25]
    
    dimensions = [30, 35, 15, 5, 10, 20, 25]
    costs, solution = matrix_chain_order(dimensions)
    print("Parenthesis arrangement: ", end='')
    print_splits(solution, 1, 6)
    print("\nSolution matrix: ")
    print(solution)

    print("\nCosts matrix: ")
    print(costs)
    

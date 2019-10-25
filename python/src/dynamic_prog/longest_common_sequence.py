import numpy as np
from typing import Tuple

class Direction:
    UP = 1
    DIAGONAL = 2
    LEFT = 3

def lc_subsequence(s: str, z: str) -> Tuple:
    """Builds a longest common subsequence between two strings

    Params:
        s: a input string
        z: the other input string
    Returns:
        table: the 2-dimensional table with the LCS for all subproblems
        dag: the Directed Acyclig Graph containing the solution path for all subproblems
    """
    m = len(s)
    n = len(z)

    table = np.zeros((m+1, n+1))
    # The underlying graph: edges are the precedence constraints, 
    # of the form (i, j) → (i − 1, j), (i, j) → (i, j − 1), and (i, j) → (i − 1, j − 1)
    # The directed edges represent the optimal subproblem solution chosen when solving (i, j).
    # Thus, we can follow the arrows later on to reconstruct the solution path,
    # which is simply the path from (m, n) to (0, 0).
    # The arrows are encoded as Direction elements
    dag = np.zeros((m + 1, n + 1)) 

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == z[j - 1]:
                table[i, j] = table[i - 1, j - 1] + 1
                dag[i, j] = Direction.DIAGONAL     # diagonal-left arrow: (i, j) → (i − 1, j − 1)
            else:
                if table[i - 1, j] >= table[i, j - 1]:
                    table[i, j] = table[i - 1, j]
                    dag[i, j] = Direction.UP       # up arrow: (i, j) → (i − 1, j)
                else:
                    table[i, j] = table[i, j - 1]
                    dag[i, j] = Direction.LEFT     # left arrow: (i, j) → (i, j − 1)
    return table, dag

def lcs_solution(dag, s, i, j, buffer):
    """Reconstruct the solution path encoded in the DAG.

        This method follows the directed edges in the DAG from 
        vertex (i, j) to the origin (0, 0).
        
        Every edge is formed either as
            (i, j) → (i − 1, j), up arrow arrow, 
            (i, j) → (i, j − 1), left arrow, or
            (i, j) → (i − 1, j − 1) diagonal-left arrow.
    
        The directed edges represent the optimal subproblem solution chosen when solving (i, j).
        The arrows are encoded as Direction enum elements
            
        Params:
            dag: a bi-dimensional array representing with the lines representing characters 
                in the input string, and collumns the characters in the sencond string used
                to build the LCS.
            s: the input string
            i: integer index representing the line coordinate to run the recursion
            j: integer index representing the column coordinate to run the recursion
            buffer: a list where the solution path should be accumulated
    """
    if i < 0 or j < 0:
        return
    if dag[i, j] == Direction.DIAGONAL: #diagonal-left
        lcs_solution(dag, s, i - 1, j - 1, buffer)
        buffer.append(s[i - 1])
    elif dag[i, j] == Direction.UP: #up
        lcs_solution(dag, s, i - 1, j, buffer)    
    else: # left
        lcs_solution(dag, s, i, j - 1, buffer)    

if __name__ == "__main__":
    s1 = "ABCBDAB"
    s2 = "BDCABA"
    t, d = lc_subsequence(s1, s2)
    solution = []
    lcs_solution(d, s1, len(s1), len(s2), solution)
    print(solution)

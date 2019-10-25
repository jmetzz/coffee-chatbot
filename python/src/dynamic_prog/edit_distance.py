import numpy as np

def edit_dist(s, z):
    """Calculates the edit distance between two given sequences.
    
        This procedure fills in the table row by row, and left to right within each row. 
        Each entry takes constant time to fill in, so the overall running time is 
        just the size of the table, O(mn).

        Args:
            s: first input string
            z: second input string
        
        Returns:
            The minimum number of edits (insertions, deletions, and substitutions of characters)
            needed to transform the first string into the second.
    """
    # Sub-problem definition:
    #    Given i as the index of the last element in s
    #    and j as the last element in z:
    #        E(i, j) = min{1 + E(i − 1, j), 1 + E(i, j − 1), diff(i, j) + E(i − 1, j − 1)}
    # The base cases:
    #    When either input string is empty
    #    E(s, 0) = len(s)
    #    E(0, z) = len(z) 
    #    
    #    E(0, ·) and E(·, 0), both of which are easily solved. 
    #    E(0, j) is the edit distance between the 0-length prefix of s, namely the empty string,
    #    and the first j letters of z: clearly, j. And similarly, E(i, 0) = i.
    n = len(s)
    m = len(z)
    table = np.zeros((n, m))
    for i in range(n):
        table[i, 0] = i

    for j in range(m):
        table[0, j] = j

    for i in range(1, n):
        for j in range(1, m):
            diff = 0 if s[i] == z[j] else 1
            options = [1 + table[i, j-1], 1 + table[i-1, j], table[i-1, j-1] + diff]
            table[i,j] = min(options)

    return table[n - 1, m - 1]


if __name__ == "__main__":
    s1 = "SUNNY"
    s2 = "SNOWY"
    # s1 = "EXPONENTIAL"
    # s2 = "POLINOMIAL"
    print(edit_dist(s1, s2))
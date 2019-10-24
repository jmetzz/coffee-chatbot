import numpy as np
from numpy import vstack, hstack
from timeit import default_timer as timer

def split_matrix(X):
    mid = X.shape[0] // 2
    upper_left = X[ : mid, : mid ]
    upper_right = X[ : mid , mid: ]
    lower_left = X[ mid: , : mid ]
    lower_right  = X[ mid: , mid: ]
    return {"A": upper_left, 
        "B": upper_right, 
        "C" : lower_left,
        "D": lower_right
    }

def rec_dot(X, Y):   
    n = X.shape[0]
    if n == 1:
        return X * Y
    else:
        # The matrices must be of type (2ˆn, 2ˆn) 
        # We enforce this by adding a line and a column of
        # zeros whenever needed. These elements must be removed
        # at the end.
        if n % 2 != 0:
            X = _add_padding(X)
            Y = _add_padding(Y)

        X_split = split_matrix(X)
        Y_split = split_matrix(Y)

        # recursively calculate the quadrant combinations
        AA = rec_dot(X_split["A"], Y_split["A"])
        BC = rec_dot(X_split["B"], Y_split["C"])
        
        AB = rec_dot(X_split["A"], Y_split["B"])
        BD = rec_dot(X_split["B"], Y_split["D"])

        CA = rec_dot(X_split["C"], Y_split["A"])
        DC = rec_dot(X_split["D"], Y_split["C"])

        CB = rec_dot(X_split["C"], Y_split["B"])
        DD = rec_dot(X_split["D"], Y_split["D"])

        result = vstack((
                        hstack((AA + BC, AB + BD)),
                        hstack((CA + DC, CB + DD))
                    ))
        
        if n % 2 != 0:
            # discard the added line and column
            result = result[:-1, :-1]
        
        return result
        


def strassen_dot(X, Y):   
    n = X.shape[0]
    if n == 1:
        return X * Y
    else:
        # The matrices must be of type (2ˆn, 2ˆn) 
        # We enforce this by adding a line and a column of
        # zeros whenever needed. These elements must be removed
        # at the end.
        if n % 2 != 0:
            X = _add_padding(X)
            Y = _add_padding(Y)

        X_split = split_matrix(X)
        Y_split = split_matrix(Y)
        # recursively calculate the necessary 7 products
        A = X_split["A"]
        B = X_split["B"]
        C = X_split["C"]
        D = X_split["D"]
        E = Y_split["A"]
        F = Y_split["B"]
        G = Y_split["C"]
        H = Y_split["D"]

        P1 = strassen_dot(A, F - H)
        P2 = strassen_dot(A + B, H)
        P3 = strassen_dot(C + D, E)
        P4 = strassen_dot(D, G - E)
        P5 = strassen_dot(A + D, E + H)
        P6 = strassen_dot(B - D, G + H)
        P7 = strassen_dot(A - C, E + F)

        # combine the recursive result to form the quadrants
        upper_left = P5 + P4 - P2 + P6
        upper_right = P1 + P2
        lower_left = P3 + P4
        lower_right = P1 + P5 - P3 - P7
        
        result = vstack((
                        hstack((upper_left, upper_right )),
                        hstack((lower_left, lower_right))
                    ))
        if n % 2 != 0:
            # discard the added line and column
            result = result[:-1, :-1]
        return result


def _add_padding(X):
    n = X.shape[0]
    line = np.zeros((1, n), dtype=int)
    column = np.zeros((n+1, 1), dtype=int)
    X = hstack((vstack((X, line)), column))
    return X


def multiply_dc(X, Y, method = strassen_dot):
    if X.shape[0] != X.shape[1] or Y.shape[0] != Y.shape[1]:
        raise ValueError("Matrices are not square")
    if X.shape[0] != Y.shape[1]:
        raise ValueError(f"Incompatible shapes: '{X.shape}' and '{Y.shape}' respectively")
    
    result = method(X, Y)
    
    return result


if __name__ == "__main__":

    # a = np.array([
    #     [1,2,3],
    #     [4,5,6],
    #     [7,8,9],
    # ])
    # b = np.array([
    #     [7,8,9],
    #     [4,5,6],
    #     [1,2,3],
    # ])
    n = 100
    a = np.random.randint(9, size = (n, n))
    b = np.random.randint(9, size = (n, n))
    info = {}

    print("Expected:")
    start = timer()
    expected = a.dot(b)
    end = timer()
    info["python lib"] = end - start

    print("\n------------------------")
    print("Result of recursive method:")
    start = timer()
    actual = multiply_dc(a, b, method=rec_dot)
    end = timer()
    info["Recursive"] = end - start
    assert((expected == actual).all())

    print("------------------------")
    print("Result of Strassen's multiplication:")
    start = timer()
    actual = multiply_dc(a, b)
    end = timer()
    info["Strassen"] = end - start
    assert((expected == actual).all())

    print(f"Time comparison for matrices with shape {a.shape}")
    for k, v in info.items():
        print(f"Time spent by '{k}' method: {v:.4f}")
    



    
def fib_recursion(n: int):
    if n < 0:
        raise ValueError(f"Invalid input{n}. Must be a number greater or equal to zero")
    if n == 0 or  n == 1:
        return n
    return fib_recursion(n - 1) + fib_recursion(n - 2)

fib_cache = {}
def fib_cached(n: int):
    if n < 0:
        raise ValueError(f"Invalid input{n}. Must be a number greater or equal to zero")
    if n == 0 or  n == 1:
        return n
    elif n in fib_cache:
        return fib_cache.get(n)
    else:    
        value = fib_recursion(n - 1) + fib_recursion(n - 2)
        fib_cache[n] = value
        return value

def fib_with_memoization(n: int):

    memo = [0] * (n + 2) # create a least 2 slots
    memo[1] = 1    
    for i in range(2, n + 1):
        memo[i] = memo[i - 1] + memo[i - 2]
    return memo[n]

def fib_memoization_small_space(n: int):
    """Calculates the fibonacci number for n.
    
    Since we only need the 2 previous elements to calculate the fib 
    number for a particular i, as in the equation

        fib(i) =  fib(i - 1) + fib(i - 2)
    
    this method does not store all the elements in the sequence, 
    but rather keeps only the i-1 and i-2 elements in memory
    so we can derive the value for the element i.
    
    """
    # start with fib(0) and fib(1) as 0 and 1.
    # position 0 represents even values of i, 
    # while position 1 represents the odd values of i
    memo = [0, 1]

    # from 2 to n, calculate the i-esim fib number
    # and asign to i-1 or i-2 according to the valu of i
    for i in range(2, n + 1):
        # fib(i) =  fib(i - 1) + fib(i - 2)
        memo[i % 2] = memo[1] + memo[0]
    return memo[n % 2]



if __name__ == "__main__":
    n = 40
    print(fib_recursion(n))
    print(fib_cached(n))
    print(fib_with_memoization(n))
    print(fib_memoization_small_space(n))
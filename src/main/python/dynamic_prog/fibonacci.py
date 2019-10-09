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
    memo = [0] * (n + 1)
    memo[1] = 1    
    for i in range(2, n+1):
        memo[i] = memo[i - 1] + memo[i - 2]
    return memo[n]

if __name__ == "__main__":
    n = 20 
    # 167960
    # print(fib_recursion(n))
    # print(fib_cached(n))
    print(fib_with_memoization(n))
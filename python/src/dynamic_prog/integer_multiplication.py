from timeit import default_timer as timer


def grade_school_method(x, y):
    """'Grade-school' integer multiplication method

        Params:
            x: the first input number
            y: the second input number
        Returns:
            a number corresponding to the multiplication of the given input numbers
    """
    x_digits = str(x)
    y_digits = str(y)
    result, step = (0, 0)

    for i in range(len(x_digits) - 1, -1, -1):
        x_i = int(x_digits[i])
        k = step
        carry_over = 0
        for j in range(len(y_digits) - 1, -1, -1):
            y_j = int(y_digits[j])
            value = x_i * y_j + carry_over
            carry_over = value // 10

            value = value % 10
            result += value * (10 ** k)
            k += 1
        if carry_over > 0:
            result += carry_over * (10 ** k)
        step += 1
    return result

def decompose(x, exp):
    a = x // 10 ** exp
    b = x % 10 ** exp
    return a, b


def recursive(x, y):
    """Recursive integer multiplication method
        
        Assumes multiplication is only is possible for one digit operands.
        
        Each input number is decomposed into a combination of two other numbers:
            x = 10ˆn/2 * a + b
            y = 10ˆn/2 * c + d

            So, for x = 5678 and y = 1234
            one can visualized these numbers as 

                a = 56  |  b = 78
                -----------------
                c = 12  |  d = 34
            
            By solving each of the four remainig cases recursively, 
            and then aggregating the values we get the final result 
            for the multiplication.

        The combining step is given by the following recursion:

        f(x, y) = x * y
        when |x| = 1 and |y| = 1, otherwise
        
        f(x, y) = 10ˆ(m*2) * (ac) 
                 + 10ˆm * (ad + bc)
                 + bd
        where m = floor(n/2) and n = max(|x|, |y|)
        
        Params:
            x: the first input number
            y: the second input number
        Returns:
            a number corresponding to the multiplication of the given input numbers
    """
    if x < 10 and y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2
    a, b = decompose(x, m)
    c, d = decompose(y, m)

    return int(
        (10**(m*2)) * (recursive(a, c))
        + (10**m) * (recursive(a, d) + recursive(b, c))
        + recursive(b, d)
    )


def karatsuba(x, y, depth=1, debug = False):
    """Karatsuba's integer multiplication method
        
        Assumes multiplication is only is possible for one digit operands.
        This method improves the recursive multiplication
        by avoiding one of the four recursive calls.

        Similarly to the recursive method, each input number 
        is decomposed into a combination of two other numbers:
            x = 10ˆn/2 * a + b
            y = 10ˆn/2 * c + d

            So, for x = 5678 and y = 1234
            one can visualized these numbers as 

                a = 56  |  b = 78
                -----------------
                c = 12  |  d = 34

        However, the combining step is improved by using a trick, as follows:
            The two recursive calls to compute (ad + bc) can be simplified.
            Turns out that 
                (a + b)(c + d) = ac + ad + bc + bd

            Since we are only interested in the 'ad + bc' part,
            we can compute it as a combination of the results from the other
            recursions instead of running an extra recursion step.
            If we already have ac and bd, then applying Guass trick we get:
            
                (a + b)(c + d) = ac + ad + bc + bd
                (a + b)(c + d) - ac - bd = ad + bc
                
            This means, we actually only need to calculate the recursions for ac and bd,
            and the recursion (a + b)(c + d) 


        The recursive definition is the same:

        f(x, y) = x * y
        when |x| = 1 and |y| = 1, otherwise
        
        f(x, y) = 10ˆ(m*2) * (ac) 
                 + 10ˆm * (ad + bc)
                 + bd
        where m = floor(n/2) and n = max(|x|, |y|)
        
        Params:
            x: the first input number
            y: the second input number
        Returns:
            a number corresponding to the multiplication of the given input numbers
    """
    # base case
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    exp = n // 2
    a, b = decompose(x, exp)
    c, d = decompose(y, exp)
    
    # the recursions
    s1 = karatsuba(a, c, depth+1)
    s2 = karatsuba(b, d, depth+1)
    s3 = karatsuba(a + b, c + d, depth+1)
    s4 = s3 - s2 - s1  # gauss trick
    # aggregation step
    s5 = int(10**(exp*2) * s1 + 10**(exp) * s4 + s2)

    if debug:
        print_debug_info(depth, n, s1, s2, s3, s4, s5)
    return s5

def print_debug_info(depth, n, ac, bd, ad_plus_bc, step4, step5):
    prefix = "".join(["    "] *  depth)
    hprefix = "".join(["  "] *  depth)
    print(f"{hprefix} ({x}, {y}); n = {n}")    
    print(f"{prefix} step {depth}.1 = {ac}")
    print(f"{prefix} step {depth}.2 = {bd}")
    print(f"{prefix} step {depth}.3 = {ad_plus_bc}")
    print(f"{prefix} step {depth}.4 = {step4}")
    print(f"{prefix} step {depth}.5 = {step5}")
    print(f"{prefix} --")


if __name__ == "__main__":
    test_cases = [
        (1, 0),
        (12, 3),
        (123, 34),
        (12, 344),
        (12555, 3222),
        (1234, 1234567),
        (1, 3456),
        (314159265358979, 2718281828459),
        (3141592653589793238462643383279502884197169399375105820974944592, 2718281828459045235360287471352662497757247093699959574966967627)
    ]
    for case in test_cases:
        x = case[0]
        y = case[1]
        expected = x * y
        actual = karatsuba(x, y)
        assert(actual == expected)    

    x = 3141592653589793238462643383279502884197169399375105820974944592
    y = 2718281828459045235360287471352662497757247093699959574966967627
    
    start = timer()
    actual = x * y
    end = timer()
    print("Time comparison for multiplication methods")
    print(f"{end - start} : python lib ")
    
    start = timer()
    actual = grade_school_method(x, y)
    end = timer()
    print(f"{end - start} : grade-school method ")

    
    start = timer()
    actual = recursive(x, y)
    end = timer()
    print(f"{end - start} : recursive method ")

    start = timer()
    actual = karatsuba(x, y)
    end = timer()
    print(f"{end - start} : karatsuba method ")

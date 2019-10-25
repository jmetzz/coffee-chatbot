# Run the examples

If you are using VS Code, make sure to add the correct configuration.
It is important the set the `PYTHONPATH` variable correctly in order to 
get the `imports` working properly.
Therefor, replace `/path/to/` part of the path with the correct path 
where the code base is located.

```json
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "env": {
                "PYTHONPATH": "/path/to/algorithm-challenges-lab/python/src:/path/to/algorithm-challenges-lab/python/resources"
            },
            "console": "integratedTerminal"
        }
    ]

```

Alternativelly, you can set the path inside the running script. For example:

```python
if __name__ == "__main__":
    import sys; print('Python %s on %s' % (sys.version, sys.platform))
    sys.path.extend(['/path/to/algorithm-challenges-lab'])
    // ...
```


# Divide and conquer algorithms and problems

| Algorithm  | Status |
|---|---|
| Merge sort - naive            | done |
| Merge sort - top down         | done |
| Merge sort - bottom up        | done |
| Quick sort - recursive & naive pivot      | done |
| Quick sort - recursive & random pivot     |   |
| Quick sort - iterative |   |
| Count inversions in a list    | done |
| Matrix multiplication         | done |
| Closes pair ||
| Fast power ||

# Dynamic programming algorithms and problems

| Algorithm  | Status |
|---|---|
| Fibonacci - naive recursion           | done |
| Fibonacci - cached                    | done |
| Fibonacci - memoization               | done |
| Fibonacci - dynamic                   | done |
| Integer multiplication - grade school | done |
| Integer multiplication - Recursive    | done |
| Integer multiplication - Karatsuba    | done |
| Knapsack - recursive                  | done |
| Knapsack - cached                     | done |
| Knapsack - memoization                | done |
| Checker board path - recursive        | done |
| Checker board path - dynamic          | done |
| Matrix multiplication sequence        | done |
| String edit distance                  | done |
| String longest commom subsequence     | done |
| Longest common substring              |  |
| Longest increasing subsequence        |  |
| Graph - tree width ||
| Graph - clique width ||
| Graph - tree decomposition ||
| CYK Cocke-Younger-Kasami ||
| Reliable shortest path ||
| Tower of Hanoi ||
| Egg dropping puzzle ||


# Unclassified yet

- String compression (cracking the code 1.6)
- Matrix rotarion (cracking the code 1.7)
- Zero Matrix (cracking the code 1.8)
- String rotation (cracking the code 1.9)
- Suffix array longest commmon prefix, longest repeated substring, KWIC - keyword in context



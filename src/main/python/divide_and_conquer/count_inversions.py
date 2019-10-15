import numpy as np
from timeit import default_timer as timer


def count_and_sort(sequence):
    n = len(sequence)
    if n == 1:
        return 0, sequence
    else:
        mid = n // 2
        x, left = count_and_sort(sequence[ : mid])
        y, right = count_and_sort(sequence[mid: ])
        z, combined = merge_and_count_split(left, right)
        return (x + y + z), combined

def merge_and_count_split(left, right):
    left_size = len(left)
    right_size = len(right)
    merged = np.zeros((left_size + right_size, 1))
    i = j = count = 0
    for k in range(left_size + right_size):
        if i >= left_size or j >= right_size: break
        if left[i] < right[j]:
            merged[k] = left[i]
            i += 1
        else:
            merged[k] = right[j]
            j += 1
            count += right_size - i
    if i < left_size:
        count += right_size - i
        _copy_over_to(left, i, merged, k)
    else:
        _copy_over_to(right, j, merged, k)
    return count, merged

def _copy_over_to(src, idx_src, dest, idx_dest):
    k = idx_dest
    i = idx_src
    while i < len(src):
        dest[k] = src[i]
        k += 1
        i += 1

if __name__ == "__main__":
    a = [1,3,5,2,4,6]
    expected = 3
    start = timer()
    actual, _ = count_and_sort(a)
    end = timer()
    print("Time comparison: A[1,3,5,2,4,6]")
    print(f"{(end - start):.4f} : count_and_sort ")
    print(f"Number of inversions: {actual}")
    assert(expected == actual)
    print("-----")

    with open('src/main/python/divide_and_conquer/IntegerArray.txt') as f:
        lines = f.readlines()
    data = np.fromstring("".join(lines), dtype=int, sep='\n')

    n = 50
    times = [0] * n
    for it in range(n):
        start = timer()
        actual, _ = count_and_sort(data)
        end = timer()
        times[it] = end - start
    avg = np.average(times)
    std = np.std(times)
    print(f"Time comparison: |A| = {len(data)} ")
    print(f"Count_and_sort AVG time: {avg:.4f} ({std:.4f})")
    print(f"Number of inversions: {count_and_sort(data)[0]}")

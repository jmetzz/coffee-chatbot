class InsertionSort:
    @classmethod
    def sort(cls, elements):
        """Sorts the given array of elements in place.

        This method is a iterative implementation of the
        Insertion sort algorithm which sorts the array in place.

        Args:
            elements: the subarray of elements to partition
        """
        cls._sort(elements, 0, len(elements) - 1)

    @classmethod
    def _sort(cls, elements, lo, hi):
        """Sorts the given array of elements in place.

        This method is a iterative implementation of the
        Insertion sort algorithm which sorts the array in place.

        Args:
            elements: the subarray of elements to partition
        """
        n = hi + 1
        for i in range(lo, n):
            current = elements[i]
            j = i
            while j > lo and current < elements[j - 1]:
                elements[j] = elements[j - 1]
                j -= 1
            elements[j] = current


if __name__ == "__main__":
    a = [2, 4, 1, 8, 5, 0, ]
    InsertionSort.sort(a)
    print(a)

    a = [2, 4, 1, 8, 5, 0, 3, 4, 5, 6, 7, 2, 1, 6]
    InsertionSort.sort(a)
    print(a)

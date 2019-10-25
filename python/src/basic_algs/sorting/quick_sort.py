import random

def swap(a, i, j):
    """Swap two elements in a given array.

    The operation is performed in place,
    exchanging the elements in position i and j.

    Args:
        i: the index of the first element
        j: the index of the second element
    """
    temp = a[j]
    a[j] = a[i]
    a[i] = temp


class QSortRec:
    @classmethod
    def sort(cls, elements):
        """Sorts the given array of elements in place.

        This method is a recursive implementation of the
        Quicksort algorithm which sorts the array in place.

        Args:
            elements: the subarray of elements to partition
        """
        cls._qsort(elements, 0, len(elements) - 1)

    @classmethod
    def _qsort(cls, elements, lo, hi):
        """Sorts the given array of elements.

        This method is a recursive implementation of the
        Quicksort algorithm which sorts the array in place.

        Args:
            elements: the subarray of elements to partition
            lo: the lower bounday index of the subarray
            hi: the higher boundary index of the subarray
        """
        n = hi - lo + 1
        if n <= 1:
            return
        pivot = cls._partition(elements, lo, hi)
        cls._qsort(elements, lo, pivot - 1)
        cls._qsort(elements, pivot + 1, hi)

    @classmethod
    def _partition(cls, elements, lo, hi):
        """Partition the array of elements in a two-way fashion.

        Uses always the first element as the pivot.
        The elements in the array reorganized according
        to the following rule:
            elements = [a_i <=  pivot, pivot, a_i > pivot]
        for all i in 0..n

        Args:
            elements: the subarray of elements to partition
            lo: the lower bounday index of the subarray
            hi: the higher boundary index of the subarray
        Returns:
            the pivot index
        """
        pivot, _ = cls.choose_pivot(elements, lo, hi)
        i = lo + 1
        for j in range(i, hi + 1):
            if elements[j] < pivot:
                swap(elements, i, j)
                i += 1
        swap(elements, lo, i - 1)
        return i - 1

    @classmethod
    def choose_pivot(cls, elements, lo, hi):
        return elements[lo], lo


class QSortRec2(QSortRec):
    @classmethod
    def _partition(cls, elements, lo, hi):
        """Partition the array of elements in a two-way fashion.

        Uses always the first element as the pivot.
        The elements in the array reorganized according
        to the following rule:
            elements = [a_i <=  pivot, pivot, a_i > pivot]
        for all i in 0..n

        Args:
            elements: the subarray of elements to partition
            lo: the lower bounday index of the subarray
            hi: the higher boundary index of the subarray
        Returns:
            the pivot index
        """
        pivot, _ = cls.choose_pivot(elements, lo, hi)
        i = lo + 1
        j = hi
        while True:
            while i < hi and elements[i] < pivot:
                i += 1
            while j > lo and elements[j] > pivot:
                j -= 1
            if i >= j:
                break
            swap(elements, i, j)
        swap(elements, lo, j)
        return j


class QSortRecRandomized(QSortRec2):
    @classmethod
    def sort(cls, elements):
        """Sorts the given array of elements in place.

        This method is a recursive implementation of the
        Quicksort algorithm which sorts the array in place.

        In order to eliminate the performance dependency
        on input and to guarantee O(N log N) running time,
        the elements are shuffled before performing the sorting.

        Args:
            elements: the subarray of elements to partition
        """
        from random import shuffle
        shuffle(elements)
        cls._qsort(elements, 0, len(elements) - 1)


class QSortRecThreeWayPartition(QSortRec2):
    @classmethod
    def _partition(cls, elements, lo, hi):
        """Partition the array of elements using three-way strategy.

        The elements in the array reorganized according
        to the following rule:
            elements = [a_i <=  pivot, pivot, a_i > pivot]
        for all i in 0..n

        This implementation is an improvement on the two-way partitioning
        method for cases when the data contains many duplicate keys.
        However, it uses many more exchanges than the stadard 2-way
        partitioning method for the common case when the numver of
        duplicate keys in the array is not high.

        We keep a few 'pointers' to control the partitioning process:
            lo: lower boundary index
            hi: higher boundary index
            lt: less than pivot higher boundary
            i: equals pivot higher bounday
            gt: greater than pivot lower boundary

        Start:
        [ pivot | | | | | | | | | | | | | | |  ]
        lo                                   hi
        lt                                   gt
        i

        During partitioning:
        [ < pivot | = pivot | unseen | > pivot ]
                  lt        i        gt
        where:
            [lo..lt] : less than pivot
            [lt + 1..i]: equals pivot
            [i + 1..gt - 1]: unseen elements
            [gt + 1..hi]: greater than pivot

        After partitioning:
        [ < pivot       | = pivot |    > pivot ]
        lo                                   hi
                      lt          gt
                         i

        Args:
            elements: the subarray of elements to partition
            lo: the lower bounday index of the subarray
            hi: the higher boundary index of the subarray
        Returns:
            the pivot index

        """
        pivot, _ = cls.choose_pivot(elements, lo, hi)
        lt = lo
        i = lo + 1
        gt = hi
        while i <= gt:
            if elements[i] < pivot:
                swap(elements, i, lt)
                lt += 1
                i += 1
            elif elements[i] > pivot:
                swap(elements, i, gt)
                gt -= 1
            else:
                i += 1
        return lt


class QSortRecThreeWayPartitionAlternative(QSortRec2):
    @classmethod
    def _partition(cls, elements, lo, hi):
        """Partition the array of elements using three-way strategy

        This implementation is an improvement on the two-way partitioning
        method for cases when the data contains many duplicate keys.

        This is a different implementation of the 3-way partitioning method.
        The abstraction is partition the array such that:

        The pivot is always the first element in the subarray.

            [ pivot | <= pivot | > pivot |     unseen     ]
            lo                                           hi

        We keep 2 pointers to control the process, lte (less than or equal to pivot)
        and gt (greater than pivot):
            [ pivot | <= pivot | > pivot |     unseen     ]
            lo                                           hi
                             lte        gt

        This way we progress lte while decrementing gt until they cross.
        At the end, we need to swap the bigger 'less than pivot' element
        with the pivot to put the pivot in the right place.
        Such element is at the index lte - 1.

        Args:
            elements: the subarray of elements to partition
            lo: the lower bounday index of the subarray
            hi: the higher boundary index of the subarray
        Returns:
            the pivot index
        """
        pivot, _ = cls.choose_pivot(elements, lo, hi)
        lte = lo
        for gt in range(lte + 1, hi + 1):
            if elements[gt] <= pivot:
                swap(elements, lte + 1, gt)
                lte += 1

        swap(elements, lte, lo)
        return lte


class QSortRecMedianOfThreePartition(QSortRec):
    @classmethod
    def choose_pivot(cls, elements, lo, hi):
        """Chosse the pivot as a median of 3.

            This method randomly selects 3 elements
            from the subarray as the pivot options.
            Then finds the median the element among
            the 3 chosen, and then swaps it with the
            element at index lo.
            This allows the usage of the base method
            for partitioning and sorting.

        Args:
            elements: the subarray of elements to partition
            lo: the lower bounday index of the subarray
            hi: the higher boundary index of the subarray
        Returns:
            pivot: the pivot value, which is the value at index lo
            pivot index: always return lo
        """
        if (hi - lo) < 3:
            return elements[lo], lo

        indexes = random.sample(range(lo, hi + 1), 3)
        values = [elements[i] for i in indexes]

        if values[0] > values[0]:
            swap(values, 0, 1)
            swap(indexes, 0, 1)

        if values[1] > values[2]:
            swap(values, 1, 2)
            swap(indexes, 1, 2)

        swap(elements, lo, indexes[1])
        return elements[lo], lo


class QSortRecRandomizedCutoff(QSortRecRandomized):
    @classmethod
    def _qsort(cls, elements, lo, hi):
        from basic_algs.sorting.insertion_sort import InsertionSort
        n = hi - lo + 1
        if n <= 1:
            InsertionSort._sort(elements, lo, hi)
            return
        pivot = cls._partition(elements, lo, hi)
        cls._qsort(elements, lo, pivot - 1)
        cls._qsort(elements, pivot + 1, hi)


class QSortRecRandomPivot(QSortRec):
    @classmethod
    def _partition(cls, a, start, end):
        raise NotImplementedError("This method is not implemented yet.")

        pivot = random.randint(0, len(a) - 1)
        swap(a, start, pivot)
        i = start + 1
        for j in range(i, end + 1):
            if a[j] < a[start]:
                swap(a, i, j)
                i += 1
        swap(a, start, i - 1)
        return i - 1


if __name__ == "__main__":

    # a =[2,4,1,8,5,0,]
    # QSortRec.sort(a)
    # print(a)

    # a =[2,4,1,8,5,0,]
    # QSortRec2.sort(a)
    # print(a)

    # a =[2,4,1,8,5,0,]
    # QSortRecRandomized.sort(a)
    # print(a)

    # a = [2, 4, 1, 8, 5, 0, 3, 4, 5, 6, 7, 2, 1, 6]
    # QSortRecThreeWayPartition.sort(a)
    # print(a)

    # a = [2, 4, 1, 8, 5, 0, 3, 4, 5, 6, 7, 2, 1, 6]
    # QSortRecThreeWayPartitionAlternative.sort(a)
    # print(a)

    # a =[2,4,1,8,5,0,]
    # QSortRecThreeWayPartitionAlternative.sort(a)
    # print(a)

    a = [2, 4, 1, 8, 5, 0, 3, 4, 5, 6, 7, 2, 1, 6]
    QSortRec.sort(a)
    print(a)

    a = [2, 4, 1, 8, 5, 0, 3, 4, 5, 6, 7, 2, 1, 6]
    QSortRecMedianOfThreePartition.sort(a)
    print(a)

    a = [2, 4, 1, 8, 5, 0, 3, 4, 5, 6, 7, 2, 1, 6]
    QSortRecRandomizedCutoff.sort(a)
    print(a)

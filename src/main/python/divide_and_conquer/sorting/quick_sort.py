import random

class QSortRec:
    @classmethod
    def sort(cls, elements):
        cls._qsort(elements, 0, len(elements) - 1)

    @classmethod
    def _qsort(cls, elements, lo, hi):
        n = hi - lo + 1
        if n <= 1:
            return
        pivot = cls._partition(elements, lo, hi)
        cls._qsort(elements, lo, pivot - 1)
        cls._qsort(elements, pivot + 1, hi)

    @classmethod
    def _partition(cls, elements, lo, hi):
        pivot = elements[lo]
        i = lo + 1
        for j in range(i, hi + 1):
            if elements[j] < pivot:
                swap(elements, i, j)        
                i += 1
        swap(elements, lo, i - 1)
        return i - 1


class QSortRec2(QSortRec):
    @classmethod
    def _partition(cls, elements, lo, hi):
        """Partition the array of elements
        
            Uses always the first element as the pivot.
            Returns the elements array reorganized according
            to the following rule:
                elements = [a_i <  pivot, pivot, a_i > pivot]
            for all i in 0..n

        """
        pivot = elements[lo]
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
        from random import shuffle
        # Eliminate the dependency on input 
        # to guarantee O(N log N) performance
        shuffle(elements) 
        cls._qsort(elements, 0, len(elements) - 1)

class QSortRecRandomPivot(QSortRec):
    @classmethod
    def _partition(cls, a, start, end):
        raise NotImplementedError("This method is not implemented yet.")

        pivot = random.randint(0,len(a) - 1)
        swap(a, start, pivot)
        i = start + 1
        for j in range(i, end + 1):
            if a[j] < a[start]:
                swap(a, i, j)        
                i += 1
        swap(a, start, i - 1)
        return i - 1


def swap(a, i, j):
    temp = a[j]
    a[j] = a[i]
    a[i] = temp

if __name__ == "__main__": 
    # a =[2,4,1,8,5,0,]
    # QSortRec.sort(a)
    # print(a)

    b =[2,4,1,8,5,0,]
    QSortRec2.sort(b)
    print(b)

    c =[2,4,1,8,5,0,]
    QSortRecRandomized.sort(c)
    print(c)
    
import numpy as np


class TopDownMergeSort:
    """Merge sort algorithm.
    
    This top down implementation of the algorithm
    does not run in place sort. Rather, it returns 
    a sorted copy of the elements.

    This implementation uses an auxiliary array as temporary space.
    """

    @classmethod
    def sort(cls, elements):
        if len(elements) == 1:
            return elements
        mid = len(elements) // 2
        left_half = cls.sort(elements[:mid])
        right_half = cls.sort(elements[mid:])
        return cls._merge(left_half, right_half)

    @staticmethod
    def _merge(left, right):
        n = len(left)
        m = len(right)
        result = [None] * (n + m)
        i = j = k = 0
        while i < n and j < m:
            if left[i] <= right[j]:
                result[k] = left[i]
                i += 1
            else:
                result[k] = right[j]
                j += 1
            k += 1

        while i < n:
            result[k] = left[i]
            i += 1
            k += 1
        while j < m:
            result[k] = right[j]
            j += 1
            k += 1

        return result


class TopDownMergeSort2:
    """Merge sort algorithm.
    
    This top down implementation of the algorithm
    sorts the given elements in place. For this, 
    it uses an auxiliary array as temporary space.
    """

    @classmethod
    def sort(cls, elements):
        buffer = [e for e in elements]
        cls._sort(elements, 0, len(elements) - 1, buffer)

    @classmethod
    def _sort(cls, elements, lo, hi, buffer):
        if hi <= lo:
            return
        mid = lo + (hi - lo) // 2
        cls._sort(elements, lo, mid, buffer)
        cls._sort(elements, mid + 1, hi, buffer)
        cls._merge(elements, lo, mid, hi, buffer)

    @staticmethod
    def _merge(elements, lo, mid, hi, buffer):
        i = lo
        j = mid + 1

        for k in range(lo, hi + 1):
            buffer[k] = elements[k]

        for k in range(lo, hi + 1):
            if i > mid:
                elements[k] = buffer[j]
                j += 1
            elif j > hi:
                elements[k] = buffer[i]
                i += 1
            elif buffer[j] < buffer[i]:
                elements[k] = buffer[j]
                j += 1
            else:
                elements[k] = buffer[i]
                i += 1


class TopDownMergeSort3(TopDownMergeSort2):
    """Merge sort algorithm.
    
    A improvement in the running time by reducing the times
    the merge method is called. 

    We can reduce the running time of the algorithm
    by skipping the call to merge in case the
    two half of the array are already in order.
    i.e., whenever a[mid] <= a[mid + 1].
    This produces a linear running for sorted subarrays.
    """
    @classmethod
    def _sort(cls, elements, lo, hi, buffer):
        if hi <= lo:
            return

        mid = lo + (hi - lo) // 2
        cls._sort(elements, lo, mid, buffer)
        cls._sort(elements, mid + 1, hi, buffer)
        
        if elements[mid] > elements[mid + 1]:
            cls._merge(elements, lo, mid, hi, buffer)


class TopDownMergeSort4:
    """Merge sort algorithm.
    
    This implementation eliminates the copy of the elements 
    from the source array to the auxiliary array during the merge step.
    It still uses the auxiliary array space, though.
    """
    @classmethod
    def sort(cls, elements):
        buffer = [e for e in elements]
        # Sort the given elements array using aux (the copy) as a source.
        cls._sort(buffer, 0, len(elements) - 1, elements)

    @classmethod
    def _sort(cls, src, lo, hi, buffer):

        # lo and hi are the boundary indexes of the subarray, both included
        if hi - lo < 1:  # if subarray size == 1
            return  # consider it ordered

        mid = (hi + lo) // 2
        cls._sort(buffer, lo, mid, src)
        cls._sort(buffer, mid + 1, hi, src)
        cls._merge(src, lo, mid, hi, buffer)

    @staticmethod
    def _merge(src, lo, mid, hi, dest):
        """Merges the two halves in order.

        The left source half is src[low : mid], both include.
        The right source half is src[mid : hi], both include.

        Args:
            src: the given elements to be merged.
            lo: the lower boundary index of the left half of the source array
            mid: the splitting point between the left and right halves of the source array.
                 It is also the higher boundary of the left array, inclusive.
            hi: The higher boundary of the right half of the array. 
            dest: The destination where the sorted elements are copied to.
        """

        if src[mid] <= src[mid + 1]:
            return 

        i = lo
        j = mid + 1
        for k in range(lo, hi + 1):
            # If left run head exists and is <= existing right run head.
            if i <= mid and (j > hi or src[i] <= src[j]):
                dest[k] = src[i]
                i += 1
            else:
                dest[k] = src[j]
                j += 1

class BottomUpMergeSort:
    @classmethod
    def sort(cls, elements):
        n = len(elements)
        buffer = [None] * n

        size = 1
        while size < n:
            for lo in range(0, n - size, size*2):
                # bear in mind the last subarray might have less
                # than size elements in case n is not an even
                # multiple of size. Thus, we calculate accordingly
                hi = min(lo + size*2 - 1, n - 1)
                # the split point mid can be calculated as
                # mid = lo + size - 1
                # However, for the sake of clarity, let's calculate 
                # it as a function of lo and hi, as in the other methods.
                mid = lo + (lo + hi)//2

                # Now we merge the subarrays
                cls._merge(elements, lo, mid, hi, buffer)
            size *= 2

    @staticmethod
    def _merge(a, lo, mid, hi, buffer):
        i = lo
        j = mid + 1

        for k in range(lo, hi + 1):
            buffer[k] = a[k]

        for k in range(lo, hi + 1):
            if i > mid:
                a[k] = buffer[j]
                j += 1
            elif j > hi:
                a[k] = buffer[i]
                i += 1
            elif buffer[j] < buffer[i]:
                a[k] = buffer[j]
                j += 1
            else:
                a[k] = buffer[i]
                i += 1

if __name__ == "__main__":
    a = [2, 4, 1, 8, 5, 0, 9, 2]
    print(TopDownMergeSort.sort(a))

    b = [2, 4, 1, 8, 5, 0, 9, 2]
    TopDownMergeSort2.sort(b)
    print(b)

    c = [2, 4, 1, 8, 5, 0, 9, 2]
    TopDownMergeSort3.sort(c)
    print(c)

    d = [9, 2, 0, 2, 1, 4, 5, 8, 0]
    TopDownMergeSort4.sort(d)
    print(d)

    e = [9, 2, 0, 2, 1, 4, 5, 8, 0, 12]
    BottomUpMergeSort.sort(e)
    print(e)

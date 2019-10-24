import random

class QSortRec:
    @classmethod
    def sort(cls, a):
        cls._qsort(a, 0, len(a) - 1)

    @classmethod
    def _qsort(cls, a, start, end):
        n = end - start + 1
        if n <= 1:
            return
        pivot = cls._partition(a, start, end)
        cls._qsort(a, start, pivot - 1)
        cls._qsort(a, pivot + 1, end)

    @classmethod
    def _partition(cls, a, start, end):
        pivot = a[start]
        i = start + 1
        for j in range(i, end + 1):
            if a[j] < pivot:
                swap(a, i, j)        
                i += 1
        swap(a, start, i - 1)
        return i - 1


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
    a =[2,4,1,8,5,0,]
    QSortRec.sort(a)
    print(a)

    b =[2,9,1,3,5,0,7]
    QSortRecRandomPivot.sort(b)
    print(b)
    
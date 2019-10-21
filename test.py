# 中值
def middlenum(array, length):
    array = qsort(array)
    if (length & 1) > 0:
        tmp = array[length / 2]
    else:
        tmp = (array[length / 2] + array[length / 2 + 1]) / 2
    return tmp


# 快排
def qsort(seq):
    if not seq:
        return seq
    else:
        pivot = seq[0]
        lesser = qsort([x for x in seq[1:] if x < pivot])
        greater = qsort([x for x in seq[1:] if x >= pivot])
        return lesser + [pivot] + greater

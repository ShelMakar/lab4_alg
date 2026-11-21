def selection_sort(spis:list) -> list:
    sorted_list = [i for i in spis]
    n = len(spis)
    for i in range(n - 1):
        index_min = i
        for j in range(i + 1, n):
            if sorted_list[index_min] > sorted_list[j]: index_min = j

        if index_min != i:
            sorted_list[index_min], sorted_list[i] = sorted_list[i], sorted_list[index_min]
    return sorted_list


def quick_sort(spis:list) -> list:
    another_spis = list(spis)
    return another_spis_quick_sort(another_spis)


def another_spis_quick_sort(spis:list) -> list:
    if len(spis) == 0 or len(spis) == 1: return spis
    pivo = spis[len(spis) // 2]
    pivo_bigger =[]
    pivo_equal = []
    pivo_smaller = []
    for i in spis:

        if i > pivo: pivo_bigger.append(i)
        elif i == pivo: pivo_equal.append(i)
        else: pivo_smaller.append(i)

    return another_spis_quick_sort(pivo_smaller) + pivo_equal + another_spis_quick_sort(pivo_bigger)

from copy import deepcopy

'''
https://www.codewars.com/kata/square-sums/train/python
'''


def square_sums(num):
    nums = list(range(1, num + 1))
    p = [[]]
    for i in nums:
        t = []
        for j in nums:
            if (i + j ** 0.5 % 1 == 0) and (i != j):
                t.append(j)
        p.append([i, t])
    for i in range(1, num + 1):
        r = calc(p[i], p, remove(nums, i), [i])
        if r: return r
    return False


def calc(cur, poten, rem, fill):
    if len(rem) == 0:
        return fill
    for num in cur[1]:
        if num in rem:
            t = calc(poten[num], poten, remove(rem, num), add(fill, num))
            if t: return t
            pass


def remove(val, v):
    t = deepcopy(val)
    t.remove(v)
    return t


def add(val, v):
    t = deepcopy(val)
    t.append(v)
    return t

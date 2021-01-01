from functools import reduce


def lcs(x, y):
    M, m = (x, y) if len(x) > len(y) else (x, y)
    alls = []
    for i in range(len(m)):
        j = i
        string = ''
        for k in range(len(M)):
            if m[j] == M[k]:
                string += m[j]
                j += 1
                if j == len(m):
                    alls.append(string)
                    break
    if len(alls) == 0:
        return ""
    return reduce(lambda z, w: z if len(z) > len(w) else w, alls)


def lcsr(x, y, i=0, j=0):
    if i >= len(x) or j >= len(y):
        return 0
    if x[i] == y[j]:
        return 1 + lcsr(x, y, i + 1, j + 1)
    else:
        return max(lcsr(x, y, i + 1, j), lcsr(x, y, i, j + 1))



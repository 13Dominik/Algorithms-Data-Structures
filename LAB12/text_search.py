# Algorithms to search patterns in text
# Dominik Tomalczyk

import time

with open("lotr.txt", encoding='utf-8') as f:
    text = f.readlines()

S = ' '.join(text).lower()


def naive_algo(S, W):
    m, i = 0, 0
    operations = 0  # number of operations (compare) durning algorithm
    found = []  # indexes of start every found pattern
    while m + len(W) - 1 < len(S):
        operations += 1
        if S[i:m + len(W)] == W:
            found.append(m)
        m += 1
        i += 1
    return len(found), operations


def __hash(word):
    d = 256
    q = 101
    N = len(word)
    hw = 0

    for i in range(N):
        hw = (hw * d + ord(word[
                               i])) % q
    return hw


def Rabin_Karp(S, W):
    M = len(S)
    N = len(W)

    hW = __hash(W)

    operations = 0
    collisions = 0
    found = []
    d = 256
    q = 101

    h = 1
    for i in range(N - 1):
        h = (h * d) % q

    m = 0
    hS = __hash(S[m:m + N])
    while m < M - N + 1:
        operations += 1
        if hS == hW:
            if S[m:m + N] == W:
                found.append(m)
            else:
                collisions += 1
        if m + N < M:  # not compute new hS on last element (indexError)
            hS = (d * (hS - ord(S[m]) * h) + ord(S[m + N])) % q
        m += 1
    return len(found), operations, collisions


def kmp_table(W):
    pos = 1
    cnd = 0
    T = [0 for _ in range(len(W) + 1)]
    T[0] = -1

    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1

    T[pos] = cnd
    return T


def kmp_search(S, W):
    m, i = 0, 0
    T = kmp_table(W)
    P = []
    nP = 0
    operations = 0
    while m < len(S):
        operations += 1
        if W[i] == S[m]:
            m += 1
            i += 1
            if i == len(W):
                P.append(m - i)
                nP += 1
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    return len(P), operations


print(naive_algo(S, "time.")[0], ";", naive_algo(S, "time.")[1])
print(Rabin_Karp(S, "time.")[0], ";", Rabin_Karp(S, "time.")[1], ";", Rabin_Karp(S, "time.")[2])
print(kmp_search(S, "time.")[0], ";", kmp_search(S, "time.")[1])

# t_start1 = time.perf_counter()
# naive_algo(S, "time.")
# t_stop1 = time.perf_counter()
# print("Czas obliczeń:", "{:.7f}".format(t_stop1 - t_start1))
# #
# t_start2 = time.perf_counter()
# Rabin_Karp(S, "time")
# t_stop2 = time.perf_counter()
# print("Czas obliczeń:", "{:.7f}".format(t_stop2 - t_start2))
#
# t_start3 = time.perf_counter()
# kmp_search(S, "time.")
# t_stop3 = time.perf_counter()
# print("Czas obliczeń:", "{:.7f}".format(t_stop3 - t_start3))

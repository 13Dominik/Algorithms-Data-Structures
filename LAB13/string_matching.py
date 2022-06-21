# Algorithms using dynamic programming to search pattern in string
# Dominik Tomalczyk

import numpy as np


def string_compare(P, T, i, j):
    if i == 0:
        return j
    if j == 0:
        return i

    changes = string_compare(P, T, i - 1, j - 1) + int(P[i] != T[j])
    inserts = string_compare(P, T, i, j - 1) + 1
    deletes = string_compare(P, T, i - 1, j) + 1

    lowest_cost = min(changes, inserts, deletes)

    return lowest_cost


def string_compare_pd(P, T, k, l):
    D = np.zeros((len(P), len(T)))
    for i in range(len(T)):
        D[0][i] = i
    for j in range(len(P)):
        D[j][0] = j

    R = np.chararray((len(P), len(T)))
    for i in range(len(R)):
        for j in range(len(R[0])):
            R[i][j] = "X"
    R = R.astype("U256")
    for i in range(1, len(R[0])):
        R[0][i] = "I"
    for j in range(1, len(R)):
        R[j][0] = "D"

    for i in range(1, k + 1):
        for j in range(1, l + 1):
            changes = D[i - 1][j - 1] + int(P[i] != T[j])
            inserts = D[i][j - 1] + 1
            deletes = D[i - 1][j] + 1
            lowest_cost = min(changes, inserts, deletes)
            D[i][j] = lowest_cost

            if changes <= inserts and changes <= deletes:
                if P[i] == T[j]:
                    R[i][j] = "M"
                else:
                    R[i][j] = "S"
            elif inserts < changes and inserts < deletes:
                R[i][j] = "I"
            else:
                R[i][j] = "D"

    return D[k][l], R


def path_reconstruction(R):
    i = len(R) - 1
    j = len(R[0]) - 1
    l = []
    current = R[i][j]
    while current != "X":
        if current == "M" or current == "S":
            i -= 1
            j -= 1
        elif current == "D":
            i -= 1
        else:
            j -= 1
        l.append(current)
        current = R[i][j]
    l.reverse()
    return "".join(l)


# d)
def string_compare_pd2(P, T, k, l):
    D = np.zeros((len(P), len(T)))
    # for i in range(len(T)):
    #     D[0][i] = i
    for j in range(len(P)):
        D[j][0] = j

    R = np.chararray((len(P), len(T)))
    for i in range(len(R)):
        for j in range(len(R[0])):
            R[i][j] = "X"
    R = R.astype("U256")
    for i in range(1, len(R[0])):
        R[0][i] = "X"
    for j in range(1, len(R)):
        R[j][0] = "D"

    for i in range(1, k + 1):
        for j in range(1, l + 1):
            if P[i] != T[j]:
                changes = D[i - 1][j - 1] + 1000
            else:
                changes = D[i - 1][j - 1]
            inserts = D[i][j - 1] + 1
            deletes = D[i - 1][j] + 1
            lowest_cost = min(changes, inserts, deletes)
            D[i][j] = lowest_cost

            if changes <= inserts and changes <= deletes:
                if P[i] == T[j]:
                    R[i][j] = "M"
                else:
                    R[i][j] = "S"
            elif inserts < changes and inserts < deletes:
                R[i][j] = "I"
            else:
                R[i][j] = "D"
    i_ = len(P) - 1
    j_ = 0
    for k in range(1, len(T)):
        if D[i_][k] < D[i_][j_]:
            j_ = k
    return j_ - len(P) + 2


# e)
def string_compare_pd3(P, T, k, l):
    D = np.zeros((len(P), len(T)))
    for i in range(len(T)):
        D[0][i] = i
    for j in range(len(P)):
        D[j][0] = j

    R = np.chararray((len(P), len(T)))
    for i in range(len(R)):
        for j in range(len(R[0])):
            R[i][j] = "X"
    R = R.astype("U256")
    for i in range(1, len(R[0])):
        R[0][i] = "I"
    for j in range(1, len(R)):
        R[j][0] = "D"

    for i in range(1, k + 1):
        for j in range(1, l + 1):
            if P[i] != T[j]:

                changes = D[i - 1][j - 1] + 10000
            else:
                changes = D[i - 1][j - 1]
            inserts = D[i][j - 1] + 1
            deletes = D[i - 1][j] + 1
            lowest_cost = min(changes, inserts, deletes)
            D[i][j] = lowest_cost

            if changes <= inserts and changes <= deletes:
                if P[i] == T[j]:
                    R[i][j] = "M"
                else:
                    R[i][j] = "S"
            elif inserts < changes and inserts < deletes:
                R[i][j] = "I"
            else:
                R[i][j] = "D"

    return D[k][l], R


def longest_sequention_reconstruction(P, T, R):
    i = len(R) - 1
    j = len(R[0]) - 1
    l = []
    current = R[i][j]
    while current != "X":
        if current == "M" or current == "S":
            i -= 1
            j -= 1
        elif current == "D":
            i -= 1
        else:
            j -= 1

        if current == "M":
            l.append(P[i + 1])
        current = R[i][j]
    l.reverse()
    return "".join(l)


if __name__ == '__main__':
    # a)
    P = " kot"
    T = " koń"
    T2 = " pies"
    print("Koszt dla przykładu kot - koń:", string_compare(P, T, 3, 3))
    print("Koszt dla przykładu kot - pies:", string_compare(P, T2, 3, 4))
    # a)

    # b)
    Pb = ' biały autobus'
    Tb = ' czarny autokar'
    costb, Rb = string_compare_pd(Pb, Tb, len(Pb) - 1, len(Tb) - 1)
    print("Koszt dla przykładu z autobusami:", costb)
    # b)

    # c)
    Pc = ' thou shalt not'
    Tc = ' you should not'
    costc, Rc = string_compare_pd(Pc, Tc, len(Pc) - 1, len(Tc) - 1)
    assert "DSMMMMMISMSMMMM" == path_reconstruction(Rc)
    print("Ścieżka dla przykładu you should not:", path_reconstruction(Rc))
    # c)

    # d)
    P = ' ban'
    T = ' mokeyssbanana'
    start_index = string_compare_pd2(P, T, len(P) - 1, len(T) - 1)
    print("Indeks w którym zaczyna się ban:", start_index)
    # d)

    # e)
    Pe = ' democrat'
    Te = ' republican'
    e, e2 = string_compare_pd3(Pe, Te, len(Pe) - 1, len(Te) - 1)
    print("Najdluzsza wspolne sekwencja:", longest_sequention_reconstruction(Pe, Te, e2))
    # e)

    # f) 24579
    Pf = ' 243517698'
    Tf = "".join(sorted(Pf))
    f, f2 = string_compare_pd3(Pf, Tf, len(Pf) - 1, len(Tf) - 1)
    print("Najdłuższa podsekwencja monotoniczna:", longest_sequention_reconstruction(Pf, Tf, f2))
    # f)

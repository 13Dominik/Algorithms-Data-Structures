# Matrix
# Dominik Tomalczyk

class Matrix:
    def __init__(self, matrix, value=0):
        if isinstance(matrix, tuple):
            self._matrix = [[value] * matrix[1] for _ in range(matrix[0])]
        else:
            self._matrix = matrix

    def __add__(self, other):
        if self.size() != other.size():
            raise Exception("Wrong matrix shape!")

        new_list = []
        for row in range(self.size()[0]):
            new_list.append([self[row][i] + other[row][i] for i in range(self.size()[1])])
        return Matrix(new_list)

    def __mul__(self, other):
        if self.size()[1] != other.size()[0]:
            raise Exception("Wrong matrix shape!")

        new_matrix = Matrix((self.size()[0], other.size()[1]))
        for i in range(self.size()[0]):
            for j in range(other.size()[1]):
                for k in range(other.size()[0]):
                    new_matrix[i][j] += self[i][k] * other[k][j]
        return Matrix(new_matrix)

    def __str__(self):
        return "\n".join([str(row) for row in self._matrix])

    def size(self):
        return len(self._matrix), len(self._matrix[0])

    def __getitem__(self, item):
        return self._matrix[item]

    def __setitem__(self, key, value):
        self._matrix[key] = value


def transpose_matrix(matrix: Matrix) -> Matrix:
    new_matrix = Matrix((matrix.size()[1], matrix.size()[0]))
    for i in range(matrix.size()[0]):
        for j in range(matrix.size()[1]):
            new_matrix[j][i] = matrix[i][j]
    return new_matrix


def main():
    A = Matrix([[1, 0, 2],
                [-1, 3, 1]])
    B = Matrix((2, 3), value=1)
    C = Matrix([[3, 1],
                [2, 1],
                [1, 0]])

    print("Transposed matrix:")
    print(transpose_matrix(A))
    print("A + B")
    print(A + B)
    print("A * C")
    print(A * C)


if __name__ == '__main__':
    main()

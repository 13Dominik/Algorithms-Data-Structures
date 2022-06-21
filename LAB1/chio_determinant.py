# Computing matrix determinant using chio method
# Dominik Tomalczyk

# Matrix form previous exercise
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


def determinant_2x2(matrix: Matrix) -> float:
    """Computing determinant of 2x2 dimension matrix"""
    return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]


def recursive_chio(coeff: float, matrix: Matrix) -> float:
    """
    Recursive Chio method of computing determinant
    :param coeff:
    :param matrix: nxn matrix, n > 2
    :return: float
    """
    if matrix.size() == (2, 2):
        return coeff * determinant_2x2(matrix)

    # check if M(1,1) is 0, if so swap rows (not divide by zero)
    if matrix[0][0] == 0:
        # looking for a first correct row
        for i in range(matrix.size()[0] + 1):
            if matrix[i][0] != 0:  # first row with no 0 on first element
                matrix[0], matrix[i] = matrix[i], matrix[0]  # swapping rows

                coeff *= -1  # determinant changes sign !!!
                break
    # new coefficient is a product of previous coefficient and the current one
    new_coeff = coeff * 1 / (matrix[0][0] ** (matrix.size()[0] - 2))

    reduced_matrix = []  # new matrix with dimension n-1 to the next function call
    for i in range(matrix.size()[0] - 1):
        new_row = []
        for j in range(matrix.size()[0] - 1):
            # Chio method:
            new_row.append(
                determinant_2x2(Matrix([[matrix[0][0], matrix[0][j + 1]], [matrix[i + 1][0], matrix[i + 1][j + 1]]])))
        reduced_matrix.append(new_row)
    return recursive_chio(new_coeff, Matrix(reduced_matrix))


def compute_determinant(matrix: Matrix) -> float:
    """Computing determinant using Chio method"""
    if matrix.size() == (2, 2):
        return determinant_2x2(matrix)
    else:
        return recursive_chio(1.0, matrix)


if __name__ == '__main__':
    A = Matrix([[5, 1, 1, 2, 3],
                [4, 2, 1, 7, 3],
                [2, 1, 2, 4, 7],
                [9, 1, 0, 7, 0],
                [1, 4, 7, 2, 2]])
    B = Matrix([[0, 1, 1, 2, 3],
                [4, 2, 1, 7, 3],
                [2, 1, 2, 4, 7],
                [9, 1, 0, 7, 0],
                [1, 4, 7, 2, 2]])
    print(compute_determinant(A))
    print(compute_determinant(B))

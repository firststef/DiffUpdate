import numpy as np
from matcherinterface import MatcherInterface


class DiffUpdateMatcher(MatcherInterface):
    """
    This class handles the diff algorithm used in DBBFile

    similarity table
    _-----C---A---B---A---D--
    | 0 | 0 | 0 | 0 | 0 | 0 |
    |---|---|---|---|---|---|
    A 0 | 0 | 1 | 1 | 1 | 1 |
    |---|---|---|---|---|---|
    B 0 | 0 | 1 | 2 | 2 | 2 |
    |---|---|---|---|---|---|
    A 0 | 0 | 1 | 2 | 3 | 3 |
    |---|---|---|---|---|---|
    operations table
    _-----C---A---B---A---D--
    | 0 | 0<| 0 | 0 | 0 | 0 |
    |---|---\---|---|---|---|
    A 0 | 1 |\2<| 3 | 2 | 3 |
    |---|---|---\---|---|---|
    B 0 | 1 | 1 |\2<| 3 | 3 |
    |---|---|---|---\---|---|
    A 0 | 1 | 2 | 1 |\2<--3*|
    |---|---|---|---|---|---|

    by tracing the longest common subsequence we can determine the operations
    we need to do to optimally generate the diff:
    3->2->2->2->0
    0 *, 1 remove, 2 same, 3 add
    add D to y -> same A -> same B -> same A -> (add C to y / remove C from x)
    only that they are in reverse
    """

    def __init__(self):
        super().__init__()
        self.operations = b''

    @staticmethod
    def longest_common_subsequence(iter1: bytes, iter2: bytes):
        """
        Computes the operations to get from iter1 to iter2
        :param iter1: the byte string you start with
        :param iter2: the byte string you want to reach
        :return: a buffer with the operations
        """
        lcs_lengths = np.full((len(iter1) + 1, len(iter2) + 1), dtype=int, fill_value=0)
        matrix = np.full((len(iter1) + 1, len(iter2) + 1), dtype=int, fill_value=0)

        """
        0 none, 1 left, 2 diagonal, 3 up
        """
        for i in range(len(iter1) + 1):
            for j in range(len(iter2) + 1):
                if i == 0 or j == 0:
                    lcs_lengths[i][j] = 0
                    matrix[i][j] = 0
                elif iter1[i - 1] == iter2[j - 1]:
                    lcs_lengths[i][j] = lcs_lengths[i - 1][j - 1] + 1
                    matrix[i][j] = 2
                else:
                    if lcs_lengths[i - 1][j] >= lcs_lengths[i][j - 1]:
                        lcs_lengths[i][j] = lcs_lengths[i - 1][j]
                        matrix[i][j] = 1
                    else:
                        lcs_lengths[i][j] = lcs_lengths[i][j - 1]
                        matrix[i][j] = 3

        # Produce actual sequence by backtracking through pairs (i,j),
        # using computed lcsLen values to guide backtracking
        operations = b''

        i = len(iter1)
        j = len(iter2)

        last_operation = None
        current_operation = None
        ops = {
            'remove': 1,
            'same': 2,
            'add': 3,
            'remove_long': 4,
            'same_long': 5,
            'add_long': 6,
        }
        size_of_op = 0
        add_buffer = b''

        while True:
            if i <= 0 and j <= 0:
                break

            if matrix[i][j] == 2:
                last_operation = 'same'
                i -= 1
                j -= 1
            elif matrix[i][j] == 3:
                add_buffer = iter2[j - 1:j] + add_buffer
                last_operation = 'add'
                j -= 1
            elif matrix[i][j] == 1:
                last_operation = 'remove'
                i -= 1
            else:
                if j == 0:
                    last_operation = 'remove'
                    i -= 1
                elif i == 0:
                    add_buffer = iter2[j - 1:j] + add_buffer
                    last_operation = 'add'
                    j -= 1

            if current_operation is not None and last_operation != current_operation:
                if current_operation == 'add':
                    operations = add_buffer + operations
                    add_buffer = b''
                if size_of_op <= 255:
                    operations = size_of_op.to_bytes(1, byteorder="little") + operations
                    operations = ops[current_operation].to_bytes(1, "little") + operations
                else:
                    operations = size_of_op.to_bytes(4, byteorder="little") + operations
                    operations = ops[current_operation + '_long'].to_bytes(1, "little") + operations
                # print(current_operation + " " + str(size_of_op))
                size_of_op = 0

            size_of_op += 1
            current_operation = last_operation

        if current_operation is not None:
            if current_operation == 'add':
                operations = add_buffer + operations
            if size_of_op <= 255:
                operations = size_of_op.to_bytes(1, byteorder="little") + operations
                operations = ops[current_operation].to_bytes(1, "little") + operations
            else:
                operations = size_of_op.to_bytes(4, byteorder="little") + operations
                operations = ops[current_operation + '_long'].to_bytes(1, "little") + operations
            # print(current_operation + " " + str(size_of_op))

        return operations

    def do_diff(self, old, new):
        """
        Executes the algorithm and stores the operations internally
        :param old: start
        :param new: target
        :return: void
        """
        self.operations = DiffUpdateMatcher.longest_common_subsequence(old, new)

    def apply_diff(self, target):
        """
        Given the old file, apply the operations from the internal buffer to reach new file
        :param target: old file
        :return: the updated file buffer
        """

        result = b''
        ops = {
            'remove': b'\x01',
            'same': b'\x02',
            'add': b'\x03',
            'remove_long': b'\x04',
            'same_long': b'\x05',
            'add_long': b'\x06',
        }

        op_i = 0
        op_t = 0
        while op_i < len(self.operations):
            if self.operations[op_i:op_i + 1] == ops['same']:
                lent = int.from_bytes(self.operations[op_i+1:op_i+2], "little")
                op_i += 2
                result += target[op_t:op_t+lent]
                op_t += lent
            elif self.operations[op_i:op_i+1] == ops['add']:
                leni = int.from_bytes(self.operations[op_i+1:op_i+2], "little")
                op_i += 2
                result += self.operations[op_i:op_i+leni]
                op_i += leni
            elif self.operations[op_i:op_i + 1] == ops['remove']:
                lent = int.from_bytes(self.operations[op_i+1:op_i+2], "little")
                op_i += 2
                op_t += lent
            elif self.operations[op_i:op_i + 1] == ops['same_long']:
                lent = int.from_bytes(self.operations[op_i + 1:op_i + 5], "little")
                op_i += 5
                result += target[op_t:op_t + lent]
                op_t += lent
            elif self.operations[op_i:op_i + 1] == ops['add_long']:
                leni = int.from_bytes(self.operations[op_i + 1:op_i + 5], "little")
                op_i += 5
                result += self.operations[op_i:op_i + leni]
                op_i += leni
            elif self.operations[op_i:op_i + 1] == ops['remove_long']:
                lent = int.from_bytes(self.operations[op_i + 1:op_i + 5], "little")
                op_i += 5
                op_t += lent
        return result

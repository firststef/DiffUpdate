import numpy as np
from matcherinterface import MatcherInterface


class DiffUpdateMatcher(MatcherInterface):
    def __init__(self):
        super().__init__()
        self.operations = b''

    @staticmethod
    def longest_common_subsequence(iter1: bytes, iter2: bytes):
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
            'same': 1,
            'add': 2,
            'remove': 3,
            'same_long': 4,
            'add_long': 5,
            'remove_long': 6,
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
                if i == 0:
                    add_buffer = iter2[j - 1:j] + add_buffer
                    last_operation = 'add'
                    j -= 1
                elif j == 0:
                    last_operation = 'remove'
                    i -= 1

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
        self.operations = DiffUpdateMatcher.longest_common_subsequence(old, new)

    def do_operations(self, target):
        result = b''
        ops = {
            'same': b'\x01',
            'add': b'\x02',
            'remove': b'\x03',
            'same_long': b'\x04',
            'add_long': b'\x05',
            'remove_long': b'\x06',
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

    def apply_diff(self, target):
        return self.do_operations(target)

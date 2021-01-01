from abc import *


class MatcherInterface(metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @staticmethod
    def detect_method(file_path):
        pass

    @abstractmethod
    def do_diff(self, old_path, new_path):
        """ Converts differences between two files to a custom file format """

    @abstractmethod
    def apply_diff(self, target):
        """ Apply the changes specified in the diff file """

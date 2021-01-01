from abc import *


class MatcherInterface(metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @staticmethod
    def detect_method(file_path: str):
        pass

    @abstractmethod
    def do_diff(self, old_path: str, new_path: str):
        """ Converts differences between two files to a custom file format """

    @abstractmethod
    def apply_diff(self, target: str):
        """ Apply the changes specified in the diff file """

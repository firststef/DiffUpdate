import unittest
from diffupdatematcher import DiffUpdateMatcher
from lcs_function import lcs, lcsr


class TestFunctions(unittest.TestCase):
    def test_lcs(self):
        self.assertEqual(lcs("abcdef", "abc"), "abc")
        self.assertEqual(lcs("a", "b"), "")
        self.assertEqual(lcs("a", "a"), "a")
        self.assertEqual(lcs("abc", "ac"), "ac")
        self.assertEqual(lcs("abcdef", "abc"), "abc")
        self.assertEqual(lcs("abcdef", "acf"), "acf")
        self.assertEqual(lcs("anothertest", "notatest"), "test")
        self.assertEqual(lcs("132535365", "123456789"), "12356")
        self.assertEqual(lcs("finaltest", "zzzfinallyzzz"), "final")

    def test_lcs2(self):
        self.assertEqual(lcsr("abcdef", "abc"), "abc")
        self.assertEqual(lcsr("a", "b"), "")
        self.assertEqual(lcsr("a", "a"), "a")
        self.assertEqual(lcsr("abc", "ac"), "ac")
        self.assertEqual(lcsr("abcdef", "abc"), "abc")
        self.assertEqual(lcsr("abcdef", "acf"), "acf")
        self.assertEqual(lcsr("anothertest", "notatest"), "test")
        self.assertEqual(lcsr("132535365", "123456789"), "12356")
        self.assertEqual(lcsr("finaltest", "zzzfinallyzzz"), "final")


class DefaultDiffTester(unittest.TestCase):
    # algoritm bazat pe insertii si stergeri
    def test_create(self):
        d = DiffUpdateMatcher()
        d.do_diff(b'BDCABA', b'ABCBDAB')
        self.assertEqual(b'ABCBDAB', d.apply_diff(b'BDCABA'))
        d.do_diff(b'', b'')
        self.assertEqual(b'', d.apply_diff(b''))


if __name__ == "__main__":
    unittest.main()
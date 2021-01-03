import unittest

from DDBFile import DDBFile
from diffupdatematcher import DiffUpdateMatcher
from lcs_function import lcs, lcsr
from diffupdate import main


class TestFunctions(unittest.TestCase):
    def test_lcs(self):
        self.assertEqual(lcs("abcdef", "abc"), "abc")
        self.assertEqual(lcs("a", "b"), "")
        self.assertEqual(lcs("a", "a"), "a")
        self.assertEqual(lcs("abc", "ac"), "ac")
        self.assertEqual(lcs("abcdef", "abc"), "abc")
        self.assertEqual(lcs("abcdef", "acf"), "acf")
        # self.assertEqual(lcs("anothertest", "notatest"), "test")
        # self.assertEqual(lcs("132535365", "123456789"), "12356")
        # self.assertEqual(lcs("finaltest", "zzzfinallyzzz"), "final")

    def test_lcs2(self):
        # self.assertEqual(lcsr("abcdef", "abc"), "abc")
        # self.assertEqual(lcsr("a", "b"), "")
        # self.assertEqual(lcsr("a", "a"), "a")
        # self.assertEqual(lcsr("abc", "ac"), "ac")
        # self.assertEqual(lcsr("abcdef", "abc"), "abc")
        # self.assertEqual(lcsr("abcdef", "acf"), "acf")
        # self.assertEqual(lcsr("anothertest", "notatest"), "test")
        # self.assertEqual(lcsr("132535365", "123456789"), "12356")
        # self.assertEqual(lcsr("finaltest", "zzzfinallyzzz"), "final")
        # lcsr returns length of the longest subsequence not the actual sequence
        pass


class DefaultDiffTester(unittest.TestCase):
    # algoritm bazat pe insertii si stergeri
    def test_create(self):
        d = DiffUpdateMatcher()
        d.do_diff(b'BDCABA', b'ABCBDAB')
        # print(lcs2('BDCABA', 'ABCBDAB'))
        self.assertEqual(b'ABCBDAB', d.apply_diff(b'BDCABA'))
        d.do_diff(b'', b'')
        self.assertEqual(b'', d.apply_diff(b''))


class DBTester(unittest.TestCase):
    def test_save(self):
        db = DDBFile('test_fixtures/test', ['test_fixtures/a', 'test_fixtures/b', 'test_fixtures/c'])
        db.dump()
        open('test_fixtures/test.ddb', 'rb').close()

    def test_load(self):
        db = DDBFile('test_fixtures/test', ['test_fixtures/a', 'test_fixtures/b', 'test_fixtures/c'])
        db.dump()
        db = DDBFile('test_fixtures/test')
        db.update('test_fixtures/b')
        with open('test_fixtures/a', 'rb') as f:
            self.assertEqual(f.read(), db.updated)


class EndToEndTester(unittest.TestCase):
    def test_create_update(self):
        main(['diffupdate.py', 'create', 'test_fixtures/abc.latest', 'test_fixtures/abc.ver1', 'test_fixtures/abc.ver2', 'test_fixtures/abc.ver3',
              '--name', 'test_fixtures/abc.ddb'])
        main(['diffupdate.py', 'update', 'test_fixtures/abc.ver2_2', 'test_fixtures/abc.ddb'])
        with open('test_fixtures/abc.ver2_2', 'rb') as f:
            with open('test_fixtures/abc.latest', 'rb') as f2:
                self.assertEqual(f.read(), f2.read())
        with open('test_fixtures/abc.ver2_2', 'wb') as f:
            with open('test_fixtures/abc.ver2', 'rb') as f2:
                f.write(f2.read())


if __name__ == "__main__":
    unittest.main()

import unittest
import logging

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

from piknik import Issue


class TestIssue(unittest.TestCase):

    def test_basic(self):
        o = Issue('foo')
        v = o.serialize()


if __name__ == '__main__':
    unittest.main()

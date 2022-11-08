# standard imports
import unittest
import logging
import json

# local imports
from piknik import (
        Basket,
        Issue,
        )
from piknik.msg import IssueMessage

# test imports
from tests.common import TestStates

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()



class TestMsg(unittest.TestCase):

    def setUp(self):
        self.b = Basket(TestStates())


    def test_basic(self):
        o = Issue('foo')
        v = IssueMessage(o)


    def test_single_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:foo')


    def test_multi_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:foo', 's:bar', 's:baz')


    def test_single_file_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 'f:tests/one.png')


    def test_mixed_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:bar')
        m = self.b.msg(v, 'f:tests/one.png')
        m = self.b.msg(v, 's:baz')
        m = self.b.msg(v, 'f:tests/two.bin')
        print(m)


if __name__ == '__main__':
    unittest.main()

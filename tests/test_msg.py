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
        self.assertEqual(v.get('Subject'), 'foo')


    def test_single_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:foo')


    def test_multi_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:foo', 's:bar', 's:baz')
        print(m)


if __name__ == '__main__':
    unittest.main()

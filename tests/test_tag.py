# standard imports
import unittest
import logging

# external imports
import shep

# local imports
from piknik import (
        Basket,
        Issue,
        )
from piknik.error import DeadIssue

# tests imports
from tests.common import debug_out
from tests.common import TestStates

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


def debug_out(self, k, v):
    logg.debug('TRACE: {} {}'.format(k, v))


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.b = Basket(TestStates())


    def test_setget(self):
        o = Issue('foo')
        v = self.b.add(o)
        self.b.tag(v, 'inky')
        self.b.tag(v, 'pinky')
        self.b.untag(v, 'pinky')

 
if __name__ == '__main__':
    unittest.main()

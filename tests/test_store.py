# standard imports
import unittest
import logging
import tempfile
import shutil

# external imports
import shep

# local imports
from piknik import (
        Basket,
        Issue,
        )
from piknik.error import DeadIssue
from piknik.store import FileStoreFactory

# tests imports
from tests.common import debug_out
from tests.common import TestStates


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


def debug_out(self, k, v):
    logg.debug('TRACE: {} {}'.format(k, v))


class TestStore(unittest.TestCase):

    def setUp(self):
        self.d = tempfile.mkdtemp()
        logg.debug('tempdir is {}'.format(self.d))
        self.store_factory = FileStoreFactory(self.d)
        self.b = Basket(self.store_factory)


    def tearDown(self):
        shutil.rmtree(self.d)
        pass


    def test_basic(self):
        o = Issue('foo')
        v = self.b.add(o)


    def test_load(self):
        o = Issue('foo')
        va = self.b.add(o)

        o = Issue('bar')
        vb = self.b.add(o)
        
        self.b.advance(va)

        b = Basket(self.store_factory)
        print('get va {}'.format(va))
        r = b.get(va)


if __name__ == '__main__':
    unittest.main()

import unittest
import shep
import logging
import tempfile

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

from piknik import (
        Basket,
        Issue,
        )
from piknik.error import DeadIssue
from piknik.store import FileStoreFactory


def debug_out(self, k, v):
    logg.debug('TRACE: {} {}'.format(k, v))


class TestStore(unittest.TestCase):

    def setUp(self):
        self.d = tempfile.mkdtemp()
        store_factory = FileStoreFactory(self.d)
        self.b = Basket(store_factory.create)


    def tearDown(self):
        logg.debug('tempdir is {}'.format(self.d))
        pass


    def test_basic(self):
        o = Issue('foo')
        v = self.b.add(o)


if __name__ == '__main__':
    unittest.main()

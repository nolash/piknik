# standard imports
import unittest
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

from piknik import Issue
from piknik.identity import Identity


class TestAssign(unittest.TestCase):

    def setUp(self):
        self.alice = 'F3FAF668E82EF5124D5187BAEF26F4682343F692'

    def test_identity_pointer(self):
        check = "sha256:65ea9b0609341322903823660bf45326f473d903ee7d327dff442f46d68eacd9"
        p = Identity(self.alice)
        r = p.uri()
        self.assertEqual(r, check)


    def test_basic(self):
        o = Issue('foo')
        #p = Identity()


if __name__ == '__main__':
    unittest.main()

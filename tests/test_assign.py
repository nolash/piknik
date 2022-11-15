# standard imports
import unittest
import logging
import json

# local imports
from piknik import Issue
from piknik.identity import Identity

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestAssign(unittest.TestCase):

    def setUp(self):
        self.alice = 'F3FAF668E82EF5124D5187BAEF26F4682343F692'
        self.bob = 'F645E047EE5BC4E2824C94DB42DC91CFA8ABA02B'


    def test_identity_pointer(self):
        check = "sha256:65ea9b0609341322903823660bf45326f473d903ee7d327dff442f46d68eacd9"
        p = Identity(self.alice)
        r = p.uri()
        self.assertEqual(r, check)


    def test_identity_load(self):
        o = Issue('foo')
        alice = Identity(self.alice)
        o.assign(alice)
        bob = Identity(self.bob)
        o.assign(bob)
        r = o.get_assigned()
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0][0], alice)
        self.assertEqual(r[1][0], bob)
        self.assertGreater(r[1][1], r[0][1])


if __name__ == '__main__':
    unittest.main()

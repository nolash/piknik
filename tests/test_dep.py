# standard imports
import unittest
import logging
import json

# local imports
from piknik import Issue
from piknik.identity import Identity
from piknik.error import UnknownIdentityError
from piknik.error import ExistsError

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestAssign(unittest.TestCase):

    def setUp(self):
        self.alice = 'F3FAF668E82EF5124D5187BAEF26F4682343F692'
        self.bob = 'F645E047EE5BC4E2824C94DB42DC91CFA8ABA02B'


    def test_dep_basic(self):
        one = Issue('foo')
        one.dep('bar')
        one.dep('baz')
        with self.assertRaises(ExistsError):
            one.dep('bar')
        one.undep('bar')
        self.assertEqual(len(one.dependencies), 1)


if __name__ == '__main__':
    unittest.main()

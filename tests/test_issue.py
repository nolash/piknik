# standard imports
import unittest
import logging
import json

# local imports
from piknik import Issue
from piknik.identity import Identity

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestIssue(unittest.TestCase):

    def test_basic(self):
        o = Issue('foo')
        r = json.loads(str(o))
        self.assertEqual(str(o.id), r['id'])
        self.assertEqual(o.title, r['title'])


    def test_basic_from_str(self):
        o = Issue('foo')
        v = str(o)
        r = Issue.from_str(v)
        self.assertTrue(o == r)



    def test_assigned_from_str(self):
        o = Issue('foo')
        alice_fp = 'F3FAF668E82EF5124D5187BAEF26F4682343F692'
        alice = Identity(alice_fp)
        bob_fp = 'F645E047EE5BC4E2824C94DB42DC91CFA8ABA02B'
        bob = Identity(bob_fp)
        o.assign(alice)
        o.assign(bob)
        v = str(o)
        r = Issue.from_str(v)
        self.assertTrue(o == r)

        check = r.get_assigned()
        self.assertEqual(len(check), 2)


if __name__ == '__main__':
    unittest.main()

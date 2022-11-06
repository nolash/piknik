import unittest
import shep
import logging

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

from piknik import (
        Basket,
        Issue,
        )


def debug_out(self, k, v):
    logg.debug('TRACE: {} {}'.format(k, v))


def create_test_state(*args, **kwargs):
    return shep.State(6, *args, event_callback=debug_out, **kwargs)


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.b = Basket(create_test_state)

    
    def test_issue_basic(self):
        o = Issue('The first issue')
        v = self.b.add(o)
        self.assertEqual(v, o.id)
        r = self.b.get(o.id)
        self.assertEqual(r, o)


    def test_list(self):
        o = Issue('The first issue')
        self.b.add(o)
        o = Issue('The second issue')
        self.b.add(o)
        r = self.b.list('backlog')
        self.assertEqual(len(r), 2)


    def test_progress(self):
        o = Issue('The first issue')
        self.b.add(o)
        o = Issue('The second issue')
        self.b.add(o)
        self.b.doing(o.id)

        r = self.b.list('backlog')
        self.assertEqual(len(r), 1)

        r = self.b.list('doing')
        self.assertEqual(len(r), 1)


if __name__ == '__main__':
    unittest.main()

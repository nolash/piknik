import unittest
import shep
import logging

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

from piknik import (
        Basket,
        Issue,
        )
from piknik.error import DeadIssue


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


    def test_progres(self):
        o = Issue('The first issue')
        self.b.add(o)
        self.b.advance(o.id)
        self.b.advance(o.id)
        self.b.advance(o.id)
        self.b.advance(o.id)
        with self.assertRaises(DeadIssue):
            self.b.advance(o.id)
            

    def test_list_jump(self):
        o = Issue('The first issue')
        self.b.add(o)
        o_two = Issue('The second issue')
        self.b.add(o_two)
        self.b.doing(o.id)

        r = self.b.list('backlog')
        self.assertEqual(len(r), 1)

        r = self.b.list('doing')
        self.assertEqual(len(r), 1)


    def test_jump(self):
        o = Issue('The first issue')
        self.b.add(o)
        self.b.doing(o.id)
        r = self.b.list('doing')
        self.assertEquals(len(r), 1)
        self.b.review(o.id)
        r = self.b.list('review')
        self.assertEquals(len(r), 1)
        self.b.backlog(o.id)
        r = self.b.list('backlog')
        self.assertEquals(len(r), 1)
        self.b.finish(o.id)
        r = self.b.list('finished')
        self.assertEquals(len(r), 1)


    def test_magic_unblock(self):
        o = Issue('The first issue')
        self.b.add(o)
        self.b.advance(o.id)
        self.b.block(o.id)
        self.assertIn(o.id, self.b.blocked())
        self.b.advance(o.id)
        self.assertNotIn(o.id, self.b.blocked())


    def test_no_resurrect(self):
        o = Issue('The first issue')
        self.b.add(o)
        self.b.finish(o.id)
        with self.assertRaises(DeadIssue):
            self.b.doing(o.id)


if __name__ == '__main__':
    unittest.main()

# standard imports
import unittest
import logging
import json
from email.message import Message

# local imports
from piknik import (
        Basket,
        Issue,
        )
from piknik.msg import IssueMessage

# test imports
from tests.common import TestStates
from tests.common import TestMsgStore

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


def test_wrapper(p):
    m = Message()
    m.add_header('Foo', 'bar')
    m.set_type('multipart/relative')
    m.set_payload(p)
    return m


class TestMsg(unittest.TestCase):

    def setUp(self):
        self.store = TestStates()
        self.b = Basket(self.store)


    def test_basic(self):
        o = Issue('foo')
        v = IssueMessage(o)


    def test_single_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:foo')


    def test_multi_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:foo', 's:bar', 's:baz')


    def test_single_file_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 'f:tests/one.png')


    def test_mixed_content(self):
        o = Issue('foo')
        v = self.b.add(o)
        m = self.b.msg(v, 's:bar')
        m = self.b.msg(v, 'f:tests/one.png')
        m = self.b.msg(v, 's:baz')
        m = self.b.msg(v, 'f:tests/two.bin')


    def test_wrapper(self):
        b = Basket(self.store, message_wrapper=test_wrapper)
        o = Issue('bar')
        v = b.add(o)
        m = b.msg(v, 's:foo')
        print(m)


if __name__ == '__main__':
    unittest.main()

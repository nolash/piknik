# standard imports
import unittest
import logging
import json
import shutil
import io
import tempfile
from email.message import Message
from email.utils import localtime as email_localtime

# external imports
from mimeparse import parse_mime_type

# local imports
from piknik import (
        Basket,
        Issue,
        )
from piknik.msg import IssueMessage
from piknik.render.base import Renderer

# test imports
from tests.common import TestStates
from tests.common import TestMsgStore
from tests.common import pgp_setup

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


def test_wrapper(p):
    m = Message()
    m.add_header('Foo', 'bar')
    m.set_type('multipart/relative')
    m.add_header('X-Piknik-Envelope', 'foo')
    m.set_payload(p)
    return m


def test_unwrapper(msg, message_callback=None, part_callback=None):
    for v in msg.walk():
        if message_callback != None:
            message_callback(v)


class TestRenderer(Renderer):

    def __init__(self, basket, accumulator=None):
        super(TestRenderer, self).__init__(basket, accumulator=accumulator)
        self.c = 0


    def apply_message(self, state, issue, tags, envelope, message, accumulator=None):
        r = self.c
        self.c += 1
        return r


class TestMsg(unittest.TestCase):

    def setUp(self):
        self.acc = []
        def accumulate(v):
            self.acc.append(v)

        #(self.crypto, self.gpg, self.gpg_dir) = pgp_setup()
        self.store = TestStates()
        self.b = Basket(self.store, message_wrapper=test_wrapper) #, message_wrapper=self.crypto.sign)
        self.render_dir = tempfile.mkdtemp()
        self.renderer = TestRenderer(self.b, accumulator=accumulate) #outdir=self.render_dir)


    def tearDown(self):
        #logg.debug('look in {}'.format(self.render_dir))
        shutil.rmtree(self.render_dir)


    def test_idlepass(self):
        issue_one = Issue('foo')
        self.b.add(issue_one)

        issue_two = Issue('bar')
        v = self.b.add(issue_two)

        m = self.b.msg(v, 's:foo')

        self.renderer.apply()
        self.assertEqual(len(self.acc), 1)


if __name__ == '__main__':
    unittest.main()

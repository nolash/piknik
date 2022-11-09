# standard imports
import os
import unittest
import logging
import json
import shutil
from email.message import Message

# local imports
from piknik import Basket
from piknik import Issue

# test imports
from tests.common import TestStates
from tests.common import TestMsgStore
from tests.common import pgp_setup

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

test_dir = os.path.realpath(os.path.dirname(__file__))


class TestMsg(unittest.TestCase):

    def setUp(self):
        self.store = TestStates()
        (self.crypto, self.gpg, self.gpg_dir) = pgp_setup()
        self.b = Basket(self.store, message_wrapper=self.crypto.sign, message_verifier=self.crypto.verify)


    def tearDown(self):
        shutil.rmtree(self.gpg_dir)


    def test_wrap_sig(self):
        m = Message()
        m.set_type('multipart/mixed')
        m.set_payload(None)

        one = Message()
        one.set_charset('utf-8')
        one.set_payload('foo')
        m.attach(one)

        two = Message()
        two.set_charset('utf-8')
        two.set_payload('bar')
        m.attach(two)

        m = self.crypto.sign(m, passphrase='foo')
        self.crypto.verify(m)


    def test_wrap_double_sig(self):
        mp = Message()
        mp.set_type('multipart/related')
        mp.set_payload(None)

        m = Message()
        m.add_header('X-Piknik-Msg-Id', 'foo')
        m.set_type('multipart/mixed')
        m.set_payload(None)

        one = Message()
        one.set_charset('utf-8')
        one.set_payload('inky')
        m.attach(one)

        two = Message()
        two.set_charset('utf-8')
        two.set_payload('pinky')
        m.attach(two)

        m = self.crypto.sign(m, passphrase='foo')
        mp.attach(m)

        m = Message()
        m.add_header('X-Piknik-Msg-Id', 'bar')
        m.set_type('multipart/mixed')
        m.set_payload(None)

        one = Message()
        one.set_charset('utf-8')
        one.set_payload('blinky')
        m.attach(one)

        two = Message()
        two.set_charset('utf-8')
        two.set_payload('clyde')
        m.attach(two)

        m = self.crypto.sign(m, passphrase='foo')
        mp.attach(m)

        r = self.crypto.verify(mp)
        self.assertEqual(len(r), 2)
        self.assertIn('foo', r)
        self.assertIn('bar', r)


    # TODO: assert
    def test_wrap_basket_sig(self):
        o = Issue('foo')
        v = self.b.add(o)
        r = self.b.msg(v, 's:foo', 's:bar')
        print(r)


    def test_wrap_basket_sig(self):
        o = Issue('foo')
        v = self.b.add(o)
        r = self.b.msg(v, 's:foo', 's:bar')


if __name__ == '__main__':
    unittest.main()

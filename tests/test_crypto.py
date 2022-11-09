# standard imports
import os
import unittest
import logging
import json
import tempfile
import shutil
from email.message import Message

# external imports
import gnupg

# local imports
from piknik import Basket
from piknik import Issue
from piknik.crypto import PGPSigner

# test imports
from tests.common import TestStates
from tests.common import TestMsgStore

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

test_dir = os.path.realpath(os.path.dirname(__file__))


class TestMsg(unittest.TestCase):

    def setUp(self):
        self.store = TestStates()
        self.gpg_dir = tempfile.mkdtemp()
        self.gpg = gnupg.GPG(gnupghome=self.gpg_dir)
        gpg_input = self.gpg.gen_key_input(key_type='RSA', key_length=1024, passphrase='foo')
        gpg_key = self.gpg.gen_key(gpg_input)
        self.crypto = PGPSigner(self.gpg_dir, default_key=gpg_key.fingerprint, passphrase='foo')
        self.b = Basket(self.store, message_wrapper=self.crypto.sign)


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

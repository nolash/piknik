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
        gpg = gnupg.GPG(gnupghome=self.gpg_dir)
        gpg_input = gpg.gen_key_input(key_type='RSA', key_length=1024, passphrase='foo')
        gpg_key = gpg.gen_key(gpg_input)
        self.crypto = PGPSigner(self.gpg_dir, default_key=gpg_key.fingerprint, passphrase='foo')
        self.b = Basket(self.store, message_wrapper=self.crypto.sign)


    def tearDown(self):
        shutil.rmtree(self.gpg_dir)

    def test_wrap_sig(self):
        m = Message()
        m.set_charset('utf-8')
        m.set_payload('foo')
        r = self.crypto.sign(m, passphrase='foo')
        print(str(r))


    def test_wrap_basket_sig(self):
        o = Issue('foo')
        v = self.b.add(o)
        r = self.b.msg(v, 's:foo', 's:bar')
        print(r)




if __name__ == '__main__':
    unittest.main()

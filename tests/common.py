# standard imports
import logging
import tempfile

# external imports
import shep
import gnupg

logg = logging.getLogger()


def debug_out(self, k, v):
    logg.debug('TRACE: {} {}'.format(k, v))


class TestMsgStore:

    def __init__(self):
        self.store = {}

    def put(self, k, v):
        self.store[k] = v

    def get(self, k):
        try:
            return self.store[k]
        except KeyError:
            pass
        raise FileNotFoundError(k)


    def purge(self, k):
        del self.store[k]


class TestStates:

    def create_states(self, *args, **kwargs):
        return shep.State(6, *args, event_callback=debug_out, **kwargs)


    def create_tags(self, *args, **kwargs):
        return shep.State(0, *args, event_callback=debug_out, check_alias=False, **kwargs)


    def create_messages(self, *args):
        return TestMsgStore()


    def create_aliases(self, *args):
        return TestMsgStore()


def pgp_setup():
    from piknik.crypto import PGPSigner
    gpg_dir = tempfile.mkdtemp()
    gpg = gnupg.GPG(gnupghome=gpg_dir)
    gpg_input = gpg.gen_key_input(key_type='RSA', key_length=1024, passphrase='foo')
    gpg_key = gpg.gen_key(gpg_input)
    crypto = PGPSigner(gpg_dir, default_key=gpg_key.fingerprint, passphrase='foo')
    return (crypto, gpg, gpg_dir,)

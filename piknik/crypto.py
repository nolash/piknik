# standard imports
from email.message import Message

# external imports
import gnupg


class PGPSigner:

    def __init__(self, home_dir=None, default_key=None, passphrase=None):
        self.gpg = gnupg.GPG(gnupghome=home_dir)
        self.default_key = default_key
        self.passphrase = passphrase


    def sign(self, msg, passphrase=None): # msg = IssueMessage object
        m = Message()
        v = msg.as_string()
        m.set_type('multipart/relative')
        ms = Message()
        ms.set_type('application/pgp-signature')
        fn = '{}.asc'.format(msg.get('X-Piknik-Msg-Id'))
        ms.add_header('Content-Disposition', 'attachment', filename=fn)

        sig = self.gpg.sign(v, keyid=self.default_key, detach=True, passphrase=self.passphrase)
        ms.set_payload(str(sig))
    
        m.attach(msg)
        m.attach(ms)

        return m

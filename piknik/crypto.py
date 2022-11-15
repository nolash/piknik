# standard imports
import os
import logging
import tempfile
from email.message import Message

# external imports
import gnupg

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()
logging.getLogger('gnupg').setLevel(logging.ERROR)



class CorruptEnvelope(Exception):
    pass


class InvalidSignature(Exception):
    pass


class PGPSigner:

    def __init__(self, home_dir=None, default_key=None, passphrase=None, use_agent=False):
        self.gpg = gnupg.GPG(gnupghome=home_dir)
        self.default_key = default_key
        self.passphrase = passphrase
        self.use_agent = use_agent


    def sign(self, msg, passphrase=None): # msg = IssueMessage object
        m = Message()
        v = msg.as_string()
        m.set_type('multipart/relative')
        m.add_header('X-Piknik-Envelope', 'pgp')
        ms = Message()
        ms.set_type('application/pgp-signature')
        fn = '{}.asc'.format(msg.get('X-Piknik-Msg-Id'))
        ms.add_header('Content-Disposition', 'attachment', filename=fn)

        sig = self.gpg.sign(v, keyid=self.default_key, detach=True, passphrase=self.passphrase)
        ms.set_payload(str(sig))
    
        m.attach(msg)
        m.attach(ms)

        return m


    def __verify_msg(self, m, ms):
        v = m.as_string()
        sig = ms.get_payload()
        (fd, fp) = tempfile.mkstemp()
        f = os.fdopen(fd, 'w')
        f.write(sig)
        f.close()
        r = self.gpg.verify_data(fp, v.encode('utf-8'))
        os.unlink(fp)
        if r.key_status != None:
            raise InvalidSignature('key status {}'.format(r.key_status))
        if r.status != 'signature valid':
            raise InvalidSignature('invalid signature')
        logg.debug('signature ok')


    def verify(self, msg): # msg = IssueMessage object
        in_envelope = False
        message_ids = []
        envelope_message = None
        message_id = None
        for m in msg.walk():
            if m.get('X-Piknik-Envelope') == 'pgp':
                logg.debug('detected pgp envelope')
                in_envelope = True
            elif in_envelope:
                if envelope_message != None:
                    if m.get('X-Piknik-Envelope') != None:
                        raise CorruptEnvelope()
                    if m.get('Content-Type') == 'application/pgp-signature':
                        self.__verify_msg(envelope_message, m)
                        logg.debug('pgp signature for message id "{}" ok'.format(message_id))
                        message_ids.append(message_id)

                        in_envelope = False
                        envelope_message = None
                        message_id = None
                else:
                    message_id = m.get('X-Piknik-Msg-Id')
                    logg.debug('checking envelope for message id "{}"'.format(message_id))
                    envelope_message = m
        return message_ids

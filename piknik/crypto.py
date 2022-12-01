# standard imports
import os
import logging
import tempfile
from email.message import Message

# external imports
import gnupg

# local imports
from piknik.error import VerifyError
from piknik.msg import MessageEnvelope

logg = logging.getLogger()
logging.getLogger('gnupg').setLevel(logging.ERROR)


class PGPSigner:

    def __init__(self, home_dir=None, default_key=None, passphrase=None, use_agent=False, skip_verify=False):
        self.gpg = gnupg.GPG(gnupghome=home_dir)
        self.default_key = default_key
        self.passphrase = passphrase
        self.use_agent = use_agent
        self.__envelope_state = -1 # -1 not in envelope, 0 in outer envelope, 1 inner envelope, not (yet) valid, 2 envelope valid (with signature)
        self.__envelope = None
        self.__skip_verify = skip_verify


    def set_from(self, msg, passphrase=None):
        r = None
        for v in self.gpg.list_keys(True):
            if self.default_key == None or v['fingerprint'].upper() == self.default_key.upper():
                r = v['uids'][0]
                break
        if r == None:
            raise UnknownIdentityError('no signing keys found')
        msg.add_header('From', r)


    def sign(self, msg, passphrase=None): # msg = IssueMessage object
        m = Message()
        v = msg.as_string()
        m.set_type('multipart/relative')
        m.add_header('X-Piknik-Envelope', 'pgp')
        ms = Message()
        ms.set_type('application/pgp-signature')
        fn = '{}.asc'.format(msg.get('X-Piknik-Msg-Id'))
        ms.add_header('Content-Disposition', 'attachment', filename=fn)

        self.set_from(msg, passphrase=passphrase)
        sig = self.gpg.sign(v, keyid=self.default_key, detach=True, passphrase=self.passphrase)
        ms.set_payload(str(sig))
    
        m.attach(msg)
        m.attach(ms)

        return m

    
    def envelope_callback(self, msg, env_header):
        self.__envelope = None
        if env_header != 'pgp':
            raise VerifyError('expected envelope type "pgp", but got {}'.format(env_header))
        if self.__envelope_state > -1 and self.__envelope_state < 2:
            raise VerifyError('new envelope before previous was verified ({})'.format(self.__envelope_state))
        self.__envelope = msg
        self.__envelope_state = 0
        return MessageEnvelope(msg)


    def message_callback(self, envelope, msg, message_id):
        if msg.get('From') != None:
            envelope.sender = msg.get('From')

        if self.__envelope_state == 0:
            self.__envelope_state = 1
            self.__envelope = msg
            return (envelope, msg,)

        if msg.get('Content-Type') != 'application/pgp-signature':
            return (envelope, msg,)

        v = self.__envelope.as_string()
        sig = msg.get_payload()
        (fd, fp) = tempfile.mkstemp()
        f = os.fdopen(fd, 'w')
        f.write(sig)
        f.close()
        r = self.gpg.verify_data(fp, v.encode('utf-8'))
        os.unlink(fp)
        
        if r.key_status != None:
            raise VerifyError('unexpeced key status {}'.format(r.key_status))
        if r.status == 'no public key':
            logg.warning('public key for {} not found, cannot verify'.format(r.fingerprint))
        elif r.status != 'signature valid':
            if self.__skip_verify:
                logg.warning('invalid signature for message {}'.format(message_id))
            else:
                raise VerifyError('invalid signature for message {}'.format(message_id))
        else:
            logg.debug('signature ok from {}'.format(r.fingerprint))
            envelope.valid = True
        #envelope.sender = r.fingerprint
        self.__envelope_state = 2

        return (envelope, msg,)

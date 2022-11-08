# standard imports
import logging
import uuid
import mimetypes
from base64 import b64encode

#from email.message import EmailMessage as Message
from email.message import Message
from email import message_from_string
from email.policy import Compat32


logg = logging.getLogger(__name__)


class IssueMessage:

    def __init__(self, issue):
        self.__m = Message()

        self.__m.add_header('Subject', issue.title)
        self.__m.add_header('X-Piknik-Id', issue.id)
        self.__m.set_payload(None)
        self.__m.set_type('multipart/mixed')
        self.__m.set_boundary(str(uuid.uuid4()))


    @classmethod
    def parse(cls, issue, v):
        o = cls(issue)
        o.__m = message_from_string(v)
        return o


    def add_text(self, m, v):
        p = Message()
        p.add_header('Content-Transfer-Encoding', 'QUOTED-PRINTABLE')
        p.set_charset('UTF-8')
        p.set_payload(str(v))
        m.attach(p)


    def detect_file(self, v):
        return mimetypes.guess_type(v)


    def add_file(self, m, v):
        mime_type = self.detect_file(v)

        p = Message()
        p.set_type(mime_type[0])
        if mime_type[1] != None:
            p.set_charset(mime-type[1])
        p.add_header('Content-Transfer-Encoding', 'BASE64')

        f = open(v, 'rb')
        r = f.read()
        f.close()
        r = b64encode(r)

        p.set_payload(str(r))
        m.attach(p)


    def add(self, *args, related_id=None):
        m_id = uuid.uuid4()
        m = Message()
        m.add_header('X-Piknik-Msg-Id', str(m_id))
        if related_id != None:
            m.add_header('In-Reply-To', related_id)
        m.set_payload(None)
        m.set_type('multipart/mixed')
        m.set_boundary(str(uuid.uuid4()))
        for a in args:
            p = a[:2]
            v = a[2:]
            if p == 'f:':
                self.add_file(m, v)
            elif p == 's:':
                self.add_text(m, v)
        self.__m.attach(m)


    def as_string(self, **kwargs):
        return self.__m.as_string(**kwargs)


    def as_bytes(self, **kwargs):
        return self.__m.as_bytes(**kwargs)


    def __str__(self):
        return self.as_string()

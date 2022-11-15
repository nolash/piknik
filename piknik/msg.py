# standard imports
import logging
import uuid
import mimetypes
from base64 import b64encode
import time

#from email.message import EmailMessage as Message
from email.message import Message
from email import message_from_string
from email.policy import Compat32
from email.utils import formatdate


logg = logging.getLogger(__name__)


class IssueMessage:

    def __init__(self, issue):
        self.__m = Message()

        self.__m.add_header('Subject', issue.title)
        self.__m.add_header('X-Piknik-Id', issue.id)
        self.__m.add_header('Date', formatdate(time.time()))
        self.__m.set_payload(None)
        self.__m.set_type('multipart/relative')
        self.__m.set_boundary(str(uuid.uuid4()))


    @classmethod
    def parse(cls, issue, v, verifier=None):
        o = cls(issue)
        m = message_from_string(v)
        if verifier != None:
            verifier(m)
        o.__m = m
        return o


    def from_text(self, v):
        m = Message()
        m.add_header('Content-Transfer-Encoding', 'QUOTED-PRINTABLE')
        m.set_charset('UTF-8')
        m.set_payload(str(v))
        return m


    def detect_file(self, v):
        r = mimetypes.guess_type(v)
        if r[0] == None:
            return ('application/octet-stream', None,)
        return r


    def from_file(self, v):
        m = Message()
        
        mime_type = self.detect_file(v)
        m.set_type(mime_type[0])

        if mime_type[1] != None:
            m.set_charset(mime-type[1])
        m.add_header('Content-Transfer-Encoding', 'BASE64')
        m.add_header('Content-Disposition', 'attachment; filename="{}"'.format(v))

        f = open(v, 'rb')
        r = f.read()
        f.close()
        r = b64encode(r)
        m.set_payload(str(r))

        return m


    def add(self, *args, related_id=None, wrapper=None):
        m_id = uuid.uuid4()
        m = Message()
        m.add_header('X-Piknik-Msg-Id', str(m_id))
        m.add_header('Date', formatdate(time.time()))
        if related_id != None:
            m.add_header('In-Reply-To', related_id)
        m.set_payload(None)
        m.set_type('multipart/mixed')
        m.set_boundary(str(uuid.uuid4()))
        for a in args:
            p = a[:2]
            v = a[2:]
            r = None
            if p == 'f:':
                r = self.from_file(v)
            elif p == 's:':
                r = self.from_text(v)
            m.attach(r)
        if wrapper:
            m = wrapper(m)
        self.__m.attach(m)


    def as_string(self, **kwargs):
        return self.__m.as_string(**kwargs)


    def as_bytes(self, **kwargs):
        return self.__m.as_bytes(**kwargs)


    def __str__(self):
        return self.as_string()

# standard imports
import logging
import uuid

#from email.message import EmailMessage as Message
from email.message import Message
from email import message_from_string
from email.policy import Compat32


logg = logging.getLogger(__name__)


class IssueMessage(Message):

    def __init__(self, issue):
        super(IssueMessage, self).__init__()
        self.add_header('Subject', issue.title)
        self.add_header('X-Piknik-Id', issue.id)
        self.set_payload(None)
        self.set_type('multipart/mixed')
        self.set_boundary(str(uuid.uuid4()))


    @staticmethod
    def from_string(self, v):
        return message_from_string(v)


    def add_text(self, m, v):
        p = Message()
        p.add_header('Content-Transfer-Encoding', 'QUOTED-PRINTABLE')
        p.set_charset('UTF-8')
        p.set_payload(str(v))
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
        self.attach(m)

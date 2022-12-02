# standard imports
import logging

# external imports
from mimeparse import parse_mime_type

# local imports
from .base import Renderer as BaseRenderer
from .base import stream_accumulator

logg = logging.getLogger(__name__)


class Renderer(BaseRenderer):

    def __init__(self, basket, dump_dir=None, accumulator=stream_accumulator, **kwargs):
        super(Renderer, self).__init__(basket, accumulator=accumulator, **kwargs)
        self.dump_dir = dump_dir


    def apply_issue(self, state, issue, tags, accumulator=None):
        s = """title: {}
tags: {}
id: {}

""".format(
        issue.id,
        issue.title,
        ', '.join(tags),
            )
        self.add(s, accumulator=accumulator)

        assigned = issue.get_assigned()

        if len(assigned) == 0:
            self.add('(not assigned)\n', accumulator=accumulator)

        else:
            self.add('assigned to:\n', accumulator=accumulator)
            owner = issue.owner()
            for v in assigned:
                o = v[0]
                s = o.id()
                if o == owner:
                    s += ' (owner)'
                s = '\t' + str(s) + '\n'
                self.add(s, accumulator=accumulator)

        super(Renderer, self).apply_issue(state, issue, tags, accumulator=accumulator)


    def apply_message(self, state, issue, tags, envelope, message, message_id, message_date, accumulator=None):
        s = '\nmessage {} from {} {} - {}\n\n'.format(
                message_date,
                envelope.sender,
                envelope.valid,
                message_id,
                )
        self.add(s, accumulator=accumulator)


    def apply_message_part(self, state, issue, envelope, message, message_id, message_date, accumulator=None):
        m = parse_mime_type(message.get_content_type())
        filename = message.get_filename()

        v = ''
        if filename == None:
            if m[0] == 'text':
                if m[1] == 'plain':
                    v = message.get_payload()
                    if message.get('Content-Transfer-Encoding') == 'BASE64':
                        v = b64decode(v).decode()
                else:
                    v = '[rich text]'
        else:
            if self.dump_dir != None:
                v = message.get_payload()
                if message.get('Content-Transfer-Encoding') == 'BASE64':
                    v = b64decode(v).decode()
                filename = to_suffixed_file(self.dump_dir, filename, v)
            sz = message.get('Content-Length')
            if sz == None:
                sz = 'unknown'
            v = '[file: {}, type {}/{}, size: {}]'.format(filename, m[0], m[1], sz)

        s = '\n\t' + v + '\n'
        self.add(s, accumulator=accumulator)

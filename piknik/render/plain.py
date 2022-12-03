# standard imports
import logging
import tempfile
import os

# external imports
from mimeparse import parse_mime_type

# local imports
from .base import Renderer as BaseRenderer
from .base import stream_accumulator

logg = logging.getLogger(__name__)

def to_suffixed_file(d, s, data):
    (v, ext) = os.path.splitext(s)
    r = tempfile.mkstemp(suffix=ext, dir=d)

    f = os.fdopen(r[0], 'wb')
    try:
        f.write(data)
    except TypeError:
        f.write(data.encode('utf-8'))
    f.close()

    return r[1]


class Renderer(BaseRenderer):

    def __init__(self, basket, dump_dir=None, accumulator=stream_accumulator, **kwargs):
        super(Renderer, self).__init__(basket, accumulator=accumulator, **kwargs)
        self.dump_dir = dump_dir


    def apply_issue(self, state, issue, tags, accumulator=None):
        if self.render_mode == 0:
            return self.apply_issue_standalone(state, issue, tags, accumulator=accumulator)

        s = '{}\t{}\t{}\n'.format(
                issue.title,
                ','.join(tags),
                issue.id,
                )
        self.add(s, accumulator=accumulator)
        super(Renderer, self).apply_issue(state, issue, tags, accumulator=accumulator)


    def apply_issue_standalone(self, state, issue, tags, accumulator=None):
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
        return s


    def apply_message_part(self, state, issue, tags, envelope, message, message_date, message_content, accumulator=None):
        if message_content['filename'] != None:
            if self.dump_dir != None:
                filename = to_suffixed_file(self.dump_dir, message_content['filename'], message_content['contents'])
            sz = message_content['size']
            if sz == -1:
                sz = 'unknown'
            v = '[file: {}, type {}/{}, size: {}]'.format(
                    message_content['filename'],
                    message_content['type'][0],
                    message_content['type'][1],
                    sz,
                    )
        else:
            v = message_content['contents']

        s = '\n\t' + v + '\n'
        return s


    def apply_state(self, state, accumulator=None):
        s = '[' + state + ']\n'
        self.add(s, accumulator=accumulator) 
        super(Renderer, self).apply_state(state, accumulator=accumulator)


    def apply_state_post(self, state, accumulator=None):
        self.add('\n', accumulator=accumulator)

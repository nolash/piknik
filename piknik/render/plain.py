# standard imports
import sys

# external imports
from mimeparse import parse_mime_type

# local imports
from .base import Renderer as BaseRenderer


class Renderer(BaseRenderer):

    def apply_issue(self, state, issue, tags, w=sys.stdout):
        w.write("""id: {}
title: {}
tags: {}

""".format(
        issue.id,
        issue.title,
        ', '.join(tags),
            )
          )

        assigned = issue.get_assigned()

        if len(assigned) == 0:
            w.write('(not assigned)\n')
            return

        w.write('assigned to:\n')
        owner = issue.owner()
        for v in assigned:
            o = v[0]
            s = o.id()
            if o == owner:
                s += ' (owner)'
            w.write('\t' + str(s))


    def apply_message(self, state, issue, tags, message, w=sys.stdout):
        pass


    def apply_message_part(self, state, issue, envelope, message, message_date, message_id, dump_dir=None, w=sys.stdout):
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
            if dump_dir != None:
                v = message.get_payload()
                if message.get('Content-Transfer-Encoding') == 'BASE64':
                    v = b64decode(v).decode()
                filename = to_suffixed_file(dump_dir, filename, v)
            sz = message.get('Content-Length')
            if sz == None:
                sz = 'unknown'
            v = '[file: {}, type {}/{}, size: {}]'.format(filename, m[0], m[1], sz)

        w.write(v)

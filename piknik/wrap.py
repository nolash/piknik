# standard imports
import logging

# external imports
from mimeparse import parse_mime_type

logg = logging.getLogger(__name__)


class Wrapper:

    def __init__(self):
        self.content_buffer = {}


    def add(self, message_id, message):
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
            sz = -1
        else:
            sz = int(sz)

        self.content_buffer[message_id] = {
                'type': m,
                'filename': filename,
                'size': sz,
                'contents': v,
                }

        logg.debug('buffered content {}'.format(self.content_buffer[message_id]))


    def pop(self, message_id):
        r = self.content_buffer[message_id]
        del self.content_buffer[message_id]
        return r

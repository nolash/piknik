# standard imports
import os
import sys
import argparse
import logging
import tempfile
from base64 import b64decode
from email.utils import parsedate_to_datetime

# external imports
from mimeparse import parse_mime_type

# local imports
from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory
from piknik.crypto import PGPSigner

#logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-f', '--files', dest='f', action='store_true', help='Save attachments to filesystem')
argp.add_argument('-o', '--files-dir', dest='files_dir', type=str, default='.', help='Directory to output saved files to')
argp.add_argument('-r', '--renderer', type=str, default='default', help='Renderer module for output')
argp.add_argument('issue_id', type=str, help='Issue id to show')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory)


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


# TODO can implement as email parser api instead?
class PGPWrapper(PGPSigner):

    def __init__(self, home_dir=None):
        super(PGPWrapper, self).__init__(home_dir=home_dir)
        self.message_date = None
        self.message = []
        self.message_id = None
        self.sender = None
        self.valid = False


    def render_message(self, envelope, messages, message_id, w=sys.stdout, dump_dir=None):
        r = ''
        for message in messages:
            m = parse_mime_type(message.get_content_type())

            v = ''
            if m[0] == 'text':
                if m[1] == 'plain':
                    v = message.get_payload()
                    if message.get('Content-Transfer-Encoding') == 'BASE64':
                        v = b64decode(v).decode()
                else:
                    v = '[rich text]'
            else:
                filename = message.get_filename()
                if dump_dir != None:
                    v = message.get_payload()
                    if message.get('Content-Transfer-Encoding') == 'BASE64':
                        v = b64decode(v).decode()
                    filename = to_suffixed_file(dump_dir, filename, v)
                sz = message.get('Content-Length')
                if sz == None:
                    sz = 'unknown'
                v = '[file: ' + filename + ', size: ' + sz + ']'

            valid = '[++]'
            if not self.valid:
                valid = '[!!]'
            r += '\n\t' + v + '\n'
        w.write('\nmessage {} from {} {} - {}\n\t{}\n'.format(self.message_date, self.sender, valid, message_id, r))


    def envelope_callback(self, envelope, envelope_type):
        envelope = super(PGPWrapper, self).envelope_callback(envelope, envelope_type)
        envelope.valid = False
        return envelope


    def message_callback(self, envelope, message, message_id):
        (envelope, message) = super(PGPWrapper, self).message_callback(envelope, message, message_id)

        if envelope != None and not envelope.resolved:
            self.sender = envelope.sender
            self.valid = envelope.valid
            self.resolved = True

        if message_id == None:
            return

        if message.get('X-Piknik-Msg-Id') == None:
            if message.get('Content-Type') == 'application/pgp-signature':
                dump_dir = None
                if arg.f:
                    dump_dir = arg.files_dir
                self.render_message(envelope, self.message, self.message_id, dump_dir=dump_dir)
                self.message = []
                self.message_id = None
            else:
                self.message.append(message)
        else:
            d = message.get('Date')
            self.message_date = parsedate_to_datetime(d)
            self.message_id = message_id

gpg_home = os.environ.get('GPGHOME')
verifier = PGPWrapper(home_dir=gpg_home)


def render_default(b, o, t):
    print("""id: {}
title: {}
tags: {}
""".format(
        o.id,
        o.title,
        ', '.join(t),
            )
          )

    assigned = o.get_assigned()

    if len(assigned) == 0:
        print('(not assigned)')
        return

    print('assigned to:')
    owner = o.owner()
    for v in assigned:
        o = v[0]
        s = o.id()
        if o == owner:
            s += ' (owner)'
        print('\t' + str(s))

    m = basket.get_msg(arg.issue_id, envelope_callback=verifier.envelope_callback, message_callback=verifier.message_callback)


def main():
    o = basket.get(arg.issue_id)
    t = basket.tags(arg.issue_id)

    globals()['render_' + arg.renderer](basket, o, t)
    

if __name__ == '__main__':
    main()

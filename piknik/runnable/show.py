# standard imports
import sys
import argparse
import logging
from base64 import b64decode
from email.utils import parsedate_to_datetime

# external imports
from mimeparse import parse_mime_type

# local imports
from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory
from piknik.crypto import PGPSigner


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-r', '--renderer', type=str, default='default', help='Renderer module for output')
argp.add_argument('issue_id', type=str, help='Issue id to show')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory)


# TODO can implement as email parser api instead?
class PGPWrapper(PGPSigner):

    def __init__(self, home_dir=None):
        super(PGPWrapper, self).__init__(home_dir=home_dir)
        self.message_date = None


    def render_message(self, message, message_id):
        r = None
        m = parse_mime_type(message.get_content_type())
        print('content {}'.format(m))

        if m[0] == 'text':
            if m[1] == 'plain':
                r = message.get_payload()
                if message.get('Content-Transfer-Encoding') == 'BASE64':
                    r = b64decode(r).decode()
            else:
                r = '[rich text]'
        else:
            sz = message.get('Content-Length')
            if sz == None:
                sz = 'unknown'
            r = '[file: ' + message.get_filename() + ', size: ' + sz + ']'

        print("message {} - {}\n\t{}\n".format(self.message_date, message_id, r))


    def message_callback(self, envelope, message, message_id):
        super(PGPWrapper, self).message_callback(envelope, message, message_id)

        if message_id == None:
            return

        if message.get('X-Piknik-Msg-Id') == None:
            if message.get('Content-Type') == 'application/pgp-signature':
                return
            self.render_message(message, message_id)
        else:
            d = message.get('Date')
            self.message_date = parsedate_to_datetime(d)

verifier = PGPWrapper()


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

# standard imports
import io
import os
import sys
import argparse
import logging
import tempfile
from base64 import b64decode
from email.utils import parsedate_to_datetime

# local imports
from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory
from piknik.crypto import PGPSigner
from piknik.render.plain import Renderer

#logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-f', '--files', dest='f', action='store_true', help='Save attachments to filesystem')
argp.add_argument('-o', '--files-dir', dest='files_dir', type=str, default='.', help='Directory to output saved files to')
argp.add_argument('-r', '--renderer', type=str, default='default', help='Renderer module for output')
argp.add_argument('--reverse', action='store_true', help='Sort comments by oldest first')
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

    def __init__(self, renderer, state, issue, home_dir=None):
        super(PGPWrapper, self).__init__(home_dir=home_dir)
        self.message_date = None
        self.messages = []
        self.part = []
        self.message_id = None
        self.sender = None
        self.valid = False
        self.renderer = renderer
        self.state = state
        self.issue = issue


    def render_message(self, envelope, messages, message_date, message_id, dump_dir=None, w=sys.stdout):
        r = ''
        w.write('\n')
        for message in messages:
            ww = io.StringIO()
            self.renderer.apply_message_part(self.state, self.issue, envelope, message, message_date, message_id, dump_dir=dump_dir, w=ww)
            valid = '[++]'
            if not self.valid:
                valid = '[!!]'
            ww.seek(0)
            r += '\n\t' + ww.read() + '\n'
        w.write('\nmessage {} from {} {} - {}\n\t{}\n'.format(message_date, self.sender, valid, message_id, r))


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

        messages = []
        if message.get('X-Piknik-Msg-Id') == None:
            if message.get('Content-Type') == 'application/pgp-signature':
                
                #self.render_message(envelope, self.message, self.message_id, dump_dir=dump_dir)
                self.messages.append((envelope, self.part, self.message_date, self.message_id,))
                self.part = []
                self.message_id = None
                self.message_date = None
            else:
                self.part.append(message)
        else:
            d = message.get('Date')
            self.message_date = parsedate_to_datetime(d)
            self.message_id = message_id


    def post_callback(self, messages_id):
        dump_dir = None
        if arg.f:
            dump_dir = arg.files_dir
        rg = None
        if arg.reverse:
            rg = range(0, len(self.messages))
        else:
            rg = range(len(self.messages)-1, -1, -1)
        for i in rg:
            v = self.messages[i]
            self.render_message(v[0], v[1], v[2], v[3], dump_dir=dump_dir)


gpg_home = os.environ.get('GPGHOME')


def render(renderer, basket, state, issue, tags):
    renderer.apply_issue(state, arg.issue_id, issue, tags)
    verifier = PGPWrapper(renderer, state, issue, home_dir=gpg_home)
    m = basket.get_msg(
            arg.issue_id,
            envelope_callback=verifier.envelope_callback,
            message_callback=verifier.message_callback,
            post_callback=verifier.post_callback,
            )


def main():
    issue = basket.get(arg.issue_id)
    tags = basket.tags(arg.issue_id)
    state = basket.get_state(arg.issue_id)

    #globals()['render_' + arg.renderer](basket, state, issue, tags)
    import piknik.render.plain
    renderer = piknik.render.plain.Renderer()
    render(renderer, basket, state, issue, tags)
    

if __name__ == '__main__':
    main()

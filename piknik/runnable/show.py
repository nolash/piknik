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

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-f', '--files', dest='f', action='store_true', help='Save attachments to filesystem')
argp.add_argument('-o', '--files-dir', dest='files_dir', type=str, default='.', help='Directory to output saved files to')
argp.add_argument('-r', '--renderer', type=str, default='default', help='Renderer module for output')
argp.add_argument('-s', '--state', type=str, action='append', default=[], help='Limit results to state(s)')
argp.add_argument('--show-finished', dest='show_finished', action='store_true', help='Include finished issues')
argp.add_argument('--reverse', action='store_true', help='Sort comments by oldest first')
argp.add_argument('issue_id', type=str, nargs='?', default=None, help='Issue id to show')
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
        #super(PGPWrapper, self).__init__(home_dir=home_dir)
        super(PGPWrapper, self).__init__(home_dir=home_dir, skip_verify=True)
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
        for message in messages:
            self.renderer.apply_message_part(self.state, self.issue, envelope, message, self.sender, message_date, message_id, self.valid, dump_dir=dump_dir, w=w)
        #valid = '[++]'
        #if not self.valid:
        #    valid = '[!!]'
        self.renderer.apply_message_post(self.state, self.issue, envelope, message, self.sender, message_date, message_id, self.valid, w=w)


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


def render(renderer, basket, issue, tags):
    renderer.apply_begin()
    render_issue(renderer, basket, issue, tags)
    renderer.apply_state_post(state)
    renderer.apply_end()


def render_issue(renderer, basket, issue, tags):
    state = basket.get_state(issue.id)
    renderer.apply_issue(state, issue, tags)
    verifier = PGPWrapper(renderer, state, issue, home_dir=gpg_home)
    m = basket.get_msg(
            issue.id,
            envelope_callback=verifier.envelope_callback,
            message_callback=verifier.message_callback,
            post_callback=verifier.post_callback,
        )
    renderer.apply_issue_post(state, issue, tags)


def render_states(renderer, basket, states):
    renderer.apply_begin()

    for k in basket.states():
        if k == 'FINISHED' and not arg.show_finished:
            continue

        renderer.apply_state(k)

        for issue_id in states[k]:
            if k != 'BLOCKED' and issue_id in states['BLOCKED']:
                continue
            issue = basket.get(issue_id)
            tags = basket.tags(issue_id)
            #renderer.apply_issue(k, issue, tags)
            #renderer.apply_issue_post(k, issue, tags)
            render_issue(renderer, basket, issue, tags)

        renderer.apply_state_post(k)

    renderer.apply_end()


def process_states(renderer, basket):
    results = {}
    states = []
    for s in arg.state:
        states.append(s.upper())

    l = len(states)
    for s in basket.states():
        
        if results.get(s) == None:
            results[s] = []

        if l == 0 or s in states:
            for v in basket.list(category=s):
               results[s].append(v)

    render_states(renderer, basket, results)


def main():
    if arg.issue_id == None:
        import piknik.render.html
        renderer = piknik.render.html.Renderer()
        return process_states(renderer, basket)

    import piknik.render.html
    renderer = piknik.render.html.Renderer()

    issue = basket.get(arg.issue_id)
    tags = basket.tags(arg.issue_id)

    #globals()['render_' + arg.renderer](basket, state, issue, tags)
    render(renderer, basket, issue, tags)
    

if __name__ == '__main__':
    main()

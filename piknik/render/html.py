# standard imports
import sys
import os

# external imports
import dominate
from dominate.tags import div, p, a, meta, ul, ol, li, h1, h2, link
from mimeparse import parse_mime_type

# local imports
from .base import Renderer as BaseRenderer


class Renderer(BaseRenderer):

    def __init__(self, outdir='/home/lash/tmp'):
        super(Renderer, self).__init__()
        self.issue_buf = []
        self.state_buf = []
        self.message_buf = []
        self.outdir = outdir


    def apply_state_post(self, state, w=sys.stdout):
        r = div(_id='state_' + state)
        r.add(h2(state))
        r_l = ul(_class='state_listing')
        while True:
            try:
                v = self.issue_buf.pop(0)
                r_l.add(v)
            except IndexError:
                break
        r.add(r_l)
        self.state_buf.append(r)


    def apply_issue(self, state, issue, tags, w=sys.stdout):
        v = li(a(issue.title, href=issue.id + '.html'))
        r_l = ol()
        while True:
            try:
                v = self.message_buf.pop(0)
                r_l.add(v)
            except IndexError:
                break
        v.add(r_l)
        self.issue_buf.append(v)


    def apply_issue_post(self, state, issue, tags, w=None):
        close = False
        if w == None:
            fp = os.path.join(self.outdir, issue.id + '.html')
            w = open(fp, 'w')
            close = True
        r = dominate.document(title='issue: {} ({})'.format(issue.title, issue.id))
        r.add(h1(issue.title))
        w.write(r.render())
       
        if close:
            w.close()


    def apply_message_post(self, state, issue, tags, message, message_from, message_date, message_id, message_valid, w=sys.stdout):
        #r = ol()
        #w.write(self.message_buf.render())
        pass


    def apply_message_part(self, state, issue, envelope, message, message_from, message_date, message_id, message_valid, dump_dir=None, w=sys.stdout):
        m = parse_mime_type(message.get_content_type())
        filename = message.get_filename()

        if filename == None:
            v = message.get_payload()
            if message.get('Content-Transfer-Encoding') == 'BASE64':
                v = b64decode(v).decode()
            self.message_buf.append(p(v))


    def apply_end(self, w=sys.stdout):
        r = dominate.document(title='issues for ...')
        r.head.add(meta(name='generator', content='piknik'))
        r.head.add(link(rel='stylesheet', href='style.css'))
        buf = None
        if len(self.state_buf) > 0:
            buf = self.state_buf
        else:
            buf = self.issue_buf
        while True:
            try:
                v = buf.pop(0)
                r.add(v)
            except IndexError:
                break
        w.write(r.render())

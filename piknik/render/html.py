import sys
import os

import dominate
from dominate.tags import div, p, a, meta, ul, li, h1, h2, link

from .base import Renderer as BaseRenderer


class Renderer(BaseRenderer):

    def __init__(self, outdir='/home/lash/tmp'):
        super(Renderer, self).__init__()
        self.issue_buf = []
        self.state_buf = []
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


    def apply_issue(self, state, issue_id, issue, tags, w=sys.stdout):
        v = li(a(issue.title, href=issue_id + '.html'))
        self.issue_buf.append(v)


    def apply_message(self, state, issue_id, issue, tags, message, w=None):



    def apply_issue_post(self, state, issue_id, issue, tags, w=None):
        close = False
        if w == None:
            fp = os.path.join(self.outdir, issue_id + '.html')
            w = open(fp, 'w')
            close = True
        r = dominate.document(title='issue: {} ({})'.format(issue.title, issue_id))
        r.add(h1(issue.title))
        w.write(r.render())
       
        if close:
            w.close()


    def apply_end(self, w=sys.stdout):
        r = dominate.document(title='issues for ...')
        r.head.add(meta(name='generator', content='piknik'))
        r.head.add(link(rel='stylesheet', href='style.css'))
        while True:
            try:
                v = self.state_buf.pop(0)
                r.add(v)
            except IndexError:
                break
        w.write(r.render())

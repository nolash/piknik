# standard imports
import sys
import os
import logging

# external imports
import dominate
from dominate.tags import div, p, a, meta, ul, ol, li, h1, h2, link, dl, dd, dt, img
from mimeparse import parse_mime_type

# local imports
from .base import Renderer as BaseRenderer

logg = logging.getLogger(__name__)


class Accumulator:

    def __init__(self):
        self.doc = None
        self.category = ul(_id='state_list')
        self.issue = None
        #self.message = None


    def add(self, v, w=sys.stdout):
        if len(v) == 0:
            self.doc.add(self.category)
            w.write(self.doc.render())
            return

        v_id = getattr(v, 'id', '')
        if len(v_id) > 1:
            if v_id[:2] == 's_':
                if self.issue != None:
                    self.category.add(self.issue)
                self.category.add(v)
                self.issue = ul(_id='issue_list_' + v_id[2:])
            elif v_id[:2] == 'i_':
                logg.debug('issue now')
                self.issue.add(v)
            elif v_id[:4] == 'd_i_':
                self.category = v
        else:
            self.doc = v


class Renderer(BaseRenderer):

    def __init__(self, basket, accumulator=None, wrapper=None, outdir='/tmp'):
        if accumulator == None:
            accumulator = Accumulator().add
        super(Renderer, self).__init__(basket, accumulator=accumulator, wrapper=wrapper)
        #self.issue_buf = []
        #self.state_buf = []
        #self.message_buf = []
        self.outdir = outdir
        self.last_message_id = None
        self.render_mode = 0
        self.msg_idx = 0


    def apply_state(self, state, accumulator=None):
        self.render_mode = 1
        v = div(_id='s_' + state.lower())
        v.add(h2(state))
        self.add(v)
        super(Renderer, self).apply_state(state, accumulator=accumulator)


    def apply_issue(self, state, issue, tags, accumulator=None):
        if self.render_mode == 1:
            s = issue.title
            u = a(s, href=issue.id + '.html')
            return li(u, _id='i_' + issue.id)
        

        r = div(_id='d_i_' + issue.id)

        s = h1(issue.title)
        r.add(s)
        
        s = dd()
        s.add(dt('issue id'))
        s.add(dd(issue.id))

        s.add(dt('tags'))
        r_r = ul()
        for v in tags:
            if v == '(UNTAGGED)':
                continue
            r_r.add(li(v))

        assigned = issue.get_assigned()
        s.add(dd(r_r))
    
        s.add(dt('assigned to'))
        if len(assigned) == 0:
            s.add(dd('not assigned'))
        else:
            owner = issue.owner()
            r_r = ul()
            for v in assigned:
                o = v[0]
                s = o.id()
                if o == owner:
                    s += ' (owner)'
                r_r.add(li(s))
            s.add(dd(r_r))

        r.add(s)

        self.add(r)

        super(Renderer, self).apply_issue(state, issue, tags, accumulator=accumulator)

#    def apply_state_post(self, state, w=sys.stdout):
#        r = div(_id='state_' + state)
#        r.add(h2(state))
#        r_l = ul(_class='state_listing')
#        while True:
#            try:
#                v = self.issue_buf.pop(0)
#                r_l.add(v)
#            except IndexError:
#                break
#        r.add(r_l)
#        self.state_buf.append(r)
#
#
#    def apply_issue(self, state, issue, tags, w=sys.stdout):
#        v = li(a(issue.title, href=issue.id + '.html'))
#        r_l = ol()
#        while True:
#            try:
#                v = self.message_buf.pop(0)
#                logg.debug('msgd {} {}'.format(issue.id, str(v)))
#                r_l.add(v)
#            except IndexError:
#                break
#        v.add(r_l)
#        self.issue_buf.append(v)
#
#
#    def apply_issue_post(self, state, issue, tags, w=None):
#        close = False
#        if w == None:
#            fp = os.path.join(self.outdir, issue.id + '.html')
#            w = open(fp, 'w')
#            close = True
#        r = dominate.document(title='issue: {} ({})'.format(issue.title, issue.id))
#        r.add(h1(issue.title))
#
#        r_l = dl()
#        r_l.add(dt('id'))
#        r_l.add(dd(issue.id))
#
#        r_l.add(dt('tags'))
#        r_r = ul()
#        for v in tags:
#            if v == '(UNTAGGED)':
#                continue
#            r_r.add(li(v))
#
#        assigned = issue.get_assigned()
#        r_l.add(dd(r_r))
#    
#        r_l.add(dt('assigned to'))
#        if len(assigned) == 0:
#            r_l.add(dd('not assigned'))
#        else:
#            owner = issue.owner()
#            r_r = ul()
#            for v in assigned:
#                o = v[0]
#                s = o.id()
#                if o == owner:
#                    s += ' (owner)'
#                r_r.add(li(s))
#            r_l.add(dd(r_r))
#
#        r.add(r_l)
#
#        for i, v in enumerate(self.message_buf):
#            r.add(p(v)) w.write(r.render())
#
#        if close:
#            w.close()
#
#
#    def apply_message_post(self, state, issue, tags, message, message_from, message_date, message_id, message_valid, w=sys.stdout):
#        #r = ol()
#        #w.write(self.message_buf.render())
#        self.msg_idx = 0
#        pass
#
#
#    def apply_message_part(self, state, issue, envelope, message, message_from, message_date, message_id, message_valid, dump_dir=None, w=sys.stdout):
#        m = parse_mime_type(message.get_content_type())
#        filename = message.get_filename()
#
#        if message_id != self.last_message_id:
#            s = '--- {} @ {}'.format(message_from, message_date)
#            self.message_buf.append(div(s, _id=issue.id))
#            self.last_message_id = message_id
#
#        r = div(_id=issue.id + '.' + message_id + '.' + str(self.msg_idx))
#        self.msg_idx += 1
#        if filename == None:
#            v = message.get_payload()
#            if message.get('Content-Transfer-Encoding') == 'BASE64':
#                v = b64decode(v).decode()
#            r.add(p(v))
#        #w.write(r.render())


    def apply_begin(self, accumulator=None):
        r = dominate.document(title='issues for ...')
        r.head.add(meta(name='generator', content='piknik'))
        r.head.add(link(rel='stylesheet', href='style.css'))
        self.add(r)


    def apply_end(self, accumulator=None):
        return ()


#    def apply_end(self, w=sys.stdout):
#        r = dominate.document(title='issues for ...')
#        r.head.add(meta(name='generator', content='piknik'))
#        r.head.add(link(rel='stylesheet', href='style.css'))
#        buf = None
#        if len(self.state_buf) > 0:
#            buf = self.state_buf
#        else:
#            buf = self.issue_buf
#        while True:
#            try:
#                v = buf.pop(0)
#                r.add(v)
#            except IndexError:
#                break
#        w.write(r.render())

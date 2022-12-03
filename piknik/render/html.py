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

    def __init__(self, w=sys.stdout):
        self.doc = None
        self.category = ul(_id='state_list')
        self.issue = None
        self.msg = None
        self.w = w


    def add(self, v, w=None):
        if w == None:
            w = self.w
        if len(v) == 0:
            self.doc.add(self.category)
            if self.msg != None:
                self.doc.add(self.msg)
            w.write(self.doc.render())
            return

        v_id = getattr(v, 'id', '')
        logg.debug('add id {}'.format(v_id))
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
                self.msg = ol(_id='message_list')
            elif v_id[:2] == 'm_':
                self.msg.add(li(v))
            elif v_id[:4] == 'd_m_':
                self.msg.add(v)
        else:
            self.doc = v


class Renderer(BaseRenderer):

    def __init__(self, basket, accumulator=None, wrapper=None, outdir=None):
        if accumulator == None:
            accumulator = Accumulator().add
        super(Renderer, self).__init__(basket, accumulator=accumulator, wrapper=wrapper)
        self.outdir = outdir


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

    
    def apply_message(self, state, issue, tags, envelope, message, message_id, message_date, accumulator=None):
        r = div(_id='m_' + message_id)

        s = dd()
        s.add(dt('Date'))
        s.add(dd(str(message_date)))

        v = envelope.sender
        if v == None:
            v = '(unknown)'
        else:
            if envelope.valid:
                v += ' (!!)'
            else:
                v += ' (??)'
        s.add(dt('By'))
        s.add(dd(v))
        r.add(s)

        self.add(r)
       

    def apply_message_part(self, state, issue, tags, envelope, message, message_date, message_content, accumulator=None):
        r = None
        if message_content['filename'] != None:
            s = 'data:{}/{};base64,{}'.format(
                    message_content['type'][0],
                    message_content['type'][1],
                    message_content['contents'],
                    )
            r = None
            if message_content['type'][0] == 'image':
                r = img(src=s)
            else:
                v = os.path.basename(message_content['filename'])
                r = a(v, href=s)
            
        else:
            r = message_content['contents']

        m_id = 'd_m_{}_{}'.format(
                    message_content['id'],
                    message_content['idx'],
                    )

        return div(r, _id=m_id)


    def apply_begin(self, accumulator=None):
        r = dominate.document(title='issues for ...')
        r.head.add(meta(name='generator', content='piknik'))
        r.head.add(link(rel='stylesheet', href='style.css'))
        self.add(r)


    def apply_end(self, accumulator=None):
        self.add(())
        return None

# standard imports
import logging
import sys

# local imports
from piknik.msg import MessageEnvelope

logg = logging.getLogger(__name__)


def stream_accumulator(v, w=sys.stdout):
    w.write(v)


class Renderer:

    def __init__(self, basket, accumulator=None, envelope_callback=None, message_callback=None):
        self.b = basket
        #self.e = None
        self.a = accumulator
        self.message_callback = message_callback
        self.envelope_callback = envelope_callback


    def add(self, v, accumulator=None):
        if accumulator == None:
            accumulator = self.a
        if accumulator != None:
            if v != None:
                accumulator(v)


    def apply_envelope_pre(self, state, issue, tags, envelope, accumulator=None):
        pass


    def apply_envelope_post(self, state, issue, tags, envelope, accumulator=None):
        pass

    
    def apply_envelope(self, state, issue, tags, envelope, accumulator=None):
        pass


    def apply_message_pre(self, state, issue, tags, envelope, message, message_id, message_date, accumulator=None):
        pass


    def apply_message_post(self, state, issue, tags, envelope, message, message_id, message_date, accumulator=None):
        pass

    
    def apply_message(self, state, issue, tags, envelope, message, message_id, message_date, accumulator=None):
        pass


    def apply_issue_pre(self, state, issue, tags, accumulator=None):
        pass


    def apply_issue_post(self, state, issue, tags, accumulator=None):
        pass


    def apply_issue(self, state, issue, tags, accumulator=None):

        def envelope_callback(envelope, envelope_type):
            if self.envelope_callback != None:
                envelope = self.envelope_callback(envelope, envelope_type)
            else:
                envelope = MessageEnvelope(envelope)
            r = self.apply_envelope_pre(state, issue, tags, envelope, accumulator=accumulator)
            self.add(r)
            r = self.apply_envelope(state, issue, tags, envelope, accumulator=accumulator)
            self.add(r)
            r = self.apply_envelope_post(state, issue, tags, envelope, accumulator=accumulator)
            self.add(r)
            return envelope

        def message_callback(envelope, message, message_id, message_date):
            if self.message_callback != None:
                (envelope, message) = self.message_callback(envelope, message, message_id, message_date)
            r = self.apply_message_pre(state, issue, tags, envelope, message, message_id, message_date, accumulator=accumulator)
            self.add(r)
            r = self.apply_message(state, issue, tags, envelope, message, message_id, message_date, accumulator=accumulator)
            self.add(r)
            r = self.apply_message_post(state, issue, tags, envelope, message, message_id, message_date, accumulator=accumulator)
            self.add(r)
            return (envelope, message,)

        #for msg in self.b.get_msg(issue.id, envelope_callback=envelope_callback, message_callback=message_callback):
        logg.debug('in msg')
        self.b.get_msg(issue.id, envelope_callback=envelope_callback, message_callback=message_callback)


    def apply_state_pre(self, state, accumulator=None):
        pass


    def apply_state_post(self, state, accumulator=None):
        pass


    def apply_state(self, state, accumulator=None):
        for issue_id in self.b.list(category=state):
            issue = self.b.get(issue_id)
            tags = self.b.tags(issue_id=issue_id)
            r = self.apply_issue_pre(state, issue, tags)
            self.add(r)
            r = self.apply_issue(state, issue, tags)
            self.add(r)
            r = self.apply_issue_post(state, issue, tags)
            self.add(r)


    def apply_begin(self, accumulator=None):
        pass


    def apply_end(self, accumulator=None):
        pass


    def apply(self, accumulator=None):
        r = self.apply_begin()
        self.add(r)

        for state in self.b.states():
            r = self.apply_state_pre(state)
            self.add(r)
            r = self.apply_state(state)
            self.add(r)
            r = self.apply_state_post(state)
            self.add(r)

        r = self.apply_end()
        self.add(r)

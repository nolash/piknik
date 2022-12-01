#import sys
import logging

logg = logging.getLogger(__name__)


class Renderer:

    def __init__(self, basket, accumulator=None):
        self.b = basket
        #self.e = None
        self.a = accumulator


    def __add(self, v):
        if self.a != None:
            if v != None:
                self.a(v)


    def apply_envelope_pre(self, state, issue, tags, envelope, accumulator=None):
        pass


    def apply_envelope_post(self, state, issue, tags, envelope, accumulator=None):
        pass

    
    def apply_envelope(self, state, issue, tags, envelope, accumulator=None):
        pass


    def apply_message_pre(self, state, issue, tags, envelope, message, accumulator=None):
        pass


    def apply_message_post(self, state, issue, tags, envelope, message, accumulator=None):
        pass

    
    def apply_message(self, state, issue, tags, envelope, message, accumulator=None):
        pass


    def apply_issue_pre(self, state, issue, tags, accumulator=None):
        pass


    def apply_issue_post(self, state, issue, tags, accumulator=None):
        pass


    def apply_issue(self, state, issue, tags, accumulator=None):

        def envelope_callback(envelope, envelope_type):
            r = self.apply_envelope_pre(state, issue, tags, envelope, accumulator=accumulator)
            self.__add(r)
            r = self.apply_envelope(state, issue, tags, envelope, accumulator=accumulator)
            self.__add(r)
            r = self.apply_envelope_post(state, issue, tags, envelope, accumulator=accumulator)
            self.__add(r)

        def message_callback(envelope, message, message_id):
            r = self.apply_message_pre(state, issue, tags, envelope, message, accumulator=accumulator)
            self.__add(r)
            r = self.apply_message(state, issue, tags, envelope, message, accumulator=accumulator)
            self.__add(r)
            r = self.apply_message_post(state, issue, tags, envelope, message, accumulator=accumulator)
            self.__add(r)

        #for msg in self.b.get_msg(issue.id, envelope_callback=envelope_callback, message_callback=message_callback):
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
            self.__add(r)
            r = self.apply_issue(state, issue, tags)
            self.__add(r)
            r = self.apply_issue_post(state, issue, tags)
            self.__add(r)


    def apply_begin(self, accumulator=None):
        pass


    def apply_end(self, accumulator=None):
        pass


    def apply(self, accumulator=None):
        r = self.apply_begin()
        self.__add(r)

        for state in self.b.states():
            r = self.apply_state_pre(state)
            self.__add(r)
            r = self.apply_state(state)
            self.__add(r)
            r = self.apply_state_post(state)
            self.__add(r)

        r = self.apply_end()
        self.__add(r)

# standard imports
import logging

# external imports
import shep

# local imports
from .error import DeadIssue
from .issue import Issue
from .msg import IssueMessage

logg = logging.getLogger(__name__)


class Basket:

    def __init__(self, state_factory):
        self.no_resurrect = True
        self.state = state_factory.create_states(default_state='proposed', verifier=self.__check_resurrect)
        self.state.add('backlog')
        self.state.add('pending')
        self.state.add('doing')
        self.state.add('review')
        self.state.add('finished')
        self.state.add('blocked')
        self.state.alias('doingblocked', self.state.DOING | self.state.BLOCKED)
        self.state.alias('pendingblocked', self.state.PENDING | self.state.BLOCKED)
        self.limit = self.state.FINISHED
        self.state.sync()

        self.__tags = state_factory.create_tags()
        self.__tags.sync(ignore_auto=False)

        self.__msg = state_factory.create_messages()

        self.issues_rev = {}


    def __check_resurrect(self, st, k, f, t):
        if self.no_resurrect:
            if f & self.state.FINISHED > 0:
                raise DeadIssue(k)


    def add(self, issue):
        issue_id = str(issue.id)
        self.state.put(issue_id, contents=str(issue))
        self.__tags.put(issue_id)
        return issue_id


    def get(self, issue_id):
        r = self.state.get(issue_id)
        o = Issue.from_str(r)
        return o


    def list(self, category=None):
        if category == None:
            category = self.state.BACKLOG
        else:
            category = self.state.from_name(category)
        return self.state.list(category)


    def state_doing(self, issue_id):
        self.state.move(issue_id, self.state.DOING)


    def state_review(self, issue_id):
        self.state.move(issue_id, self.state.REVIEW)


    def state_backlog(self, issue_id):
        self.state.move(issue_id, self.state.BACKLOG)


    def state_finish(self, issue_id):
        self.state.move(issue_id, self.state.FINISHED)


    def advance(self, issue_id):
        if self.state.state(issue_id) & self.limit > 0:
            raise DeadIssue(issue_id)
        self.unblock(issue_id)
        self.state.next(issue_id)


    def unblock(self, issue_id):
        if self.state.state(issue_id) & self.state.BLOCKED > 0:
            self.state.unset(issue_id, self.state.BLOCKED)


    def block(self, issue_id):
        self.state.set(issue_id, self.state.BLOCKED)


    def blocked(self):
        return self.list('blocked')


    def states(self):
        return self.state.all(pure=True, bit_order=True)


    def tag(self, issue_id, tag):
        v = 0
        try:
            v = self.__tags.from_name(tag)
        except AttributeError:
            self.__tags.add(tag)
            v = self.__tags.from_name(tag)
      
        move = False
        try:
            r = self.__tags.state(issue_id)
            if r == 0:
                move = True
        except shep.error.StateItemNotFound:
            self.__tags.put(issue_id)
            move = True

        if move:
            self.__tags.move(issue_id, v)
        else:
            self.__tags.set(issue_id, v)



    def untag(self, issue_id, tag):
        v = self.__tags.from_name(tag)
        self.__tags.unset(issue_id, v, allow_base=True)


    def tags(self, issue_id):
        v = self.__tags.state(issue_id)
        r = self.__tags.elements(v)
        if r == 'UNTAGGED':
            r = '(' + r + ')'
        return shep.state.split_elements(r)


    def __get_msg(self, issue_id):
        r = self.state.get(issue_id)
        o = Issue.from_str(r)
        try:
            v = self.__msg.get(issue_id)
            return IssueMessage.parse(o, v.decode('utf-8'))
        except FileNotFoundError:
            logg.debug('instantiating new message log for {}'.format(issue_id))

        return IssueMessage(o)


    def msg(self, issue_id, *args):
        m = self.__get_msg(issue_id)
        m.add(*args)
        ms = m.as_bytes()
        self.__msg.put(issue_id, ms)
        return m

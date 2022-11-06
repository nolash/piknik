import shep

from .error import DeadIssue


class Basket:

    def __init__(self, state_factory):
        self.no_resurrect = True
        self.state = state_factory(default_state='backlog', verifier=self.__check_resurrect)
        self.state.add('pending')
        self.state.add('doing')
        self.state.add('review')
        self.state.add('finished')
        self.state.add('blocked')

        self.state.alias('doingblocked', self.state.DOING | self.state.BLOCKED)
        self.state.alias('pendingblocked', self.state.PENDING | self.state.BLOCKED)

        self.limit = self.state.FINISHED
        self.issues_rev = {}


    def __check_resurrect(self, st, k, f, t):
        if self.no_resurrect:
            if f & self.state.FINISHED > 0:
                raise DeadIssue(k)


    def add(self, issue):
        issue_id = str(issue.id)
        self.state.put(issue_id, contents=str(issue))
        self.issues_rev[issue_id] = issue
        return issue_id


    def get(self, issue_id):
        return self.issues_rev[issue_id]

    
    def list(self, category=None):
        if category == None:
            category = self.state.BACKLOG
        else:
            category = self.state.from_name(category)
        return self.state.list(category)


    def doing(self, issue_id):
        self.state.move(issue_id, self.state.DOING)


    def review(self, issue_id):
        self.state.move(issue_id, self.state.REVIEW)


    def backlog(self, issue_id):
        self.state.move(issue_id, self.state.BACKLOG)


    def finish(self, issue_id):
        self.state.move(issue_id, self.state.FINISHED)


    def advance(self, issue_id):
        if self.state.state(issue_id) & self.limit > 0:
            raise DeadIssue(issue_id)
        self.unblock(issue_id)
        self.state.next(issue_id)


    def unblock(self, issue_id):
        if self.state.state(issue_id) & self.state.BLOCKED > 0:
            print('unset')
            self.state.unset(issue_id, self.state.BLOCKED)


    def block(self, issue_id):
        self.state.set(issue_id, self.state.BLOCKED)


    def blocked(self):
        return self.list('blocked')

import shep


class Basket:

    def __init__(self, state_factory):
        self.state = state_factory(default_state='backlog')
        self.state.add('pending')
        self.state.add('doing')
        self.state.add('review')
        self.state.add('finished')
        self.state.add('blocked')
        self.limit = self.state.FINISHED
        self.issues_rev = {}


    def add(self, issue):
        self.state.put(issue.id, contents=issue)
        self.issues_rev[issue.id] = issue
        return issue.id


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

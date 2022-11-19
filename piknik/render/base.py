import sys


class Renderer:

    def apply_begin(self, w=sys.stdout):
        pass


    def apply_state_pre(self, state, w=sys.stdout):
        pass


    def apply_state(self, state, w=sys.stdout):
        pass


    def apply_issue_pre(self, state, issue, tags, w=sys.stdout):
        pass


    def apply_issue(self, state, issue, tags, w=sys.stdout):
        pass

    
    def apply_issue_post(self, state, issue, tags, w=sys.stdout):
        pass


    def apply_state_post(self, state, w=sys.stdout):
        pass


    def apply_end(self, w=sys.stdout):
        pass

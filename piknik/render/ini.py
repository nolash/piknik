import sys

from .base import Renderer as BaseRenderer


class Renderer(BaseRenderer):

    def apply_state(self, state, w=sys.stdout):
        w.write('[' + state + ']\n') 


    def apply_issue(self, state, issue, tags, w=sys.stdout):
        w.write('{}\t{}\t{}\n'.format(issue.title, ','.join(tags), issue.id))


    def apply_state_post(self, state, w=sys.stdout):
        w.write('\n')

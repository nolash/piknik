import sys

from .base import Renderer as BaseRenderer


class Renderer(BaseRenderer):

    def apply_state(self, state, w=sys.stdout):
        w.write('[' + state + ']\n') 


    def apply_issue(self, state, issue, tags, w=sys.stdout):
        w.write('{}\t{}\t{}\n'.format(issue.title, ','.join(tags), issue.id))


    def apply_state_post(self, state, w=sys.stdout):
        w.write('\n')


    def apply_message_part(self, state, issue, envelope, message, message_from, message_date, message_id, message_valid, dump_dir=None, w=sys.stdout):
        pass


    def apply_message_post(self, state, issue, tags, message, message_from, message_date, message_id, message_valid, w=sys.stdout):
        pass

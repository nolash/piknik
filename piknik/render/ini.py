# local imports
from .base import Renderer as BaseRenderer
from .base import stream_accumulator


class Renderer(BaseRenderer):

    def __init__(self, basket, accumulator=stream_accumulator):
        super(Renderer, self).__init__(basket, accumulator=accumulator)


    def apply_state(self, state, accumulator=None):
        s = '[' + state + ']\n'
        self.add(s, accumulator=accumulator) 
        super(Renderer, self).apply_state(state, accumulator=accumulator)


    def apply_issue(self, state, issue, tags, accumulator=None):
        s = '{}\t{}\t{}\n'.format(
                issue.title,
                ','.join(tags),
                issue.id,
                )
        self.add(s, accumulator=accumulator)


    def apply_state_post(self, state, accumulator=None):
        self.add('\n', accumulator=accumulator)

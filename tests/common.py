# standard imports
import logging

# external imports
import shep

logg = logging.getLogger()


def debug_out(self, k, v):
    logg.debug('TRACE: {} {}'.format(k, v))


class TestMsgStore:

    def __init__(self):
        self.store = {}

    def put(self, k, v):
        self.store[k] = v

    def get(self, k):
        try:
            return self.store[k]
        except KeyError:
            pass
        raise FileNotFoundError(k)


class TestStates:

    def create_states(*args, **kwargs):
        return shep.State(6, *args, event_callback=debug_out, **kwargs)


    def create_tags(*args, **kwargs):
        return shep.State(0, *args, event_callback=debug_out, check_alias=False, **kwargs)


    def create_messages(*args):
        return TestMsgStore()

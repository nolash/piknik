# standard imports
import logging

# external imports
import shep

logg = logging.getLogger()


def debug_out(self, k, v):
    logg.debug('TRACE: {} {}'.format(k, v))


class TestStates:

    def create_states(*args, **kwargs):
        return shep.State(7, *args, event_callback=debug_out, **kwargs)


    def create_tags(*args, **kwargs):
        return shep.State(0, *args, event_callback=debug_out, check_alias=False, **kwargs)

import os

from shep.store.file import SimpleFileStoreFactory
from shep.persist import PersistedState


class FileStoreFactory:

    def __init__(self, directory=None):
        if directory == None:
            directory = os.path.join(os.environ['HOME'], '.piknik')
        self.directory = directory


    def create_states(self, logger=None, default_state=None, verifier=None):
        factory = SimpleFileStoreFactory(self.directory).add
        return PersistedState(factory, 7, logger=logger, verifier=verifier, default_state=default_state)

    
    def create_tags(self, logger=None, default_state=None, verifier=None):
        directory = os.path.join(self.directory, '.tags')
        os.makedirs(directory, exist_ok=True)
        factory = SimpleFileStoreFactory(directory)
        state = PersistedState(factory.add, 0, logger=logger, check_alias=False, default_state='untagged')
        aliases = []
        for k in factory.ls():
            if k == 'UNTAGGED':
                continue
            elif k[0] == '_':
                aliases.append(k)
                continue
            state.add(k)

        for v in aliases:
            s = state.from_elements(v)
            state.alias(v, s)
                
        return state

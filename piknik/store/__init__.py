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
        return PersistedState(factory, 6, logger=logger, verifier=verifier, default_state=default_state)

    
    def create_tags(self, logger=None, default_state=None, verifier=None):
        directory = os.path.join(self.directory, '.tags')
        factory = SimpleFileStoreFactory(directory).add
        return PersistedState(factory, 0, logger=logger, check_alias=False, default_state='untagged')

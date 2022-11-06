import os

from shep.store.file import SimpleFileStoreFactory
from shep.persist import PersistedState


class FileStoreFactory:

    def __init__(self, directory=None):
        if directory == None:
            directory = os.path.join(os.environ['HOME'], '.piknik')
        self.directory = directory
        self.factory = SimpleFileStoreFactory(directory).add


    def create(self, logger=None, default_state=None, verifier=None):
        return PersistedState(self.factory, 6, logger=logger, verifier=verifier, default_state=default_state)

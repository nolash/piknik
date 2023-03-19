# standard imports
import os

# local imports
from piknik import Basket
from piknik.store import FileStoreFactory


class Context:

    def __init__(self, arg, assembler, mode=0, gpg_home=os.environ.get('GPGHOME')):
        self.issue_id = arg.issue_id
        self.files_dir = arg.files_dir
        #self.store_factory = FileStoreFactory(arg.d)
        store_factory = FileStoreFactory(arg.d)
        self.basket = Basket(store_factory)
        self.gpg_home = gpg_home
        assembler(self, arg)

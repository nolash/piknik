# external imports
import gnupg


class Signer:

    def __init__(self, home_dir=None, default_key=None):
        self.gpg = gnupg.GPG(gnupghome=home_dir)
        self.default_key = default_key


    def sign(self, issue_msg):
        pass 

import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory
from piknik.crypto import PGPSigner


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-s', '--sign-as', dest='s', type=str, help='PGP fingerprint of key to sign issue update with')
argp.add_argument('-m', '--message', type=str, required=True, help='Add literal message text')
argp.add_argument('issue_id', type=str, help='Issue id to modify')
arg = argp.parse_args(sys.argv[1:])

signer = PGPSigner(default_key=arg.s, use_agent=True)
store_factory = FileStoreFactory(arg.d)
#basket = Basket(store_factory, message_wrapper=wrapper, message_verifier=verifier)
basket = Basket(store_factory, message_wrapper=signer.sign)


def main():
    basket.msg(arg.issue_id, 's:' + arg.message)


if __name__ == '__main__':
    main()

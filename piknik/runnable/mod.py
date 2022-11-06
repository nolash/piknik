import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('issue_id', type=str, help='Issue id to modify')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory.create)


def main():
    o = basket.get(arg.issue_id)


if __name__ == '__main__':
    main()

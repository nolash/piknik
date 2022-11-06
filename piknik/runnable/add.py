import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.cli import FileStoreFactory


argp = argparse.ArgumentParser()
argp.add_argument('title', type=str, help='issue title')
arg = argp.parse_args(sys.argv[1:])


store_factory = FileStoreFactory()
basket = Basket(store_factory.create)


def main():
    o = Issue(arg.title)
    basket.add(o)


if __name__ == '__main__':
    main()

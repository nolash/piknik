import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('title', type=str, help='issue title')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory.create)


def main():
    o = Issue(arg.title)
    v = basket.add(o)
    sys.stdout.write(v + '\n')


if __name__ == '__main__':
    main()

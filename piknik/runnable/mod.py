import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('--block', action='store_true', help='Set issue as blocked')
argp.add_argument('--unblock', action='store_true', help='Set issue as unblocked')
argp.add_argument('--finish', action='store_true', help='Set issue as finished (alias of -s finish)')
argp.add_argument('-s', '--state', type=str, help='Move to state')
argp.add_argument('issue_id', type=str, help='Issue id to modify')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory.create)


def main():
    o = basket.get(arg.issue_id)

    if arg.block:
        basket.block(arg.issue_id)
    elif arg.unblock:
        basket.unblock(arg.issue_id)

    if arg.state != None:
        m = getattr(basket, 'state_' + arg.state)
        m(arg.issue_id)
    elif arg.finish:
        basket.state_finish(arg.issue_id)


if __name__ == '__main__':
    main()

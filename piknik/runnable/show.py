import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-r', '--renderer', type=str, default='default', help='Renderer module for output')
argp.add_argument('issue_id', type=str, help='Issue id to show')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory)


def render_default(b, o, t):
    print("""id: {}
title: {}
tags: {}
""".format(
        o.id,
        o.title,
        ', '.join(t),
            )
          )

    assigned = o.get_assigned()

    if len(assigned) == 0:
        print('(not assigned)')
        return

    print('assigned to:')
    owner = o.owner()
    for v in assigned:
        o = v[0]
        s = o.id()
        if o == owner:
            s += ' (owner)'
        print('\t' + str(s))

    m = basket.get_msg(arg.issue_id)
    print()
    print(m)


def main():
    o = basket.get(arg.issue_id)
    t = basket.tags(arg.issue_id)

    globals()['render_' + arg.renderer](basket, o, t)
    

if __name__ == '__main__':
    main()

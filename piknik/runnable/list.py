import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-s', '--state', type=str, action='append', default=[], help='Include state in list')
argp.add_argument('-r', '--renderer', type=str, default='ini', help='Renderer module for output')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory.create)


def render_ini(b, r):
    for k in r.keys():
        print('[' + k + ']') 

        for v in r[k]:
            o = b.get(v)
            print('{}\t{}'.format(o.title, v))

        print()


def main():
    results = {}
    states = []
    for s in arg.state:
        states.append(s.upper())

    l = len(states)
    for s in basket.states():
        if results.get(s) == None:
            results[s] = []

        if l == 0 or s in states:
            for v in basket.list(category=s):
               results[s].append(v)

    globals()['render_' + arg.renderer](basket, results)


if __name__ == '__main__':
    main()

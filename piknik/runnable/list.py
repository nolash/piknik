import sys
import argparse

from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory


argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-s', '--state', type=str, action='append', default=[], help='Include state in list')
argp.add_argument('--show-finished', dest='show_finished', action='store_true', help='Include finished issues')
argp.add_argument('-r', '--renderer', type=str, default='ini', help='Renderer module for output')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory)


def render_ini(b, r):
    for k in basket.states():
        if k == 'FINISHED' and not arg.show_finished:
            continue

        print('[' + k + ']') 

        for v in r[k]:
            o = b.get(v)
            t = b.tags(v)
            print('{}\t{}\t{}'.format(o.title, ','.join(t), v))

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

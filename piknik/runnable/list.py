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


def render(b, r, m):
    m.apply_begin()

    for k in basket.states():
        if k == 'FINISHED' and not arg.show_finished:
            continue

        m.apply_state(k)

        for v in r[k]:
            if k != 'BLOCKED' and v in r['BLOCKED']:
                continue
            o = b.get(v)
            t = b.tags(v)
            m.apply_issue(k, v, o, t)
            m.apply_issue_post(k, v, o, t)

        m.apply_state_post(k)

    m.apply_end()


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

    import piknik.render.html
    m = piknik.render.html.Renderer()
    #globals()['render_' + arg.renderer](basket, results, m)
    render(basket, results, m)


if __name__ == '__main__':
    main()

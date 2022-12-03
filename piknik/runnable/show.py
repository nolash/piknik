# standard imports
import io
import os
import sys
import argparse
import logging
import tempfile
from base64 import b64decode
from email.utils import parsedate_to_datetime
import importlib

# local imports
from piknik import Basket
from piknik import Issue
from piknik.store import FileStoreFactory
from piknik.crypto import PGPSigner
from piknik.render.plain import Renderer

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-f', '--files', dest='f', action='store_true', help='Save attachments to filesystem')
argp.add_argument('-o', '--files-dir', dest='files_dir', type=str, default='.', help='Directory to output saved files to')
argp.add_argument('-r', '--renderer', type=str, default='default', help='Renderer module for output')
argp.add_argument('-s', '--state', type=str, action='append', default=[], help='Limit results to state(s)')
argp.add_argument('--show-finished', dest='show_finished', action='store_true', help='Include finished issues')
argp.add_argument('--reverse', action='store_true', help='Sort comments by oldest first')
argp.add_argument('issue_id', type=str, nargs='?', default=None, help='Issue id to show')
arg = argp.parse_args(sys.argv[1:])

store_factory = FileStoreFactory(arg.d)
basket = Basket(store_factory)

gpg_home = os.environ.get('GPGHOME')


def main():

    renderer = arg.renderer
    if renderer == 'default':
        renderer = 'piknik.render.plain'
    elif renderer == 'html':
        renderer = 'piknik.render.html'

    m = None
    try:
        m = importlib.import_module(renderer)
    except ModuleNotFoundError:
        renderer = 'piknik.render.' + renderer
        m = importlib.import_module(renderer)


    if arg.issue_id == None:
        renderer = m.Renderer(basket)
        renderer.apply()
        return

    issue = basket.get(arg.issue_id)
    tags = basket.tags(arg.issue_id)
    state = basket.get_state(arg.issue_id)
    verifier = PGPSigner(home_dir=gpg_home, skip_verify=False)
    renderer = m.Renderer(basket, wrapper=verifier)

    renderer.apply_begin()
    renderer.apply_issue(state, issue, tags)
    renderer.apply_end()
    

if __name__ == '__main__':
    main()

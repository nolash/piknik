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
from piknik.cli import Context
from piknik.cli.show import subparser as subparser_show
from piknik.cli.mod import subparser as subparser_mod
from piknik.cli.add import subparser as subparser_add

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-f', '--files', dest='f', action='store_true', help='Save attachments to filesystem')
argp.add_argument('-o', '--files-dir', dest='files_dir', type=str, help='Directory to output saved files to')
argp.add_argument('-i','--issue-id',  type=str, help='Issue id to show')

argsub = argp.add_subparsers(title='subcommand', dest='subcmd')
argsub = subparser_show(argsub)
argsub = subparser_mod(argsub)
argsub = subparser_add(argsub)
arg = argp.parse_args(sys.argv[1:])

m = None
if arg.subcmd == 'show':
    m = importlib.import_module('piknik.cli.show')
elif arg.subcmd == 'mod':
    m = importlib.import_module('piknik.cli.mod')
elif arg.subcmd == 'add':
    m = importlib.import_module('piknik.cli.add')
else:
    raise ValueError('invalid subcommand: ' + arg.subcmd)

m.ctx = Context(arg, m.assembler)

if __name__ == '__main__':
    m.main()

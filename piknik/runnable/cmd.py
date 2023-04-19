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
import copy

# local imports
from piknik.cli import Context
from piknik.cli.show import subparser as subparser_show
from piknik.cli.mod import subparser as subparser_mod
from piknik.cli.add import subparser as subparser_add
from piknik.cli.comment import subparser as subparser_comment

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

argp = argparse.ArgumentParser()
argp.add_argument('-d', type=str, help='Data directory')
argp.add_argument('-f', '--files', dest='f', action='store_true', help='Save attachments to filesystem')
argp.add_argument('-o', '--files-dir', dest='files_dir', type=str, help='Directory to output saved files to')
argp.add_argument('-v', action='store_true', help='Turn on debug logs')
argp.add_argument('-i','--issue-id',  type=str, help='Issue id to show')
argp.add_argument('cmd', type=str, help='subcommand to execute')
strargs = copy.copy(sys.argv[1:])
try:
    strargs.remove('-h')
except ValueError:
    pass
try:
    strargs.remove('--help')
except ValueError:
    pass
arg, unknown = argp.parse_known_args(strargs)

m = None
if arg.cmd == 'show':
    m = importlib.import_module('piknik.cli.show')
elif arg.cmd == 'add':
    m = importlib.import_module('piknik.cli.add')
elif arg.cmd == 'mod':
    m = importlib.import_module('piknik.cli.mod')
elif arg.cmd == 'comment':
    m = importlib.import_module('piknik.cli.comment')
else:
    raise ValueError('unknown subcommand')


argp = m.subparser(argp)
arg = argp.parse_args(sys.argv[1:])
if arg.v:
    logg.setLevel(logging.DEBUG)

m.ctx = Context(arg, m.assembler)


def main():
    global m
    m.main()


if __name__ == '__main__':
    main()

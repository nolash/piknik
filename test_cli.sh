#!/bin/bash

set -a
set -e
set -x
default_pythonpath=$PYTHONPATH:.
export PYTHONPATH=${default_pythonpath:-.}
d=`mktemp -d`
g=`mktemp -d`

# works with gnupg 2.2.41
export GNUPGHOME=$g
gpg --homedir $g --passphrase '' --quick-generate-key --pinentry loopback --yes testuser
fp=`gpg --list-keys --homedir $g testuser 2> /dev/null | awk '/^ / {print $1;}'`

i_foo=`python piknik/runnable/cmd.py add "foo"`
i_bar=`python piknik/runnable/cmd.py add "bar"`

python piknik/runnable/cmd.py mod --accept -i $i_foo
python piknik/runnable/cmd.py mod --finish -i $i_bar
python piknik/runnable/cmd.py comment -s $fp -x bazbazbaz -i $i_foo
python piknik/runnable/cmd.py show
python piknik/runnable/cmd.py show -r html
python piknik/runnable/cmd.py show -i $i_foo
python piknik/runnable/cmd.py show -r html -i $i_bar
set +x
set +e
set +a




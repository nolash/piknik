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

i_foo=`python piknik/runnable/cmd.py -d $d add "foo"`
i_bar=`python piknik/runnable/cmd.py -d $d add "bar"`

python piknik/runnable/cmd.py mod -d $d --accept -i $i_foo 
python piknik/runnable/cmd.py mod -d $d --finish -i $i_bar
python piknik/runnable/cmd.py comment -d $d -s $fp -x bazbazbaz -i $i_foo
python piknik/runnable/cmd.py show -d $d 
python piknik/runnable/cmd.py show -d $d -r html
python piknik/runnable/cmd.py show -d $d -i $i_foo
python piknik/runnable/cmd.py show -d $d -r html -i $i_bar
set +x
set +e
set +a




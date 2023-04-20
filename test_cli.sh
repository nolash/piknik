#!/bin/bash

set -a
set -e
set -x
default_pythonpath=$PYTHONPATH:.
export PYTHONPATH=${default_pythonpath:-.}
d=`mktemp -d`
i_foo=`python piknik/runnable/cmd.py add "foo"`
i_bar=`python piknik/runnable/cmd.py add "bar"`
python piknik/runnable/cmd.py mod --accept -i $i_foo
python piknik/runnable/cmd.py mod --finish -i $i_bar
python piknik/runnable/cmd.py comment -x bazbazbaz -i $i_foo
python piknik/runnable/cmd.py show
python piknik/runnable/cmd.py show -r html
python piknik/runnable/cmd.py show -i $i_foo
python piknik/runnable/cmd.py show -r html -i $i_bar
set +x
set +e
set +a




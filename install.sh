#!/usr/bin/env bash

cd "$(dirname $0)"

dir=$(pwd)

cd
cd bin

ln -s $dir/nscp.py nscp
ln -s $dir/sshow.sh sshow
ln -s $dir/nssh.py nssh
#!/bin/env bash

set -eu

cd $(dirname $0)

SRC_DIR=$(pwd)

if [ -z ${TARGET_DIR+x} ] ; then
	TARGET_DIR=$(echo $PATH | tr ":" "\n" | grep $HOME | head -n 1) 

	if [ `whoami` = "root" ] ; then
		TARGET_DIR=/usr/bin
	fi
fi

install () {
  	echo installing into $TARGET_DIR

	cd $TARGET_DIR

	cp $SRC_DIR/nscp.py nscp
	cp $SRC_DIR/sshow.sh sshow
	cp $SRC_DIR/nssh.py nssh

	chmod +x nscp sshow nssh
}

uninstall () {
  	echo uninstalling from $TARGET_DIR
	cd $TARGET_DIR
 	rm -f nscp sshow nssh
}



install_dev () {
	echo linking source files into $TARGET_DIR

	cd $TARGET_DIR

	ln -s $SRC_DIR/nscp.py nscp
	ln -s $SRC_DIR/sshow.sh sshow
	ln -s $SRC_DIR/nssh.py nssh

	chmod +x nscp sshow nssh

}

test () {
	set -x
	echo $TARGET_DIR
	echo $SRC_DIR
}

"$@"
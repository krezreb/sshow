#!/bin/bash

LONGFORM=false
if [[ "$@" == *"--long"* ]] ; then
    LONGFORM=true
    shift
fi
if [[ "$@" == *"-l"* ]] ; then
    LONGFORM=true
    shift
fi

SEARCH=$1
if [ -z "${SEARCH+x}" ]; then
	SEARCH=''
fi

GOTO=$2
if [ -z "${GOTO+x}" ]; then
    GOTO=''
fi

include=$(cat ~/.ssh/config | grep -v "^#" | grep Include | cut -d ' ' -f 2 )
if [ -z "${include}" ]
then
	include=" "
else
	include=$(eval find -L $include  -maxdepth 0  -type f  )
fi


for line in $(grep -iHne "^Host "  ~/.ssh/config $include | cut -d '#' -f 1 | grep -v \* | grep -i  "${SEARCH/,/\\\|}" | sed "s/:Host /:/g"  ) ; do

    file=$(echo $line | cut -d ':' -f 1)
    linenum=$(echo $line | cut -d ':' -f 2)
    host=$(echo $line | cut -d ':' -f 3)

    if [ $LONGFORM == true ] ; then
        echo -e "$host\t\t\t$file\t$linenum"
    else
        if [ "$GOTO" == "go" ] ; then
          echo "sshing to $host"
          ssh $host
          exit  
        fi
        echo $host
    fi
done


#!/bin/bash 

SEARCH=$1
if [ -z "${SEARCH+x}" ]; then
	SEARCH=''
fi

include=$(cat ~/.ssh/config | grep Include | cut -d ' ' -f 2 )
if [ -z "${include}" ]
then
	include=" "
else
	include=$(eval ls $include)
fi

cat ~/.ssh/config $include | grep "^Host " | grep -i  "${SEARCH/,/\\\|}" |  cut -d ' ' -f 2 | cut -d '#' -f 1 | grep -v \* | sort



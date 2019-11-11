#!/bin/bash

workdir=$(cd $(dirname $0); pwd)
crontab -l > conf 2>/dev/null
echo "* * * * * sh $workdir/start.sh > /dev/null 2>&1 &" >> conf && crontab conf && rm -f conf


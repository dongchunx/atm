#!/bin/bash

source ./global.sh

#若端口处于监听状态，则认为服务正常运行
port=`netstat -lntp | grep $PORT`
if [ -n "$port" ]
then
    #服务正常,退出
    PIDS=`ps aux |grep $PROGRESS | grep -v grep | awk '{print $2}'`
    for PID in $PIDS
    do
        kill -9 $PID
    done
    echo
    echo
    echo "stop server success"
else
    #无服务,不需要终止
    echo
    echo
    echo "no server started"
fi


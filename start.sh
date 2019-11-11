#!/bin/bash

#获取shell脚本目录
workdir=$(cd $(dirname $0); pwd)
cd $workdir
source ./global.sh

#若端口处于监听状态，则认为服务正常运行
port=`netstat -lntp | grep $PORT`
if [ -n "$port" ]
then
    #服务正常,退出
    echo
    echo
    echo "server already started"
    exit
else
    #服务异常，重新启动
    nohup ./Python3/bin/python3 $PROGRESS 2>&1  &
    echo
    echo
    echo "start server success"
fi


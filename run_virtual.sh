#!/bin/sh

./build.sh

can_bak=0
if [ -e can.ini ]; then
    cp can.ini can.ini.bak
    can_bak=1
fi
cp virtual-can.ini can.ini

. ./venv/bin/activate && ./app

rm can.ini
if [ ${can_bak} -ne 0 ]; then
    mv can.ini.bak can.ini
fi

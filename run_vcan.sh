#!/bin/sh

sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set dev vcan0 up


./build.sh

can_bak=0
if [ -e can.ini ]; then
    cp can.ini can.ini.bak
    can_bak=1
fi
cp vcan-can.ini can.ini

candump vcan0 &
p1=$!

{ for i in $(seq 0 10); do cansend vcan0 100#010203; sleep 0.3; done; } &
p2=$!


. ./venv/bin/activate && ./app

wait $p2
kill $p1

rm can.ini
if [ ${can_bak} -ne 0 ]; then
    mv can.ini.bak can.ini
fi

sudo ip link set dev vcan0 down
sudo ip link delete dev vcan0

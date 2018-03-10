#!/bin/bash

set -e

PORT=/dev/ttyUSB0
SPEED=115200
PYTHON=esp8266-20170108-v1.8.7.bin 
URL=http://micropython.org/resources/firmware/$PYTHON

# download micropython
if [ ! -f $PYTHON ]; then
	wget $URL
fi

# flash python to ESP
esptool.py --port $PORT erase_flash
esptool.py --port $PORT --baud $SPEED write_flash --flash_size=detect --flash_mode=dio 0 $PYTHON


sleep 10
echo "== Reset board now =="

# setup network
python setup-network.py $PORT 

# upload code
( cd ..; 
  for i in *.py; do 
	   echo -e "Uploading $i "; 
	   ampy -p /dev/ttyUSB1 put $i ; 
           echo OK;
   done
)

while [ x"$1" != x ]; do
    pushd $1
    for i in *.py; do
        echo -e "Uploading $i "
        ampy -p /dev/ttyUSB1 put $i
        echo OK
    done
    popd
    shift
fi

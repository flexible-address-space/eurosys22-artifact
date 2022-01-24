#!/bin/bash

echo Left rows: 10^5 insert and 10^8 append/lookup/range

make -B M=j INSERT=100000lu REGULAR=100000000lu 1>/dev/null
./test.out
make -B M=j INSERT=100000lu REGULAR=100000000lu BTREE=y 1>/dev/null
./test.out
make -B M=j INSERT=100000lu REGULAR=100000000lu ARRAY=y 1>/dev/null
./test.out

echo
echo Right rows: 10^6 insert and 10^9 append/lookup/range

make -B M=j INSERT=1000000lu REGULAR=1000000000lu 1>/dev/null
./test.out
make -B M=j INSERT=1000000lu REGULAR=1000000000lu BTREE=y 1>/dev/null
./test.out
make -B M=j INSERT=1000000lu REGULAR=1000000000lu ARRAY=y 1>/dev/null
./test.out

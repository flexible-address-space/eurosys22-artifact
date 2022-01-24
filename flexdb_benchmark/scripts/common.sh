#!/bin/bash

export FORKER_ASYNC_SHIFT=1

export disk="/dev/nvme1n1"
export basedir="/home/flex/mnt"

sudo umount $basedir
sudo mkfs.xfs -f $disk
sudo mount $disk $basedir
sudo chown -R flex:flex $basedir
sudo chmod -R 770 $basedir

sleep 5

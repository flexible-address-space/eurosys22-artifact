#!/bin/bash

disk="/dev/nvme1n1"
basedir="/home/flex/mnt"

function __format {
    sleep 10

    s=${1}
    sudo umount $basedir
    sleep 2

    if [ "$s" = "flexfile" ] || [ "$s" = "xfs" ]; then
        sudo mkfs.xfs -f $disk
    elif [ "$s" = "ext4" ]; then
        sudo mkfs.ext4 $disk
    elif [ "$s" = "f2fs" ]; then
        sudo mkfs.f2fs -f $disk
    elif [ "$s" = "btrfs" ]; then
        sudo mkfs.btrfs -f $disk
    else
        echo "missing format dev";
        exit 1;
    fi
    sleep 2

    sudo mount $disk $basedir
    sudo chown -R flex:flex $basedir
    sudo chmod -R 770 $basedir
}

path="$basedir"/testfile

blksz=${1}
filesz=${2}

if [ -z "$blksz" ] || [ -z "$filesz" ]; then
    echo "Usage: ./multi.sh <blksz> <filesz>"
    exit 1
fi

output=./results/flexfile/multi-$blksz-$filesz

mkdir -p "$output"

make -B -j16 M=j

for s in flexfile xfs; do
    if [ "$s" = "flexfile" ]; then
        pprefix="flexfile_"
    else
        pprefix=""
    fi

    __format $s

    # write phase
    ./"$pprefix"randw.out $path $blksz $filesz
    sleep 2

    # read phase
    for t in 1 2 4 8; do
        ./drop_cache.sh
        ./"$pprefix"read_m.out $path $blksz $filesz $t 0 | tee "$output"/"$s"_seqr_cold_"$t"
        sleep 1
        ./"$pprefix"read_m.out $path $blksz $filesz $t 0 | tee "$output"/"$s"_seqr_warm_"$t"

        ./drop_cache.sh
        ./"$pprefix"read_m.out $path $blksz $filesz $t 1 | tee "$output"/"$s"_randr_cold_"$t"
        sleep 1
        ./"$pprefix"read_m.out $path $blksz $filesz $t 1 | tee "$output"/"$s"_randr_warm_"$t"
    done
done

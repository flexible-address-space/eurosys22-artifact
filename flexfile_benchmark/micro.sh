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
        sudo mkfs.ext4 -F $disk
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
    echo "Usage: ./micro.sh <blksz> <filesz>"
    exit 1
fi

output=./results/flexfile/micro-$blksz-$filesz

mkdir -p "$output"

make -B -j16 M=j

for s in flexfile xfs ext4 f2fs btrfs; do
    if [ "$s" = "flexfile" ]; then
        pprefix="flexfile_"
    else
        pprefix=""
    fi

    for e in insert seqw randw; do
        if [ "$e" = "insert" ]; then
            if [ "$s" = "f2fs" ] || [ "$s" = "btrfs" ]; then
                continue
            fi
        fi

        __format $s

        # write phase
        sudo smartctl -a $disk | tee "$output"/"$s"_"$e"_smart_before
        ./"$pprefix""$e".out $path $blksz $filesz | tee "$output"/"$s"_"$e"
        sudo smartctl -a $disk | tee "$output"/"$s"_"$e"_smart_after

        sleep 2

        # read phase
        for r in seqr randr; do
            ./drop_cache.sh
            ./"$pprefix""$r".out $path $blksz $filesz | tee "$output"/"$s"_"$e"_"$r"_cold
            sleep 1
            ./"$pprefix""$r".out $path $blksz $filesz | tee "$output"/"$s"_"$e"_"$r"_warm
        done
    done
done

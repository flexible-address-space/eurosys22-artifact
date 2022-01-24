#!/bin/bash

source ./scripts/common.sh

OUTDIR="results/flexdb/ycsb-mem/"

mkdir -p "${OUTDIR}"

runit()
{
  local fill=${1}
  local maxk=$((${fill} - 1))
  local fp=$((${fill} / ${nt} - 1))

  local out1="${s}-ycsb-mem-${d[0]}-${sys[2]}"
  local vlen=${d[2]}
  local klen=${d[1]}
  local scan="50"

  # simulate YCSB ABCDE    wargs[6] <pset> <pupd> <pget> <pscn> <vlen> <nscan>

  numactl -N 0 --preferred=0 \
    ./dbtest1.out api ${sys[@]} \
      rgen incu    0 ${maxk}      pass ${nt} 1 ${maxk} 1 0 3 S ${klen} ${vlen}\
  | tee "${OUTDIR}"/"${out1}"

  numactl -N 0 --preferred=0 \
    ./ycsbtest.out api ${sys[@]} \
      rgen zipfian 0 ${maxk} pass ${nt} 0         60 1 0 7   50 0  50  0 ${klen} ${vlen} ${scan} \
      rgen zipfian 0 ${maxk} pass ${nt} 0         60 1 0 7   5 0   95  0 ${klen} ${vlen} ${scan} \
      rgen zipfian 0 ${maxk} pass ${nt} 0         60 1 0 7   0  0 100  0 ${klen} ${vlen} ${scan} \
      rgen latest       1000 pass ${nt} 0         60 1 0 7   5  0  95  0 ${klen} ${vlen} ${scan} \
      rgen zipfian 0 ${maxk} pass ${nt} 0         60 1 0 7   5  0   0 95 ${klen} ${vlen} ${scan} \
      rgen zipfian 0 ${maxk} pass ${nt} 0         60 1 0 7   0 50  50  0 ${klen} ${vlen} ${scan} \
  | tee -a "${OUTDIR}"/"${out1}"
}

cachesz=$3

if [ -z "$cachesz" ]; then
    echo "Usage: ./ycsb-mem.sh <sys> <dataset> <cachesz>"
    exit 1
fi

case $1 in
rdb)
  sys=('rdb' "$basedir/rdb" "$cachesz")
  ;;
fdb)
  sys=('flexdb' "$basedir/fdb" "$cachesz")
  ;;
*)
  exit 0
  ;;
esac

case $2 in
udb)
    d=(udb 27 127)
    run=420000000
    ;;
zippydb)
    d=(zippydb 48 43)
    run=720000000
    ;;
sys)
    d=(sys 28 396)
    run=150000000
    ;;
*)
    exit 0
    ;;
esac

make -B O=rg ycsbtest.out ROCKSDB=y LEVELDB=y KVELL=y M=j
make -B O=rg dbtest1.out ROCKSDB=y LEVELDB=y KVELL=y M=j

s=$1
nt=4
rm -rf ${sys[1]}

runit ${run}

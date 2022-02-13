#!/bin/bash

source ./scripts/common.sh

OUTDIR="results/flexdb/scale/"

mkdir -p "${OUTDIR}"

runit()
{
  local fill=${1}
  local maxk=$((${fill} - 1))
  local fp=$((${fill} / ${nt} - 1))

  local out1="${s}-scale-write-${d[0]}-${nt}"
  local vlen=${d[2]}
  local klen=${d[1]}
  local scan="50"

  numactl -N 0 --preferred=0 \
    ./dbtest1.out api ${sys[@]} \
      rgen zipfian 0 ${maxk}      pass     ${nt} 1   ${fp}   1 0 3 s ${klen} ${vlen}\
      \
  | tee "${OUTDIR}"/"${out1}"
}

case $1 in
rdb)
  sys=('rdb' "$basedir/rdb" '16384')
  ;;
fdb)
  sys=('flexdb' "$basedir/fdb" '16384')
  ;;
kvell)
  sys=('kvell' "$basedir/kvell" '1' '4' '20' '64')
  if [ "$2" == "zippydb" ]
  then
      sys=('kvell' "$basedir/kvell" '1' '4' '4' '64')
  elif [ "$2" == "sys" ]
  then
      sys=('kvell' "$basedir/kvell" '1' '4' '50' '64')
  fi
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

make -B O=rg dbtest1.out ROCKSDB=y LEVELDB=y KVELL=y M=j

s=$1
nt=$3
rm -rf ${sys[1]}

runit ${run}

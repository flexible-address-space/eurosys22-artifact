#!/bin/bash

source ./scripts/common.sh

OUTDIR="results/flexdb/latency/"

mkdir -p "${OUTDIR}"

runit-get()
{
  local fill=${1}
  local maxk=$((${fill} - 1))
  local fp=$((${fill} / ${nt} - 1))

  local out1="${s}-latency-get-${d[0]}"
  local vlen=${d[2]}
  local klen=${d[1]}
  local scan="50"

  numactl -N 0 --preferred=0 \
    ./dbcdf.out api ${sys[@]} \
      rgen incu    0 ${maxk}      pass ${nt} 1   ${maxk} 1 0 3 S ${klen} ${vlen}\
      rgen zipfian 0 ${maxk}      pass ${nt} 0        60 1 0 3 g ${klen} ${vlen} \
      | tee "${OUTDIR}"/"${out1}"
}

runit-set()
{
  local fill=${1}
  local maxk=$((${fill} - 1))
  local fp=$((${fill} / ${nt} - 1))

  local out1="${s}-latency-set-${d[0]}"
  local vlen=${d[2]}
  local klen=${d[1]}
  local scan="50"

  numactl -N 0 --preferred=0 \
    ./dbcdf.out api ${sys[@]} \
      rgen zipfian 0 ${maxk}      pass     ${nt} 1   ${fp} 1 0 3 s ${klen} ${vlen}\
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
  sys=('kvelll' "$basedir/kvell" '1' '4' '20' '64')
  if [ "$2" == "zippydb" ]
  then
      sys=('kvelll' "$basedir/kvell" '1' '4' '4' '64')
  elif [ "$2" == "sys" ]
  then
      sys=('kvelll' "$basedir/kvell" '1' '4' '50' '64')
  fi
  ;;
kvell1)
  sys=('kvelll' "$basedir/kvell" '1' '4' '20' '1')
  if [ "$2" == "zippydb" ]
  then
      sys=('kvelll' "$basedir/kvell" '1' '4' '4' '1')
  elif [ "$2" == "sys" ]
  then
      sys=('kvelll' "$basedir/kvell" '1' '4' '50' '1')
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
make -B O=rg dbcdf.out ROCKSDB=y LEVELDB=y KVELL=y M=j

s=$1
nt=4
rm -rf ${sys[1]}

case $3 in
set)
    runit-set ${run}
    ;;
get)
    runit-get ${run}
    ;;
*)
    exit 0
    ;;
esac

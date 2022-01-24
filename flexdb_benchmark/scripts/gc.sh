#!/bin/bash

source ./scripts/common.sh

OUTDIR="results/flexdb/gc/"

mkdir -p "${OUTDIR}"

runit-zipf()
{
  local fill=${1}
  local maxk=$((${fill} - 1))
  local fp=$((${fill} / ${nt} - 1))

  local out1="${s}-gc-zipf-${d[0]}-${maxoff[0]}"
  local vlen=${d[2]}
  local klen=${d[1]}
  local scan="50"

  sudo smartctl -a /dev/nvme1n1 | tee "${OUTDIR}"/"${out1}"-smart-before
  numactl -N 0 --preferred=0 \
    ./dbtest1.out api ${sys[@]} \
      rgen incu    0 ${maxk}      pass 4 1 ${maxk} 1 0 3 S ${klen} ${vlen}\
      rgen zipfian 0 ${maxk}      pass 4 1 100000000 1 0 3 s ${klen} ${vlen}\
  | tee "${OUTDIR}"/"${out1}"
  sudo smartctl -a /dev/nvme1n1 | tee "${OUTDIR}"/"${out1}"-smart-after
}

runit-czipf()
{
  local fill=${1}
  local maxk=$((${fill} - 1))
  local fp=$((${fill} / ${nt} - 1))

  local out1="${s}-gc-czipf-${d[0]}-${maxoff[0]}"
  local vlen=${d[2]}
  local klen=${d[1]}
  local scan="50"

  sudo smartctl -a /dev/nvme1n1 | tee "${OUTDIR}"/"${out1}"-smart-before
  numactl -N 0 --preferred=0 \
    ./dbtest1.out api ${sys[@]} \
      rgen incu    0 ${maxk}      pass 4 1 ${maxk} 1 0 3 S ${klen} ${vlen}\
      rgen zipfuni 0 ${maxk} 1000 pass 4 1 100000000 1 0 3 s ${klen} ${vlen}\
  | tee "${OUTDIR}"/"${out1}"
  sudo smartctl -a /dev/nvme1n1 | tee "${OUTDIR}"/"${out1}"-smart-after
}

case $1 in
fdb)
  sys=('flexdb' "$basedir/fdb" '16384')
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

s=$1
nt=4
rm -rf ${sys[1]}

case $4 in
128g)
    maxoff=(128g 137438953472lu)
    ;;
75g)
    maxoff=(75g 80530636800lu)
    ;;
*)
    exit 0
    ;;
esac

make -B O=rg dbtest1.out M=j MAX_OFF=${maxoff[1]}

case $3 in
zipf)
    runit-zipf ${run}
    ;;
czipf)
    runit-czipf ${run}
    ;;
*)
    exit 0
    ;;
esac

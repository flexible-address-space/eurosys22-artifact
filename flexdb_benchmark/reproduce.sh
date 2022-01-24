#!/bin/bash

# Fig 11(a) and 11(b) - Write and WA
function flexdb_write {
    for s in fdb rdb kvell
    do
        for d in zippydb udb sys
        do
            for w in seq zipf czipf
            do
                ./scripts/write.sh $s $d $w
                sleep 30
            done
        done
    done
}

# Fig 11(c) and 11(d) - Point query and range query
function flexdb_read {
    for s in fdb rdb kvell
    do
        for d in zippydb udb sys
        do
            ./scripts/read.sh $s $d
            sleep 30
        done
    done
}

# Fig 11(e) - Write scalability
function flexdb_scale_write {
    for s in fdb rdb kvell
    do
        for d in udb
        do
            for t in 1 2 3 4 5 6 7 8
            do
                ./scripts/scale-write.sh $s $d $t
                sleep 30
            done
        done
    done
}

# Fig 11(e) - Read scalability
function flexdb_scale_read {
    for s in fdb rdb kvell
    do
        for d in udb
        do
            ./scripts/scale.sh $s $d
            sleep 30
        done
    done
}

# Fig 11(f)
function flexdb_gc {
    ./scripts/gc.sh fdb udb zipf 128g
    ./scripts/gc.sh fdb udb zipf 75g
    ./scripts/gc.sh fdb udb czipf 128g
    ./scripts/gc.sh fdb udb czipf 75g
}

# Table 4 - Latency
function flexdb_latency {
    for s in fdb rdb kvell kvell1
    do
        for d in udb
        do
            ./scripts/latency.sh $s $d set
            sleep 30
            ./scripts/latency.sh $s $d get
            sleep 30
        done
    done
}

# Figure 12(a) - YCSB
function flexdb_ycsb {
    for s in fdb rdb kvell
    do
        for d in udb
        do
            ./scripts/ycsb.sh $s $d
            sleep 30
        done
    done
}

# Figure 12(b) - YCSB out-of-core
function flexdb_ycsb_oc {
    for s in fdb rdb
    do
        for d in udb
        do
            ./scripts/ycsb-oc.sh $s $d
            sleep 30
        done
    done
}

flexdb_write
flexdb_read
flexdb_scale_write
flexdb_scale_read
flexdb_gc
flexdb_latency
flexdb_ycsb
flexdb_ycsb_oc

#!/usr/bin/python3
import sys
import matplotlib
import matplotlib.pyplot as plt

targets = (
    "flexfile",
    "xfs",
    "ext4",
    "f2fs",
    "btrfs",
    )

exps = (
    ("insert", "randw", "seqw"),
    ("insert_seqr_cold", "randw_seqr_cold", "seqw_seqr_cold"),
    ("insert_randr_cold", "randw_randr_cold", "seqw_randr_cold"),
    ("insert_seqr_warm", "randw_seqr_warm", "seqw_seqr_warm"),
    ("insert_randr_warm", "randw_randr_warm", "seqw_randr_warm"),
)

for i in exps:
    t = []
    for j in i:
        for k in targets:
            if "insert" in j and (k == "f2fs" or k == "btrfs"):
                continue
            c = 0
            s = 0
            with open("_".join([k, j]), "r") as f:
                f.readline()
                r = f.readline()
                r = r.split()[0]
                t.append(float(r) / 1e3)
    print(" & ".join(["{:.2f}".format(x) for x in t]))

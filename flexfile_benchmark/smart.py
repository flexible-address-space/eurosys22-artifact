#!/usr/bin/python3
import sys

targets = (
    "flexfile",
    "xfs",
    "ext4",
    "f2fs",
    "btrfs",
)

exps = (
    "insert",
    "randw",
    "seqw",
)

base = 1

y = []
for j in exps:
    for i in targets:
        if j == "insert" and (i == "f2fs" or i == "btrfs"):
            continue
        b = 0
        a = 0
        with open("_".join([i, j, "smart_before"]), "r") as f:
            for l in f.readlines():
                if "Data Units Written" in l:
                    b = int(l.strip().replace(" ", "").replace(",", "")[17:27])
                    b = b / 2 / 1024
        with open("_".join([i, j, "smart_after"]), "r") as f:
            for l in f.readlines():
                if "Data Units Written" in l:
                    a = int(l.strip().replace(" ", "").replace(",", "")[17:27])
                    a = a / 2 / 1024
        y.append((a-b)/base)

print(" & ".join(["{:.2f}".format(x) for x in y]))

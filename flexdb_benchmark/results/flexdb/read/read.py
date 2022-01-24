#!/usr/bin/python3
import sys
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'Noto Serif'
fig = plt.figure(constrained_layout=True, figsize=(5, 2.5))
fontsize = 15
ticksize = 12
barwidth=0.25

targets = (
    ("rdb", "RocksDB", "\\\\\\", "#add8e6"),
    ("kvell", "KVell", "///", "#bbbbbb"),
    ("fdb", "FDB", "", "coral"),
)

sizes = (
    ("zippydb", "ZippyDB"),
    ("udb", "UDB"),
    ("sys", "SYS"),
)

exps = (
    ("seq", "S"),
    ("zipf", "Z"),
    ("czipf", "C"),
)


#gs = fig.add_gridspec(1, len(exps))
#ax = [fig.add_subplot(gs[:, i:(i+1)]) for i in range(len(exps))]
nplots = len(sizes)
gs = fig.add_gridspec(1, nplots)
ax = [fig.add_subplot(gs[:, i:i+1]) for i in range(nplots)]

for j in range(len(sizes)):
    s = sizes[j]
    for i in range(len(targets)):
        t = targets[i]
        y = []
        xticklabels = []
        name = "-".join([t[0], "read", s[0]])
        with open(name, "r") as f:
            for _ in range(4):
                f.readline()
            for e in exps:
                l = f.readline()
                l = f.readline()
                a = l.strip().split()
                idx = a.index("avg")
                y.append(float(a[idx+1]))
                xticklabels.append(e[1])
        ax[j].bar([m + (i - len(targets)/2+0.5) * barwidth for m in range(1, len(y)+1)], y,
                label=t[1], width=barwidth, linewidth=1, hatch=t[2], edgecolor='black',
                zorder=3, color=t[3])
        print(y)
    ax[j].grid(True, axis="y", linestyle="--", lw=0.5, color="#666666", zorder=0)
    ax[j].set_ylim(0, 4)
    ax[j].set_xticks(list(range(1, len(y)+1)))
    ax[j].set_xticklabels([_ll for _ll in xticklabels], rotation=0)
    ax[j].tick_params(labelsize=ticksize)
    ax[j].set_title(s[1], fontsize=fontsize)
    if j == 1:
        ax[j].set_xlabel("Key Distribution", fontsize=fontsize)
    if j == 0:
        ax[j].set_ylabel("Throughput (Mops/sec)", fontsize=fontsize)
    else:
        ax[j].set_yticklabels([])

handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', fontsize=fontsize, ncol=3, bbox_to_anchor=(0.545, 1.18), handletextpad=0.4, borderpad=0.25, columnspacing=1.8)
# plot
fig.savefig("flexdb-read.pdf", bbox_inches="tight", pad_inches=0.03, format='pdf')
plt.close(fig)

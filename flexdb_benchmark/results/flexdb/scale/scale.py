#!/usr/bin/python3
import sys
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'Noto Serif'
fig = plt.figure(constrained_layout=True, figsize=(6, 2.5))
fontsize = 15
ticksize = 12
barwidth=0.35

targets = (
    ("rdb", "RocksDB", "x", "steelblue", "--"),
    ("kvell", "KVell", ".", "grey", "-."),
    ("fdb", "FDB", "*", "coral", "-"),
)

sizes = (
    ("udb", "UDB"),
)

nthreads = list(range(1, 9))
print(nthreads)

#gs = fig.add_gridspec(1, len(exps))
#ax = [fig.add_subplot(gs[:, i:(i+1)]) for i in range(len(exps))]
nplots = 3
gs = fig.add_gridspec(1, nplots)
ax = [fig.add_subplot(gs[:, i:i+1]) for i in range(nplots)]

for i in range(len(targets)):
    t = targets[i]
    y = []
    s = sizes[0]
    for n in nthreads:
        name = "-".join([t[0], "scale-write", s[0], str(n)])
        with open(name, "r") as f:
            l = f.readline()
            a = l.strip().split()
            idx = a.index("avg")
            y.append(float(a[idx+1]))
            ax[0].plot(y, label=t[1], zorder=3, linewidth=1.75, marker=t[2], color=t[3], linestyle=t[4], markersize=6)
    print(y)
    y = []
    name = "-".join([t[0], "scale", s[0]])
    with open(name, "r") as f:
        for _ in range(4):
            f.readline()
        for n in nthreads:
            l = f.readline()
            l = f.readline()
            a = l.strip().split()
            idx = a.index("avg")
            y.append(float(a[idx+1]))
        ax[1].plot(y, label=t[1], zorder=3, linewidth=1.75, marker=t[2], color=t[3], linestyle=t[4], markersize=6)
        print(y)
        y = []
        for n in nthreads:
            l = f.readline()
            l = f.readline()
            a = l.strip().split()
            idx = a.index("avg")
            y.append(float(a[idx+1]))
        ax[2].plot(y, label=t[1], zorder=3, linewidth=1.75, marker=t[2], color=t[3], linestyle=t[4], markersize=6)
        print(y)

    ax[0].grid(True, axis="both", linestyle="--", lw=0.5, color="#666666", zorder=0)
    ax[1].grid(True, axis="both", linestyle="--", lw=0.5, color="#666666", zorder=0)
    ax[2].grid(True, axis="both", linestyle="--", lw=0.5, color="#666666", zorder=0)
    ax[0].set_ylim(0, 1.0)
    ax[0].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[1].set_ylim(0, 2.6)
    ax[1].set_yticks([0, 0.5, 1, 1.5, 2, 2.5])
    ax[2].set_ylim(0, 0.55)
    ax[2].set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax[0].set_xticks(list(range(0, len(y))))
    ax[0].set_xticklabels([str(_ll) for _ll in nthreads], rotation=0)
    ax[0].tick_params(labelsize=ticksize)
    ax[0].set_title("SET", fontsize=fontsize)
    ax[1].set_xticks(list(range(0, len(y))))
    ax[1].set_xticklabels([str(_ll) for _ll in nthreads], rotation=0)
    ax[1].tick_params(labelsize=ticksize)
    ax[1].set_title("GET", fontsize=fontsize)
    ax[2].set_xticks(list(range(0, len(y))))
    ax[2].set_xticklabels([str(_ll) for _ll in nthreads], rotation=0)
    ax[2].tick_params(labelsize=ticksize)
    ax[2].set_title("SCAN50", fontsize=fontsize)

    #if j == 1:
    ax[0].set_xlabel("# of Threads", fontsize=fontsize)
    ax[1].set_xlabel("# of Threads", fontsize=fontsize)
    ax[2].set_xlabel("# of Threads", fontsize=fontsize)
    #if j == 0:
    ax[0].set_ylabel("Throughput (Mops/sec)", fontsize=fontsize)
    #else:
    #ax[1].set_yticklabels([])

#fig.text(0.55, -0.06, "Number of Threads", fontsize=fontsize, ha="center")

handles, labels = ax[1].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', fontsize=fontsize, ncol=3, bbox_to_anchor=(0.545, 1.18), handletextpad=0.4, borderpad=0.25, columnspacing=1.8)
# plot
fig.savefig("flexdb-scale.pdf", bbox_inches="tight", pad_inches=0.03, format='pdf')
plt.close(fig)

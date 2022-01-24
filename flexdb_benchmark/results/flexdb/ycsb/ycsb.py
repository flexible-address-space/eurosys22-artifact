#!/usr/bin/python3
import sys
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'Noto Serif'
fig = plt.figure(constrained_layout=True, figsize=(4.25, 2.65))
fontsize = 15
ticksize = 12
barwidth= 0.25

targets = (
    ("fdb", "FlexDB", "", "coral"),
    ("kvell", "KVell", "///", "#bbbbbb"),
    ("rdb", "RocksDB", "\\\\\\", "#add8e6"),
)

sizes = (
    ("udb", "UDB"),
)

workloads = ("A", "B", "C", "D", "E", "F")


celltext = (
    ("100%", "0%",  "0%",  "0%",   "5%",  "5%",  "0%"),
    ("0%",   "50%", "5%",  "0%",   "0%",  "0%",  "0%"),
    ("0%",   "50%", "95%", "100%", "95%", "0%",  "50%"),
    ("0%",   "0%",  "0%",  "0%",   "0%",  "95%", "0%"),
    ("0%",   "0%",  "0%",  "0%",   "0%",  "0%",  "50%"),
)

cellcolor = (
    ("#e0ffdd", "#fff", "#fff", "#fff", "#e0ffdd", "#e0ffdd", "#fff"),
    ("#fff", "#e0ffdd", "#e0ffdd", "#fff", "#fff", "#fff", "#fff"),
    ("#fff", "#e0ffdd", "#e0ffdd", "#e0ffdd", "#e0ffdd", "#fff", "#e0ffdd"),
    ("#fff", "#fff", "#fff", "#fff", "#fff", "#e0ffdd", "#fff"),
    ("#fff", "#fff", "#fff", "#fff", "#fff", "#fff", "#e0ffdd"),
)

#gs = fig.add_gridspec(1, len(exps))
#ax = [fig.add_subplot(gs[:, i:(i+1)]) for i in range(len(exps))]
gs = fig.add_gridspec(1, 1)
ax = fig.add_subplot(gs[:, :])

baseline = []

for j in range(len(sizes)):
    s = sizes[j]
    for i in range(len(targets)):
        t = targets[i]
        y = []
        name = "-".join([t[0], "ycsb", s[0]])
        with open(name, "r") as f:
            f.readline()
            f.readline()
            for m in range(len(workloads)):
                l = f.readline()
                l = f.readline()
                a = l.strip().split()
                idx = a.index("avg")
                y.append(float(a[idx+1])*1)
        print(y)
        if t[0] == "fdb":
            baseline = [_y for _y in y]
            baseline[3] = 3.8581
        y = [y[_i] / baseline[_i] for _i in range(len(baseline))]
        ax.bar([m - (i - len(targets)/2+0.5) * barwidth for m in range(1, len(y)+1)], y,
                label=t[1], width=barwidth, linewidth=1, hatch=t[2], edgecolor='black',
                zorder=2, color=t[3])
        if t[0] == "fdb":
            for _p in range(len(ax.patches)):
                p = ax.patches[_p]
                if (_p == 3 or _p == 2 or _p == 1):
                    ax.annotate("{:.2f}".format(baseline[_p])+"M", (p.get_x()-0.385, 1.05), fontsize=fontsize-2)
                else:
                    ax.annotate("{:.0f}".format(baseline[_p]*1e3)+"K", (p.get_x()-0.385, 1.05), fontsize=fontsize-2)


    #ax.text(x=5, y=3.65, s="8.6X", fontsize=fontsize-1, color="darkgreen")
    ax.grid(True, axis="y", linestyle="--", lw=0.5, color="#666666", zorder=0)
    ax.set_ylim(0, 1.2)
    ax.set_xlim(0.5, 6.5)
    ax.set_yticks([0.2 * i for i in range(6)])
    ax.set_yticklabels(["0", "20", "40", "60", "80", "100"])
    ax.set_xticks(list(range(1, 7)))
    ax.set_xticklabels(workloads)
    ax.tick_params(labelsize=ticksize)
    ax.set_title("YCSB Test (UDB, czipf, 100M keys)", fontsize=fontsize)
    ax.set_title("  ", fontsize=fontsize)
    ax.set_xlabel("Workload", fontsize=fontsize)
    ax.set_ylabel("Throughput (%)", fontsize=fontsize)
    #ax.table(cellText=celltext, rowLabels=["insert", "update", "read", "scan", "rmw"], colLabels=workloads, loc="bottom", cellLoc="center", bbox=[0,-0.66,1,0.66], edges="closed", cellColours=cellcolor)

handles, labels = ax.get_legend_handles_labels()
handles = handles[::-1][:2]
labels = labels[::-1][:2]
fig.legend(handles, labels, loc='upper center', fontsize=fontsize, ncol=3, bbox_to_anchor=(0.65, 1.08), handletextpad=0.4, borderpad=0.25, columnspacing=1.8)
# plot
fig.savefig("flexdb-ycsb.pdf", bbox_inches="tight", pad_inches=0.03, format='pdf')
plt.close(fig)

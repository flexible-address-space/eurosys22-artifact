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
        xticklabels = []
        y = []
        for k in range(len(exps)):
            a = 0
            b = 0
            e = exps[k]
            name = "-".join([t[0], "write", e[0], s[0], "smart-before"])
            with open(name, "r") as f:
                for l in f.readlines():
                    if "Data Units Written" in l:
                        b = int(l.strip().replace(" ", "").replace(",", "")[17:27])
                        b = b / 2 / 1024
                        break
            name = "-".join([t[0], "write", e[0], s[0], "smart-after"])
            with open(name, "r") as f:
                for l in f.readlines():
                    if "Data Units Written" in l:
                        a = int(l.strip().replace(" ", "").replace(",", "")[17:27])
                        a = a / 2 / 1024
                        break
            xticklabels.append(e[1])
            y.append(a-b)
        print(t[1], y)
        #xticklabels.append("\n\n" + s[0])
        ax[j].bar([m + (i - len(targets)/2+0.5) * barwidth for m in range(1, len(y)+1)], y,
                label=t[1], width=barwidth, linewidth=1, hatch=t[2], edgecolor='black',
                zorder=2, color=t[3])
        if t[0] == 'kvell' and j < 2:
            yyy = 490
            ax[j].annotate("{:.0f}".format(y[1]), xy=(2-barwidth/2-0.05, yyy),  xycoords='data',
                    xytext=(0.35, 0.95), textcoords='axes fraction',
                    arrowprops=dict(facecolor='black', width=0.2, headwidth=2, headlength=3),
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=12
                    )
            xytext=(0.83, 0.88)
            if y[2] > 1000:
                xytext=(0.86, 0.88)

            ax[j].annotate("{:.0f}".format(y[2]), xy=(3-barwidth/2-0.05, yyy),  xycoords='data',
                    xytext=xytext, textcoords='axes fraction',
                    arrowprops=dict(facecolor='black', width=0.2, headwidth=2, headlength=3),
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=12, bbox=dict(boxstyle="square,pad=0.1", fc="#eeeeee", ec='#666666')
                    )


    ax[j].set_title(s[1], fontsize=fontsize)
    ax[j].grid(True, axis="y", linestyle="--", lw=0.5, color="#666666", zorder=0)
    ax[j].set_ylim(0, 500)
    ax[j].set_yticks([0, 100, 200, 300, 400, 500])
    ax[j].set_xticks(list(range(1, len(y)+1)))
    ax[j].set_xticklabels([_ll for _ll in xticklabels], rotation=0)
    ax[j].tick_params(labelsize=ticksize)
    if j == 1:
        ax[j].set_xlabel("Key Distribution", fontsize=fontsize)
    if j == 0:
        ax[j].set_ylabel("Data Written (GB)", fontsize=fontsize)
    if j != 0:
        ax[j].set_yticklabels([])

handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', fontsize=fontsize, ncol=3, bbox_to_anchor=(0.545, 1.18), handletextpad=0.4, borderpad=0.25, columnspacing=1.8)
# plot
fig.savefig("flexdb-wa.pdf", bbox_inches="tight", pad_inches=0.03, format='pdf')
plt.close(fig)

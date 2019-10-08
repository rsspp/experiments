import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import pandas
from os import sys
from common import *
series = [ "Shared", "Group-table" ]
labels = [ "Shared", "Per-bucket" ]

shift = np.array([-10, 2, 14]) - 2
f = "migration-udp-cx5"


data_a_s = []
data_b_s = []
data_c_s = []
for s in series:
        c = pandas.read_csv(f + "/" + s + "DUTTHROUGHPUT.csv", header=None, engine="python",usecols=range(4),delim_whitespace=True)
        data_a_s.append(np.array(c))
        c = pandas.read_csv(f + "/" + s + "ILATENCY.csv", header=None, engine="python",usecols=range(4),delim_whitespace=True)
        data_b_s.append(np.array(c))
        c = pandas.read_csv(f + "/" + s + "NCPU.csv", header=None, engine="python",usecols=range(4),delim_whitespace=True)
        data_c_s.append(np.array(c))


fig, ax1 = plt.subplots()
fig.set_size_inches(6,3)

for i,data in enumerate(data_a_s):
    ax1.plot(data[:,0] + shift[0], [np.mean(l) for l in data[:,1]], label=labels[i], color = graphcolor[i], linestyle=linestyles[i % len(series)], marker='None')

ax1.set_ylabel('Throughput (Gbps)', color=darker(colors[0]))
ax1.set_xlabel('Time (s)')
ax1.set_ylim(0,100)
ax1.set_xlim(0,35)
ax1.tick_params(axis='y', labelcolor=darker(colors[0]))

ax2 = ax1.twinx()
ax2.set_ylabel("Latency (µs)", color=darker(colors[1]))
ax2.set_ylim(0,8000)
ax2.tick_params(axis='y', labelcolor=darker(colors[1]))
for i,data in enumerate(data_b_s):
    ax2.plot(data[:,0] + shift[1], [np.mean(l) for l in data[:,1]], label=labels[i], color = graphcolor[i + 2], linestyle=linestyles[i % len(series)], marker='None') #markers[ int(i / 2)]

yTickPos,_ = plt.yticks()
yTickPos = yTickPos[:-1]
data = data_c_s[1]
h=max([max(data_b[:,1]) for data_b in data_b_s])
h=8000
import pandas as pd

df = pd.DataFrame(data)
df = df.groupby(df.columns[1], as_index=False).first().reset_index()
df = df.sort_values(by=[df.columns[2]]).as_matrix()

#Background
t = np.asarray(df[:,2])
w = np.asarray(np.ediff1d([0] + t))
t=t[:-1]
b = ax2.bar((t + w / 2) - shift[2], height=h, width=w, color=[lighter(colors[2],.12,1),lighter(colors[2],.05,1)], zorder=-99999)

ax1.set_zorder(ax2.get_zorder()+1)
ax1.patch.set_visible(False)
for i, rect in enumerate(b):
    ax2.text(rect.get_x() + rect.get_width()/2, 0, '%d' % int(df[i,1]), ha='center', va='bottom', color=darker(colors[2]))
xy=(b[2].get_x() + b[2].get_width()/2, 8000/12)
ax2.annotate('# of cores',
            xy=xy, xycoords='data',
            xytext=(0.22,0.3), textcoords='axes fraction',
	    color = darker(colors[2]),
            arrowprops=dict(facecolor=darker(colors[2]), shrink=0.1,width=2,headwidth=4,headlength=4),
            horizontalalignment='center', verticalalignment='top')


leg = ax1.legend(loc="lower left", title="Throughput", bbox_to_anchor = (0, 1))
leg = ax2.legend(loc="lower right", title = "Latency", bbox_to_anchor = (1, 1), markerfirst=False)
#leg._legend_box.align = "right"
for vl in leg._legend_box.get_children():
    vl.align = "right"
#for l in leg.legendHandles:
#    l.set_color('black')

#ax1.set_xscale("log")
#ax1.set_ylim(2.5,4.5)
#ax1.set_yticks([2.5,3,3.5,4,4.5])
#ax1.set_xticks(4* np.asarray([pow(2,i) for i in range(11)]))
#ax1.set_xlim([4, 4096])
#ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
#ax1.minorticks_off()
#ax1.set_ylim([0, 25])

#ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#           ncol=3, mode="expand", borderaxespad=0.)

#lines = [Line2D([0], [0], color="black" ),
#         Line2D([0], [0], color="black", linestyle='--')]

#leg1 = plt.legend(lines, series, loc="lower left",  bbox_to_anchor=(0.0,1.0,0.45,1), title="Queue selection", mode="expand")



#lines = []

#for i in range(4):
#    lines.append(Line2D([0], [0], color=colors[i],marker=markers[i], linestyle=' '))

#plt.legend(lines, labels_t, loc="lower right",  bbox_to_anchor=(0.45,1.0,0.55,1), ncol=2, title="Per-flow action",mode="expand" )

#ax1.add_artist(leg1)
plt.tight_layout()

plt.savefig('migration.pdf')

plt.clf()

sys.exit(0)


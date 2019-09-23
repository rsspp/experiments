import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
from common import *

series = ["kthmorning-cx5/RSS" ,  "kthmorning-cx5/RSSPP", "kthmorning-cx5/Metron" ]
labels = ["RSS","RSS++","Metron"]
colors = [c_rss, c_rsspp, c_metron]
shift = [0,0,0]

throughputs = []
latencys = []
for s in series:
    throughputs.append(np.genfromtxt(s + "ITHROUGHPUT.csv"))
    latencys.append(np.genfromtxt(s + "NCPU.csv"))


fig, ax1 = plt.subplots()
fig.set_size_inches(6,3)

for i,throughput in enumerate(throughputs):
    ax1.plot(throughput[:,0] - min(throughput[:,0]) - shift[i], throughput[:,1], label=labels[i], color = colors[i])

ax1.set_ylabel('Throughput (Gbps)')
ax1.set_xlabel('Time (s)')
ax1.set_xlim([0, 60])
ax1.set_ylim([0, 25])

ax2 = ax1.twinx()
ax2.set_ylabel('# of CPUs')

tlinestyles = ['-.','--',':']

for i,latency in enumerate(latencys):
    if i == 0:
        m = max(latency[:,1])
        latency = np.array([[0,m],[60,m]])
    print("Average CPU of %s : %.01f" % (labels[i],np.mean(latency[:60,1])))
    ax2.plot(latency[:,0] - min(latency[:,0]) - shift[i], latency[:,1], linestyle=tlinestyles[i], drawstyle='steps',color=colors[i],label=labels[i])

ax2.set_ylim([0, 16])
ax2.yaxis.set_major_locator(ticker.MultipleLocator(2.00))
ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

artist = ax1.legend(loc="lower left", title="Throughput", bbox_to_anchor = (0.18,0))
artist.remove()
artist.set_zorder(9999)

#ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#           ncol=3, mode="expand", borderaxespad=0.)

#lines = [Line2D([0], [0], color="black" ),
#                  Line2D([0], [0], color="black", linestyle=':')]
#
#ax2.legend(lines, ["Throughput", "CPUs"], loc="upper right",  bbox_to_anchor=(1.0,0.9) )

ax2.legend(loc="upper right", title="# of CPUs", bbox_to_anchor=(1,0.9))
#,  bbox_to_anchor=(1.0,0.9) )

ax2.add_artist(artist)
plt.tight_layout()

plt.savefig('dynamicscale.pdf')

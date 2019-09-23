import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import pandas

graphcolor = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
              (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
              (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
              (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
              (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
series = [ "Sprayer", "RSS" ]
series_t = [ "WPF__No_-_SERIE__", "WPF__Read_-_SERIE__", "WPF__Write_-_SERIE__", "WPF__Sequential_write_-_SERIE__" ]
labels = ["Sprayer","RSS"]
labels_t = ["None","Read","Write","Sequential write"]

colors = []
for i in range(int(len(graphcolor) / 2)):
    colors.append((np.asarray(graphcolor[i*2]) + np.asarray(graphcolor[i*2+1])) / 2)

#colors = [(97,146,187),(230,141,60),(88,172,82)]


graphcolor = [(c1/255.0,c2/255.0,c3/255.0) for c1,c2,c3 in graphcolor]
colors = [(c1/255.0,c2/255.0,c3/255.0) for c1,c2,c3 in colors]
shift = [0,0,0]
markers=['o', '^', 's', 'D', '*', 'x', '.', '_', 'H', '>', '<', 'v', 'd']
linestyles = ['-', '--', '-.', ':']

ooos= []
cycles = []
for s in series_t:
    for t in series:
        c = pandas.read_csv("shared-udp-cx5/" + s  + t + "OUTOFORDERPC.csv", header=None,engine="python",usecols=range(4),delim_whitespace=True)
        ooos.append(np.array(c))
        c = pandas.read_csv("shared-udp-cx5/" + s  + t + "KCYCLESPP.csv", header=None,engine="python",usecols=range(4),delim_whitespace=True)
        cycles.append(np.array(c))

prop = 8
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [prop, 1],"wspace":None,"hspace":0.1,"bottom":0.15,"top":0.75,"left":0.1,"right":0.95}, constrained_layout=False )

#fig, ax1 = plt.subplots()
fig.set_size_inches(6,3.5)

for i,data in enumerate(cycles):
    ax1.plot(data[:,0] * 4, [np.mean(l) for l in data[:,1]], label=None, color = graphcolor[i], linestyle=linestyles[i % len(series)], marker=markers[ int(i / 2)])
ax1.set_ylabel('KCycles per packets')
ax2.set_xlabel('Number of flows')
ax1.set_xscale("log")
ax1.set_ylim(2.4,4.5)
ax2.set_ylim(0,(4.5-2.5)/prop)
ax1.set_yticks([2.5,3,3.5,4,4.5])
ax2.set_yticks([0])
ax2.set_xticks(4* np.asarray([pow(2,i) for i in range(11)]))
ax2.set_xlim(4, 4096)
ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
ax2.minorticks_off()


ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False,labelbottom=False,bottom=False,top=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()


#ax1.set_ylim([0, 25])

#ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#           ncol=3, mode="expand", borderaxespad=0.)

lines = [Line2D([0], [0], color="black" ),
         Line2D([0], [0], color="black", linestyle='--')]

artist = ax1.legend(lines, series, loc="lower left",  bbox_to_anchor=(0.0,1.0,0.45,1), title="Queue selection", mode="expand")

lines = []

for i in range(4):
    lines.append(Line2D([0], [0], color=colors[i],marker=markers[i], linestyle=' '))

ax1.legend(lines, labels_t, loc="lower right",  bbox_to_anchor=(0.45,1.0,0.55,1), ncol=2, title="Per-flow action",mode="expand" )

ax1.add_artist(artist)

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d * prop, 1 + d * prop), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d * prop, 1 + d * prop), **kwargs)  # bottom-right diagonal

ax1.grid(True,axis="y")
#plt.tight_layout()

plt.savefig('shared.pdf')

plt.clf()

fig, ax1 = plt.subplots()
fig.set_size_inches(6,2.5)

for i,data in enumerate(ooos):
    ax1.plot(data[:,0] * 4, [np.mean(l) for l in data[:,1] * 100], label=None, color = graphcolor[i], linestyle=linestyles[i % len(series)], marker=markers[ int(i / 2)])

ax1.set_ylabel('Out of order packets (%)')
ax1.set_xlabel('Number of flows')
ax1.set_ylim(0,30)
ax1.set_xscale("log")
ax1.set_xticks(4* np.asarray([pow(2,i) for i in range(11)]))
ax1.set_xlim(4, 4096)
ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
ax1.minorticks_off()

ax1.grid(True,axis="y")

plt.tight_layout()
plt.savefig('shared-ooos.pdf')


from common import *
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import pandas
from math import ceil

n_results=10

series = [ "Sprayer", "RSS" ]
series_t = [ "WPF__No_-_SERIE__", "WPF__Read_-_SERIE__", "WPF__Write_-_SERIE__", "WPF__Sequential_write_-_SERIE__" ]
labels = ["Sprayer","RSS"]
labels_t = ["None","Read","Write","Sequential write"]

#colors = [(97,146,187),(230,141,60),(88,172,82)]


shift = [0,0,0]

ooos= []
cycles = []
for s in series_t:
    for t in series:
        try:
            c = pandas.read_csv("shared-udp-cx5/" + s  + t + "OUTOFORDERPC.csv", header=None,engine="python",usecols=range(1 + n_results),delim_whitespace=True)
            ooos.append(np.array(c))
            c = pandas.read_csv("shared-udp-cx5/" + s  + t + "KCYCLESPP.csv", header=None,engine="python",usecols=range(1 + n_results),delim_whitespace=True)
            cycles.append(np.array(c))
        except Exception as e:
            print(e)

prop = 8
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [prop, 1],"wspace":None,"hspace":0.1,"bottom":0.15,"top":0.75,"left":0.1,"right":0.95}) #constrained_layout=False )

#fig, ax1 = plt.subplots()
fig.set_size_inches(6,3.5)

for i,data in enumerate(cycles):
    ax1.plot(data[:,0] * 4, [np.nanmean(l) for l in data[:,1:]], label=None, color = graphcolor[i], linestyle=linestyles[i % len(series)], marker=markers[ int(i / 2)], markerfacecolor=make_alpha(graphcolor[i],0.1),markeredgecolor=graphcolor[i])
ax1.set_ylabel('Cycles per packets X1000')
ax2.set_xlabel('Number of flows')
ax1.set_xscale("log")
ax1.set_ylim(2.4,ceil(np.nanmax(data[:,1:])))
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
    lines.append(Line2D([0], [0], color=colors[i],marker=markers[i], markerfacecolor=make_alpha(colors[i],0.1),markeredgecolor=colors[i], linestyle=' '))

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

print("Saving to shared.pdf")
plt.savefig('shared.pdf')

plt.clf()

fig, ax1 = plt.subplots()
fig.set_size_inches(6,2.5)

for i,data in enumerate(ooos):
    ax1.plot(data[:,0] * 4, [np.mean(l) for l in data[:,1] * 100], label=None, color = graphcolor[i], linestyle=linestyles[i % len(series)], marker=markers[ int(i / 2)], markerfacecolor=make_alpha(graphcolor[i],0.1),markeredgecolor=graphcolor[i] )

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

print("Saving to shared-ooos.pdf")
plt.savefig('shared-ooos.pdf')


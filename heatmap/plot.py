from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import pandas

def lighter(c, p, n):
    n = n / 255.
    return tuple(a * p + (1-p) * n for a in c)


step = 10
tm = step * 3

                                #6 2.4
plt.rcParams["figure.figsize"] = (5,3)

colors = [(97,146,187),(230,141,60),(88,172,82)]
colors = [(c1/255.0,c2/255.0,c3/255.0) for c1,c2,c3 in colors]

cpus = []

for i in range(18):
    data = np.genfromtxt("results/CPU-%d.csv" % i)
    cpus.append(np.asarray(data)[:,1])

cpus = np.asarray(cpus)
im = plt.imshow(cpus[:,2:], vmin=0,vmax=100)

ax = plt.gca()

ax.set_ylabel("CPU Core ID");
ax.set_xlabel("Time (s)")
ax.set_xlim(-0.5,tm + 0.5)
ax.set_ylim(-0.5,17.5)
ax.set_yticks([0,3,5,7,9,11,13,15,17])

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x + 1)))

#ax.annotate('iPerf2 sharded', xy=(0, 1.1), xycoords='axes fraction', xytext=(0.33, 1.1),
#                    arrowprops=dict(arrowstyle="<->", color='b'))

def aarrow(t,start,end,y):
    if y == 17.5:
        prop = y / 18.0
    else:
        prop = (y / 18.0) * 3/2
    y = y * (18.4 / 17.5)
    m=start + (end - start) / 2
    half=(end - start) / 2
    plt.arrow(m,y-(0.2 * prop),half,0,clip_on=False, width=0.07 * prop, length_includes_head=True, head_width=0.5 * prop, shape="full", edgecolor=None, facecolor="black",overhang=0.2, head_length=1.5 * 0.5)

    plt.arrow(m,y- 0.2 * prop,-half,0,clip_on=False, width=0.07 * prop, length_includes_head=True, head_width=0.5 * prop, shape="full", edgecolor=None, facecolor="black", overhang=0.2, head_length=1.5 * 0.5)
    plt.text(m,y + 0.1 * prop,t, horizontalalignment='center',verticalalignment="bottom")

aarrow("RSS", 0,step,17.5)
aarrow("RSS++\n(Autoscale off)", step + 1,step*2,17.5)
aarrow("RSS++\n(Autoscale on)", step*2 + 1,step*3,17.5)

cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("CPU Load (%)", rotation=-90, va="bottom")
#cbar.ax.set_ylim(0,100)
plt.tight_layout()

plt.savefig('heatmap.pdf')

plt.clf()


dual=False

plt.rcParams["figure.figsize"] = (6,2.4)
fig, ax1 = plt.subplots()

#bw = np.genfromtxt("results-3/BW.csv")
#rtt = np.genfromtxt("results-3/RTT.csv")
#ax1 = plt.gca()
bw = pandas.read_csv("results/BW.csv", header=None, engine="python",delim_whitespace=True,index_col=False).to_numpy()
rtt = pandas.read_csv("results-3/RTT.csv", header=None, engine="python",delim_whitespace=True,index_col=False).to_numpy()

s=bw[:,0]
speed=bw[:,1] / 1000000000
ax1.set_xlabel('Time (s)')

time = rtt[:,0] - 2
rtts = rtt[:,1:]

if dual:
    ax1.set_ylim(0,100)
    ax1.set_ylabel('Bandwidth (Gbps)', color=darker(colors[0]))
    ax1.plot(s, speed, color=colors[0])
    ax1.tick_params(axis='y', labelcolor=darker(colors[0]))

    h=102
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
else:
    h = np.max(rtts) * (1.02 / 0.93)
    ax2 = ax1

print("Average BW : %d" % np.mean(speed))
aarrow("RSS", 0,step,h)
aarrow("RSS++\n(Autoscale off)", step + 1,2*step,h)
aarrow("RSS++\n(Autoscale on)", 2*step + 1,3*step,h)

if dual:
    rcolor = darker(colors[1])
else:
    rcolor = "black"

ax2.set_ylabel('RTT (µs)', color=rcolor)  # we already handled the x-label with ax1

rects = ax2.boxplot([data[~np.isnan(data)] for data in rtts],positions=time)
if dual:
    plt.setp(rects['boxes'], color = colors[1])
    plt.setp(rects['whiskers'], color = colors[1])
    plt.setp(rects['caps'], color = colors[1])
    plt.setp(rects['fliers'], color = colors[1])
    plt.setp(rects['medians'], color = lighter(colors[1],0.50,0))

    ax2.tick_params(axis='y', labelcolor=rcolor)
ax2.set_ylim(0)
ax2.set_xlim(-0.5,tm + 0.5)
t = np.arange(int(tm / 5) + 1) * 5

ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))

ax2.set_xticks(t)
plt.tight_layout()  # otherwise the right y-label is slightly clipped
plt.subplots_adjust(top=0.78)
print("RTT mean/std of RSS is ", np.nanmean(rtts[2:step -1 ]), np.nanstd(rtts[2:step -1]))
print("RTT mean/std of RSS++ is ", np.nanmean(rtts[step:2*step-1]), np.nanstd(rtts[step:2*step-1]))
rttmid = rtt[( rtt[:,0] > (step + int(step / 2) + 2)) & (rtt[:,0] < 2*step+ 2),1:]
rttem = rtt[ (rtt[:,0] > (step + (step *0.8) + 2)) & (rtt[:,0] < 2*step + 2),1:]
print("RTT mean/std of RSS++ (after %d sec) is " % (step *1.5), np.nanmean(rttmid), np.nanstd(rttmid))
print("RTT mean/std of RSS++ (after %d sec) is " % (step *1.9), np.nanmean(rttem), np.nanstd(rttem))
print("RTT mean/std of RSS++ auto is ", np.nanmean(rtts[2*step:,3*step]), np.nanstd(rtts[2*step:3*step]))

if dual:
    plt.savefig('rttbw.pdf')
else:
    plt.savefig('rtt.pdf')

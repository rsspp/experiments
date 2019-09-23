import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
from common import *
from math import log,pow
from study import *
import pandas

traces = ["kth", "kthmorningquad", "kthmorningsingle", "caida18"]


print("Plotting tail latency according to load")

for trace in traces:
    print("Reading trace %s" % trace)
    data_s = []
    th_s = []
    for serie in series:


        try:
            #latency-kth/RSSlatency-kth-LAT99.csv
            #data = np.genfromtxt("latency-%s/%sLAT95.csv" % (trace, serie))
            data = pandas.read_csv("latency-%s/%sLAT95.csv" % (trace, serie), header=None,engine="python",delim_whitespace=True, usecols=range(4), index_col=False)
            data = data.to_numpy()

            th = pandas.read_csv("latency-%s/%sTHROUGHPUT.csv" % (trace, serie), header=None,engine="python",delim_whitespace=True, usecols=range(4), index_col=False)
            th = th.to_numpy()
            #data = data[ (data[:,0] < 50) & (data[:,0] > 5) ]
            data_s.append(data)
            th_s.append(th)
        except Exception as e:
            print("While reading trace %s:" % trace)
            print(e)
            continue

    plt.clf()
    plt.rcParams["figure.figsize"] = (6,4.2)
    fig, ax1 = plt.subplots()

    ax2 = ax1

    #rcolor = darker(colors[1])
    #ax2.set_ylabel('Packets in queues', color=rcolor)  # we already handled the x-label with ax1

    ax2.set_ylabel('$95^{th}$ percentile latency (µs)')

    for i,data in enumerate(data_s):

        scolor = tcolors[i]
        X = data[:,0] / 1000000000
        med = np.nanmedian(data[:,1:],axis=1)

        th = [np.nanmean(th[1:]) for th in th_s[i]]
        f = th > X*0.95
        print(f)
        rects = ax2.plot(X[f], med[f], color=scolor,marker=tmarkers[i],label=labels[i])

        rects = ax2.plot(X[np.invert(f)], med[np.invert(f)], color=lighter(scolor,0.75,1),linestyle=':',marker=tmarkers[i], fillstyle='none')
        rects = ax2.fill_between(X, np.nanpercentile(data[:,1:],25,axis=1), np.nanpercentile(data[:,1:],75,axis=1), color=list(scolor) + [0.25])

   #t = np.arange(7) * 5
    ax2.set_xlim(-0.5,35.5)
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    ax2.set_xlabel("Offered load (Gbps)")

    plt.grid(True, axis="y")
    ax2.set_yscale("symlog")

    milog = int(log(max(32,ax2.get_ylim()[0]),2))
    mlog = int(log(ax2.get_ylim()[1],2)) +1
    ax2.set_ylim(pow(2,milog),pow(2,mlog))

    ax2.set_yticks([pow(2,e) for e in range(milog,mlog)])

    ax2.legend(ncol=3,bbox_to_anchor=(0.5,1),loc="lower center")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    name = 'latency-%s.pdf' % trace
    plt.savefig(name)
    print("Generated %s" % name)



plt.clf()



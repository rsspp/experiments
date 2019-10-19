from common import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
from math import log,pow
#from study import *
import pandas

traces = ["kthmorning"]


s=["RSS","Sprayer","RSSPP"]
t=["FW","FWNAT","FWNATDPI"]

labelss=["RSS", "Sprayer", "RSS++"]
labelst=["FW", "FW+NAT", "FW+NAT+DPI"]

exp_time=80

tcolors=[c_rss,c_sprayer,c_rsspp]
series=[]
labels=[]
tmarkers = ['o','^','d']

for it,te in enumerate(t):
    for i,se in enumerate(s):
        series.append("%s_%s" % (se,te))
        labels.append("%s %s" % (labelss[i],labelst[it]))
#nat-kthmorning-cx5/Sprayer_FWNATDPIITHROUGHPUT.csv

labels.append("Offered load (Gbps)")

txx = []

for trace in traces:
    print("Reading trace %s" % trace)
    data_s = []
    th_s = []
    for serie in series:
        try:
            #latency-kth/RSSlatency-kth-LAT99.csv
            #data = np.genfromtxt("latency-%s/%sLAT95.csv" % (trace, serie))
            data = pandas.read_csv("nat-%s-cx5/%sITHROUGHPUT.csv" % (trace, serie), header=None,engine="python",delim_whitespace=True, usecols=range(4), index_col=False)
            data = data.to_numpy()
            tx = pandas.read_csv("nat-%s-cx5/%sITX.csv" % (trace, serie), header=None,engine="python",delim_whitespace=True, usecols=range(4), index_col=False)
            tx = tx.to_numpy()
            txx.append(tx)
            #data[:,0] = tx[:,0]
            #th = pandas.read_csv("latency-%s/%sTX.csv" % (trace, serie), header=None,engine="python",delim_whitespace=True, usecols=range(4), index_col=False)
            #th = th.to_numpy()
            #data = data[ (data[:,0] < 50) & (data[:,0] > 5) ]
            data_s.append(data[ data[:,0] <= exp_time ])
            #th_s.append(th)
        except Exception as e:
            print("While reading trace %s:" % trace)
            print(e)
            continue

    max_th=max([np.nanmax(txd[:,1:]) for txd in txx]) / pow(10,9)

    data = pandas.read_csv("nat-%s-cx5/%sITX.csv" % (traces[0], series[0]), header=None,engine="python",delim_whitespace=True, usecols=range(4), index_col=False)
    thx = data.to_numpy()
    thx = thx[ thx[:,0] <= exp_time ]
    plt.clf()
    plt.rcParams["figure.figsize"] = (6,4)
    fig, ax1 = plt.subplots()

    ax2 = ax1

    #rcolor = darker(colors[1])
    #ax2.set_ylabel('Packets in queues', color=rcolor)  # we already handled the x-label with ax1

    ax2.set_ylabel('Throughput (Gbps)')
    ax2.set_ylim(0,max_th)
    for i,data in enumerate(data_s):

        scolor = tcolors[int(i % 3)]
        X = data[:,0]
        med = data[:,1] #np.nanmedian(data[:,1:],axis=1)

        #th = [np.nanmean(th[1:]) for th in th_s[i]]
        #f = th > X*0.95

        rects = ax2.plot(X, med, color=scolor,markevery=10, marker=tmarkers[int(i % 3)], linestyle=linestyles[int(i / 3)], label=labels[i])

   #t = np.arange(7) * 5
    ax2.set_xlim(-0.5,exp_time + 0.5)
    inter = int(exp_time/10)
    ticks=np.arange(10) * (inter + 1)
    ax2.set_xticks(ticks)
    ax2.set_xticklabels(["%d" % (t / 1000000000) for t in thx[:,1][np.arange(10) * inter]])
    #ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    ax2.set_xlabel("Offered load (Gbps)")

    plt.grid(True, axis="y")
    #ax2.set_yscale("symlog")

    #milog = int(log(max(32,ax2.get_ylim()[0]),2))
    #mlog = int(log(ax2.get_ylim()[1],2)) +1
    #ax2.set_ylim(pow(2,milog),pow(2,mlog))

    #ax2.set_yticks([pow(2,e) for e in range(milog,mlog)])

    ax2.legend(ncol=3,bbox_to_anchor=(0.5,1),loc="lower center")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.subplots_adjust(top=0.80)
    name = 'nat-%s.pdf' % trace
    plt.savefig(name)

    print("Generated %s" % name)



plt.clf()



import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
from common import *
from math import log,pow
from study import *
traces = ["kth", "kthmorningquad", "kthmorningsingle", "caida18"]
traces = ["kthmorningquad"]
dolegend = True

print("Plotting tail latency according to load")
cores = range(1,16)
fill = False

for trace in traces:
    print("Reading trace %s" % trace)
    data_s = []
    for serie in series:


        data=[]
        for core in cores:

            try:
                d = np.genfromtxt("drop-%s/%s_-_Number_of_processing_cores__%dTHROUGHPUT.csv" % (trace, serie, core))
                data.append(np.array(d,ndmin=1))
                #data = data[ (data[:,0] < 50) & (data[:,0] > 5) ]
                #print(data)
            except Exception as e:
                data.append(np.asarray([]))
                print("While reading trace %s:" % trace)
                print(e)

        data_s.append(np.asarray(data))

    plt.clf()
    y=3.5
    if dolegend:
        y=4.2
    plt.rcParams["figure.figsize"] = (6,y)
    fig, ax1 = plt.subplots()

    ax2 = ax1

    #rcolor = darker(colors[1])
    #ax2.set_ylabel('Packets in queues', color=rcolor)  # we already handled the x-label with ax1

    ax2.set_ylabel('Throughput (Gbps)')

    for i,data in enumerate(data_s):

        scolor = tcolors[i]
        #X = data[:,0] #/ 1000000000
        X = cores
        Y = [np.median(d) if len(d) > 0 else np.nan for d in data]
        perc25 = [np.percentile(d,25) if len(d) > 0 else np.nan for d in data]
        perc75 = [np.percentile(d,75) if len(d) > 0 else np.nan for d in data]
        if fill:
            rects = ax2.plot(X, Y, color=scolor,marker=tmarkers[i],label=labels[i])
            rects = ax2.fill_between(X, perc25, perc75, color=list(scolor) + [0.25])
        else:
            rects = ax2.errorbar(X,Y,yerr=[np.std(d) if len(d) > 0 else np.nan for d in data], label=labels[i], color=scolor, marker=tmarkers[i])
   #t = np.arange(7) * 5
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    ax2.set_xlabel("Number of processing cores")

    plt.grid(True, axis="y")
    #ax2.set_yscale("symlog")
    #ax2.set_ylim(32,2048)
    ax2.set_ylim(0)
    #ax2.set_yticks([32,64,128,256,512,1024,2048])
    ax2.set_xlim(0.5)
    ax2.set_xticks(np.arange(int(max(cores)  / 2) + 1) * 2 + 1)
    if dolegend:
        ax2.legend(ncol=3,bbox_to_anchor=(0.5,1),loc="lower center")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig('throughput-%s.pdf' % trace)



plt.clf()



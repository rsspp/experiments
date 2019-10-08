from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import os
from matplotlib import container
from common import *
from collections import OrderedDict
from matplotlib.markers import MarkerStyle
from matplotlib.ticker import FormatStrFormatter

from matplotlib.ticker import FuncFormatter
import traceback

#################################################
#################################################

print("Plotting VSDROPPED")

traces = ["Campus", "Campus_4" ]
labels = ["Campus", "Campus #4"]
styles= ['-', ':']

for i,trace in enumerate(traces):
    count = pandaload("iter-count-nodiff/%sCOUNT.csv" % trace)
    print("Number of packet in %s : %d" % (trace, np.nanmedian(count)))
    cbytes = pandaload("iter-count-nodiff/%sBYTES.csv" % trace)
    print("Number of bytes in %s : %d" % (trace, np.nanmedian(cbytes)))
    print("Average packet size in %s : %f" % (trace, float(np.nanmedian(cbytes)) / np.nanmedian(count)))
    count = pandaload("iter-count-nodiff/%sTX.csv" % trace)
    print("TX in %s : %d" % (trace, np.nanmedian(count)))
    count = pandaload("iter-count-nodiff/%sCOUNTN.csv" % trace)
    print("Number of flows in %s : %d" % (trace, np.nanmedian(count[-1,1])))
    print("")

try:
    start = 4
    plt.rcParams["figure.figsize"] = (6,3)
    fig, ax1 = plt.subplots()

    for i,trace in enumerate(traces):
        nflows = pandaload("iter-count-diff/%sNFLOWS.csv" % trace)
        print("Average number of active flows : ", np.mean(nflows[10:60,1]))

        ax1.plot(nflows[:,0] - start,nflows[:,1]/1000, label=labels[i]) #marker=markers[si]  #facecolors=[scolor,'none'][i])

    ax1.legend(loc="lower right", bbox_to_anchor=(0.5,1.02), ncol=2, title="Active flows")
    ax2 = ax1.twinx()

    for i,trace in enumerate(traces):
        newflows = pandaload("iter-count-diff/%sNEWFLOWS.csv" % trace)
        print("Average number of new flows : ", np.mean(newflows[10:60,1]))
#        ax1.scatter(x, y, label=label, color=scolor, marker=markers[si])  #facecolors=[scolor,'none'][i])

        ax2.plot(newflows[:,0] - start,newflows[:,1]/1000, label=labels[i], linestyle=':') #marker=markers[si]  #facecolors=[scolor,'none'][i])
    ax2.legend(loc="lower left", bbox_to_anchor=(0.5,1.02), ncol=2,title="New flows")

    ax1.set_xlim(0,60)
    #ax1.set_yscale("symlog")
    ax1.set_ylim(0,100)
    ax2.set_ylim(0,100)
#    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Number of active flows X1000')
    ax2.set_ylabel('Number of new flows X1000')
    #plt.grid(True,axis="y")
    #ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))

#    plt.tight_layout()
    plt.subplots_adjust(top=0.8)

    plt.savefig('count-nflows.pdf')

  #  print("Figure saved to loadvsdrop.pdf")

except Exception as e:
    print("Could not plot:")
    traceback.print_exc()

plt.clf()

print("Plotting histogram")

try:

    plt.rcParams["figure.figsize"] = (6,3)
    plt.rcParams['axes.axisbelow'] = True
    fig, ax1 = plt.subplots()

    plt.grid(True,axis="y")
    sz=64
    for i,trace in enumerate(traces):
        nflows = pandaload("iter-count-nodiff/%sLENGTHT.csv" % trace)
        mi = 64
        ma = np.max(nflows[:,0] + 4)
        bins = np.arange((ma-mi) / sz)
        vals = []
        binsx = []
        for j in bins:
            x = mi + (j * sz)
            vals.append(np.sum(nflows[(nflows[:,0] >= x-4) & (nflows[:,0] < x - 4 + sz),1]))
            binsx.append(x)
            #print("%d-%d -> %d" % (x,x+sz,vals[-1]))


        ax1.bar(np.array(binsx) + (i - 0.5) * (sz/2), np.array(vals) / 1000000, label=labels[i], width=(sz*0.8)/len(traces), align="center") #marker=markers[si]  #facecolors=[scolor,'none'][i])

    ax1.legend(loc="lower center", bbox_to_anchor=(0.5,1.02), ncol=2, title="Trace")

    binsx.append(ma)
    ax1.set_xticks(np.array(binsx) -( sz /2))
    ax1.set_xticklabels([("%d" %x) if i%2==0 else "" for i,x in enumerate(binsx)])
    ax1.set_yscale("symlog")
    ax1.set_yticks([0,1,2,4,8,16,32,64])
    #ax1.set_ylim(0,100)
    ax1.set_xlabel('Packet size (bytes)')
    ax1.set_ylabel('Number of packets (M)')
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    plt.tight_layout()
    #plt.subplots_adjust(top=0.8)

    plt.savefig('length-hist.pdf')

    print("Figure saved to length-hist.pdf")

except Exception as e:
    print("Could not plot:")
    traceback.print_exc()


plt.clf()

print("Plotting histogram of flow duration")

try:

    plt.rcParams["figure.figsize"] = (6,3)
    plt.rcParams['axes.axisbelow'] = True
    fig, ax1 = plt.subplots()

    plt.grid(True,axis="y")
    sz=64
    for i,trace in enumerate(traces):
        val = pandaload("iter-count-nodiff/%sCOUNTN.csv" % trace)
        freq= [0]
        freq.extend(val[:,1][:-1])

        freq=val[:,1] - freq
#        print(val[:,0],freq)
        fake = np.repeat(val[:,0], [int(f) for f in freq])
        tot = np.sum(val[:,0] * freq)
        print("Average flow size for trace %s : %d %d %d" % (trace, tot / np.sum(freq), np.mean(fake),np.median(fake)))

        cdf = pandaload("iter-count-nodiff/%sCOUNTCDF.csv" % trace)
        p = ax1.plot(cdf[:,0], cdf[:,1], label=labels[i], ls=styles[i]) #marker=markers[si]  #facecolors=[scolor,'none'][i])

        plt.annotate("100%% = %d flows" % val[np.argmax(val[:,0]),1],xy= (np.max(val[:,0]),cdf[np.argmax(val[:,0]),1]), xytext=(0.9,0.8 - i*0.11), textcoords="axes fraction",color=p[0].get_color(), horizontalalignment="right")

    ax1.legend(loc="lower center", bbox_to_anchor=(0.5,1.02), ncol=2, title="Trace")


    ax1.set_xscale("symlog")
    ax1.set_xlim(1)
    #ax1.set_yscale("symlog")
    #ax1.set_yticks([0,1,2,4,8,16,32,64])
    #ax1.set_ylim(0,100)
    ax1.set_ylabel('Fraction of flows')
    ax1.set_xlabel('Number of packets in flows')
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%d%%'))

    ax1.xaxis.set_major_formatter(FuncFormatter(lambda x,pos : "%d" % int(x) if int(x) < 1000 else "%dK" % (int(x)/1000)))

    plt.tight_layout()
    #plt.subplots_adjust(top=0.8)

    plt.savefig('count-hist.pdf')

    print("Figure saved to count-hist.pdf")

except Exception as e:
    print("Could not plot:")
    traceback.print_exc()

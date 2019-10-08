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

import traceback

series = ["loadvslat-kthmorning-cx5/RSS" ,  "loadvslat-kthmorning-cx5/RSSPP"]
#, "kthmorning-cx5/Metron" ]
labels = ["RSS","RSS++","Metron"]
#colors = [(c1/255.0,c2/255.0,c3/255.0) for c1,c2,c3 in colors]

t_markers = [m_rss, m_rsspp]


colors = [c_rss,c_rsspp,c_metron]

#################################################
#################################################

print("Plotting VSDROPPED")


#speed_gbps = get_speed_gbps(series[1].replace('loadvslat','loadvsdrop'))
speed_gbps={}

speed_tx={}
try:

    plt.rcParams["figure.figsize"] = (6,3)

    fig, ax1 = plt.subplots()
    speeds = [120, 130, 140]
#data_v_s = []
    for i,s in enumerate(series):
        data_v=OrderedDict()

        print("Reading %s" % s)
        for speed in speeds:
            th = pandaload(s.replace("vslat","vsdrop") + "_-_Trace_replay_speed___" + str(speed) + "IGTHROUGHPUT.csv")
            th = th[(th[:,0] > 5) & (th[:,0] < 60),1:]
            speed_gbps[speed] = np.mean(th)

            tx = pandaload(s.replace("vslat","vsdrop") + "_-_Trace_replay_speed___" + str(speed) + "IGTX.csv")
            tx = tx[(tx[:,0] > 5) & (tx[:,0] < 60),1:]
            speed_tx[speed] = np.mean(tx / 1000000000)
            d = pandas.read_csv(  s.replace("vslat","vsdrop") + "_-_Trace_replay_speed___" + str(speed) + "IGDROPPED.csv", header=None, engine="python",delim_whitespace=True,names=list(range(4)))

            for idx,l in d.iterrows():
                data_v.setdefault(speed,[])

                data_v[speed].append(l.to_numpy())
        #data_v_s.append(data_v)

        print("Plotting %s" % s)
        for si,speed in enumerate(speeds):
            data = data_v[speed]
            print("Speed %d" % speed)
            data = np.asarray(data)
            agg = OrderedDict()
            for l in data:
                #k=int(l[0])
                k=l[0]
                agg.setdefault(k,[]).extend(l[1:])
            x = np.array(list(agg.keys()))
            y = np.array([np.nanmean(d) for k,d in agg.items() ])
            label = "%s - %.01f/%.01fGbps" % (labels[i],speed_gbps[speed],speed_tx[speed])
            scolor=shade(colors[i],si,len(speeds) )
            ax1.scatter(x, y, label=label, color=scolor, marker=markers[si])  #facecolors=[scolor,'none'][i])

    ax1.legend(loc="lower center", bbox_to_anchor=(0.5,1), ncol=2)

    ax1.set_xlim(0,60)
    #ax1.set_yscale("symlog")
    ax1.set_ylim(0)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Packets dropped X1000')
    #plt.grid(True,axis="y")
    #ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    plt.tight_layout()
    plt.subplots_adjust(top=0.75)

    plt.savefig('loadvsdrop.pdf')

    print("Figure saved to loadvsdrop.pdf")

except Exception as e:
    print("Could not plot:")
    traceback.print_exc()
    print("Last data :")
    print(d)

plt.clf()



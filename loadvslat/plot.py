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
import pandas
from matplotlib.markers import MarkerStyle
import traceback

series = ["loadvslat-kthmorning-cx5/RSS" ,  "loadvslat-kthmorning-cx5/RSSPP"]
#, "kthmorning-cx5/Metron" ]
labels = ["RSS","RSS++","Metron"]
#colors = [(c1/255.0,c2/255.0,c3/255.0) for c1,c2,c3 in colors]

t_markers = [m_rss, m_rsspp]


colors = [c_rss,c_rsspp,c_metron]



tx = np.genfromtxt(series[1] + "TX.csv")
tx[:,1:] = tx[:,1:] / 1000000000
speed_gbps = {}
for tx_d in tx:
    speed_gbps[int(tx_d[0])]= np.mean(tx_d[1:])

load = pandas.read_csv( series[1]  + "TLOAD.csv", header=None,engine="python",delim_whitespace=True)
load_avg = {}
for col,seriesv in load.iterrows():
    speed = seriesv[0]
    load_d = seriesv[1]
    load_avg[int(speed)]= np.mean(load_d) / 4

print("Speed to Load mapping")
print(speed_gbps)
print("Speed to CPU mapping")
print(load_avg)


#################################################
#################################################

print("Plotting VSDROPPED")
try:

    plt.rcParams["figure.figsize"] = (6,3)

    fig, ax1 = plt.subplots()
    speeds = [120, 130, 140]
#data_v_s = []
    for i,s in enumerate(series):
        data_v=OrderedDict()

        print("Reading %s" % s)
        for speed in speeds:
            d = pandas.read_csv(  s.replace("vslat","vsdrop") + "_-_Trace_replay_speed___" + str(speed) + "IDROPPED.csv", header=None, engine="python",delim_whitespace=True,names=list(range(4)))
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
            print(len(x), len(y))
            label = "%s - %.01fGbps" % (labels[i],speed_gbps[speed])

            scolor=shade(colors[i],si,len(speeds) )
            ax1.scatter(x, y, label=label, color=scolor, marker=markers[si])  #facecolors=[scolor,'none'][i])

    ax1.legend(loc="lower center", bbox_to_anchor=(0.5,1), ncol=2)

#lines = [Line2D([0], [0], color=colors[0], linestyle='-'),
#         Line2D([0], [0], color=colors[1], linestyle='-')]

#artist = ax1.legend(lines, labels[:2], loc="lower left",  bbox_to_anchor=(0.0,1.0,0.45,1), title=None, mode="expand")

#lines = []

#speeds_gbps = []
#for i in range(3):
#    lines.append(Line2D([0], [0], color=shade((0.5,0.5,0.5),i,3),marker=markers[i], linestyle=' '))
#
#    idx = np.where( tx[:,0] == speeds[i] )
#    gbps = np.mean(tx[idx,1:])
#    speeds_gbps.append("%.01fGbps" % (gbps))
#ax1.legend(lines, speeds_gbps, loc="lower right",  bbox_to_anchor=(0.45,1.0,0.55,1), ncol=1, title=None,mode="expand" )

#ax1.add_artist(artist)


    ax1.set_xlim(0,60)

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Packets dropped X1000')


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


#################################################
#################################################
print("Plotting CDFLAT")

plt.rcParams["figure.figsize"] = (6,3.5)

cdflat_speeds = [105,125,135]

try:
    fig, ax1 = plt.subplots()
    latencys = []
    for i,s in enumerate(series):
        latencys.append([])
        for rspeed in cdflat_speeds:
            print("Loading %d from %s..." % (rspeed,s))
            latencys[i].append((np.genfromtxt(os.path.dirname(s.replace("vslat","vslatcdf")) + os.sep + "lat-" + os.path.basename(s) +"-"+str(int(rspeed)) +".csv")))

    percs = [0.5,0.75,0.8,0.9,0.95]

    perc_show = [95,90,50]
    perc_vals = []
    for i,latency_s in enumerate(latencys):
        for il,latency in enumerate(latency_s):
            num_bins = 1000
            counts, bin_edges = np.histogram (latency, bins=num_bins, normed=True)
            cdf = np.cumsum (counts)
            #markevery=(0.0, 0.1),
            #marker = markers[il],
            for perc in percs:
                print("Perc %s at %d -> %d : %d" % (labels[i],cdflat_speeds[il],perc*100,np.percentile(latency,perc*100)))
            perc_vals.append(np.percentile(latency,perc_show[il]))
            rects = ax1.plot(bin_edges[1:], cdf/cdf[-1] * 100, color=shade(colors[i], il, len(cdflat_speeds)), linestyle=linestyles[il], label="%s - CPU @ %d%%" % (labels[i],load_avg[cdflat_speeds[il]] * 100))

    pos=[90,60,30]
    for il,perc in enumerate(perc_show):
        a = perc_vals[il]
        b = perc_vals[il + len(perc_show)]
        ax1.annotate(xy=(a,perc),xytext=(b,perc),color="black",s="",arrowprops=dict(facecolor='black', arrowstyle='|-|'))
        ax1.arrow(b + (a - b) *0.5,perc,6000-a,pos[il]-perc,color="black", linestyle=':' )
        ax1.text(15000,pos[il] - 10,color="black",s="%dth perc.\nCPU @ %d%%\n%.01fX" % (perc, load_avg[cdflat_speeds[il]]*100, a / b), horizontalalignment='center',verticalalignment='center' )

    ax1.set_xscale("symlog")
    ax1.set_ylabel("Fraction of packets (%)")
    ax1.set_xlabel("Latency (us)")

    ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax1.legend(loc="lower center",bbox_to_anchor=(0.5,1.0), ncol=2)




    plt.tight_layout()

    print("Figure saved to loadvscdflat.pdf")
    plt.savefig('loadvscdflat.pdf')

except Exception as e:
    print("ERROR:")
    print(e)
    traceback.print_exc()


plt.clf()





########################################
########################################

print("Ploting loadvslat")
plt.ticklabel_format()

throughputs = []
latencys = []


for s in series:
    throughputs.append(np.genfromtxt(s + "THROUGHPUT.csv")) #TLOAD
fig, ax1 = plt.subplots()

fig.set_size_inches(6,3)

for i,throughput in enumerate(throughputs):
    ax1.errorbar(throughput[:,0], [np.mean(t) for t in throughput[:,1:]], yerr=[np.std(t) for t in throughput[:,1:]], label=labels[i], color = colors[i], marker=t_markers[i])

ax1.errorbar(tx[:,0], [np.mean(t) for t in tx[:,1:]], yerr=[np.std(t) for t in tx[:,1:]], label="Offered load", color = "black", ls = ":")

handles, labels = ax1.get_legend_handles_labels()

new_handles = []

for h in handles:
    #only need to edit the errorbar legend entries
    if isinstance(h, container.ErrorbarContainer):
        new_handles.append(h[0])
    else:
        new_handles.append(h)

ax1.legend(new_handles, labels)

ax1.set_ylabel('Throughput (Gbps)')
#ax1.set_ylabel('CPU Load')
ax1.set_xlabel('Average offered load (Gbps)')

#ax1.set_xlim([0, 60])
#ax1.set_ylim([0, 25])


#ax2.xaxis.set_major_locator(ticker.FixedLocator(ticks))


ax2 = ax1.twinx()

def lighter(c, p, n):
    n = n / 255.
    return tuple(a * p + (1-p) * n for a in c)


for i,s in enumerate(series):
    latencys.append([])
    for rspeed in throughputs[i][:,0]:
        print("Loading %d..." % rspeed)
        latencys[i].append((np.genfromtxt(os.path.dirname(s) + os.sep + "lat-" + os.path.basename(s) +"-"+str(int(rspeed)) +".csv") / 1000))




for i,mmlatency in enumerate(latencys):
    rects = ax2.boxplot(mmlatency, showfliers=False, positions=throughput[:,0] + (-1+2*i), widths=1.2)
    plt.setp(rects['boxes'], color = colors[i])
    plt.setp(rects['whiskers'], color = colors[i])
    plt.setp(rects['caps'], color = colors[i])
    plt.setp(rects['fliers'], color = colors[i])
    plt.setp(rects['medians'], color = lighter(colors[i],0.50,0))


    #if i == 0:
    #    m = max(latency[:,1])
    #    latency = np.array([[0,m],[60,m]])
    #ax2.plot(latency[:,0] - min(latency[:,0]) - shift[i], latency[:,1], linestyle=':', drawstyle='steps')

mi=min(throughput[:,0])
ma=max(throughput[:,0])

ticks=mi + np.arange(int((ma-mi)/10))*10
ax2.set_xticks(ticks)
ax2.set_xlim(min(ticks)-5,max(ticks)+5)
ax2.set_xticklabels(["%.01f" % (speed_gbps[speed]) for speed in ticks])
ax2.set_ylabel('Latency (ms)')
#ax2.legend(loc="lower right")

#ax2.set_ylim([0, 16])
#ax2.yaxis.set_major_locator(ticker.MultipleLocator(2.00))
#ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

#ax1.legend()
#ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#           ncol=3, mode="expand", borderaxespad=0.)

#lines = [Line2D([0], [0], color="black" ),
#                  Line2D([0], [0], color="black", linestyle=':')]

#ax2.legend(lines, ["Throughput", "CPUs"], loc="upper right",  bbox_to_anchor=(1.0,0.9) )


plt.tight_layout()

plt.savefig('loadvslat.pdf')



from common import *
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

#################################################
#################################################
print("Plotting CDFLAT")

plt.rcParams["figure.figsize"] = (6,3.5)

cdflat_speeds = [105,125,135]

speed_gbps = get_speed_gbps(series[1].replace('loadvslat','loadvslatcdf'))

load_avg = get_load_avg(series[1].replace('loadvslat','loadvslatcdf'))

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
        print("%d -> %d / %d = %f" % (perc,a,b,a/b))
        ax1.annotate(xy=(a,perc),xytext=(b,perc),color="black",s="",arrowprops=dict(facecolor='black', arrowstyle='|-|'))
        ax1.arrow(b + (a - b) *0.5,perc,6000-a,pos[il]-perc,color="black", linestyle=':' )
        ax1.text(15000,pos[il] - 10,color="black",s="%dth perc.\nCPU @ %d%%\n%.01fX" % (perc, load_avg[cdflat_speeds[il]]*100, a / b), horizontalalignment='center',verticalalignment='center' )

    ax1.set_xscale("symlog")
    ax1.set_ylabel("Fraction of packets (%)")
    ax1.set_xlabel("Latency (us)")

    ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax1.legend(loc="lower center",bbox_to_anchor=(0.5,1.0), ncol=2)




    plt.tight_layout()

    plt.subplots_adjust(top=0.8)
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


load_avg = get_load_avg(series[1])

speed_gbps = get_speed_gbps(series[1])

plt.ticklabel_format()

throughputs = []
latencys = []

tx = np.genfromtxt(series[1] + "TX.csv")

for s in series:
    throughputs.append(np.genfromtxt(s + "THROUGHPUT.csv")) #TLOAD
fig, ax1 = plt.subplots()

fig.set_size_inches(6,3)

for i,throughput in enumerate(throughputs):
    ax1.errorbar(throughput[:,0], [np.mean(t) for t in throughput[:,1:]], yerr=[np.std(t) for t in throughput[:,1:]], label=labels[i], color = colors[i], marker=t_markers[i])

ax1.errorbar(tx[:,0], [np.median(t / 1000000000) for t in tx[:,1:]], yerr=[np.std(t / 1000000000) for t in tx[:,1:]], label="Offered load", color = "black", ls = ":")

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
        lats = np.genfromtxt(os.path.dirname(s) + os.sep + "lat-" + os.path.basename(s) +"-"+str(int(rspeed)) +".csv") / 1000
        latencys[i].append(lats[int(len(lats) / 10):int(len(lats)/10)*9])




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

mi=100 #min(throughput[:,0])
ma=170 #max(throughput[:,0])
print("From %d to %d" % (mi,ma))
ticks=mi + np.arange(int((ma-mi)/10) )*10
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



import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
from common import *
from math import log,pow
import pandas

traces = ["kthmorningsingle", "kthmorningquad"] #, "caida18"]

traces_names=["Campus (4Gbps)","Campus #4 (15Gbps)"] #, "CAIDA (3.5Gbps)"]

series= ["RSS", "Sprayer", "Software_Shared_Queue", "Software_RR_Queue", "Software_Stateful_RR", "Software_Stateful_Load", "Metron_Dynamic", "RSSPP"]

labels= ["RSS", "Sprayer", "SW Shared Queue", "SW RR Queues", "SW Stateful RR", "SW Stateful Load", "Traffic-Class", "RSS++"]
tcolors = [ c_rss, c_sprayer, light_orange, dark_orange, light_red, dark_red, c_metron, c_rsspp ]

tmarkers = markers

tmarkers[labels.index("RSS++")] = 'd'


print("Plotting THROUGHPUT per core")
cores = range(1,17)
for trace in traces:
    try:
        print("Reading trace %s" % trace)
        data_s_c = []
        for serie in series:
          data_s = []
          for core in cores:
            #Sprayer_-_Number_of_processing_cores__9MIN-MAX-LOAD-PKTS-RATIO.csv
            data = np.genfromtxt("imbalance-all-%s/%s_-_Number_of_processing_cores__%dIGTHROUGHPUT.csv" % (trace, serie, core))
            data = data[ (data[:,0] < 50) & (data[:,0] > 5) ]
            #print(data)
            data_s.append(data)
          data_s_c.append(data_s)
    except Exception as e:
        print("While reading trace %s:" % trace)
        print(e)
        continue

    plt.clf()
    plt.rcParams["figure.figsize"] = (6,3)
    fig, ax1 = plt.subplots()

    ax2 = ax1

    #rcolor = darker(colors[1])
    #ax2.set_ylabel('Packets in queues', color=rcolor)  # we already handled the x-label with ax1

    ax2.set_ylabel('Throughput (Gbps)')

    for i,data_s in enumerate(data_s_c):

        scolor = tcolors[i]
        rects = ax2.plot(cores, [np.median(data[:,1:]) for data in data_s], color=scolor,marker=tmarkers[i],label=labels[i])

        rects = ax2.fill_between(cores, [np.percentile(data[:,1:],25) for data in data_s], [np.percentile(data[:,1:],75) for data in data_s], color=list(scolor) + [0.25])

    ax2.set_ylim(0)

    ax2.set_xlim(min(cores)-0.5,max(cores) + 0.5)
    #t = np.arange(7) * 5
    #ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))

    plt.grid(True, axis="y")
    #ax2.set_yscale("symlog")
    #ax2.legend()
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    #ax2.set_xticks(t)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig('throughput-all-%s.pdf' % trace)



plt.clf()




print("Plotting standard MIN-MAX version, one graph per trace")
for trace in traces:
  try:
    print("Reading trace %s" % trace)
    data_s = []
    for serie in series:
        data = np.genfromtxt("imbalance-%s/%sMIN-MAX-LOAD-PKTS-RATIO.csv" % (trace, serie))
        data = data[ data[:,0] < 50 ]

    #    ideal = np.genfromtxt("imbalance-%s/%sIDEAL-LOAD-PER-QUEUE-PKTS.csv" % (trace, serie))
    #    ideal = ideal[ ideal[:,0] < 50 ]
    #    data = []
    #    for queue in range(8):
    #        d = np.genfromtxt("imbalance-%s/%sIQUEUE-PKTS-%d.csv" % (trace,serie,queue))
    #        d = d[ d[:,0] < 50 ]
    #        d = np.ediff1d(d[:,1])
    #        data.extend(d * 100 / ideal[1:,1])
        data_s.append(data)
    plt.clf()
    plt.rcParams["figure.figsize"] = (6,3.5)
    fig, ax1 = plt.subplots()

    ax2 = ax1

    assert(len(data_s) == len(labels))
    #rcolor = darker(colors[1])
    #ax2.set_ylabel('Packets in queues', color=rcolor)  # we already handled the x-label with ax1

    ax2.set_ylabel('Load imbalance (%)')

    for i,data in enumerate(data_s):
        x = [i]

        #time = data[:,0]
        rtts = data[:,1:]
        #rtts = data
        #to plot all
        #rects = ax2.boxplot(np.transpose(rtts),positions=time)

        scolor = tcolors[i]
        rects = ax2.boxplot(rtts,positions=x, widths = 0.8)
        plt.setp(rects['boxes'], color = scolor)
        plt.setp(rects['whiskers'], color = scolor)
        plt.setp(rects['caps'], color = scolor)
        plt.setp(rects['fliers'], color = scolor)
        plt.setp(rects['medians'], color = lighter(scolor,0.50,0))

        ax2.text((i + 0.5) / len(data_s) , 0.02, "%d%%" % (np.mean(rtts)), horizontalalignment="center", transform=ax2.transAxes, color=scolor, weight="bold")

    #ax2.tick_params(axis='y', labelcolor=rcolor)
    #ax2.set_ylim(0)
    ax2.set_xlim(-0.5,len(data_s) - 0.5)
    plt.xticks(np.arange(len(data_s)), labels, rotation = 45)
    #t = np.arange(7) * 5
    #ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))

    plt.grid(True, axis="y")
    ax2.set_yscale("symlog")

    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    #ax2.set_xticks(t)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig('imbalance-%s.pdf' % trace)
  except Exception as e:
      print(e)
      pass
plt.clf()


do_legend = True
print("Plotting MIN-MAX per core")
cores = range(1,17)
for trace in traces:
    print("Reading trace %s" % trace)
    data_s_c = []
    for serie in series:

        data_s = []
        for core in cores:

            try:
                fname = "imbalance-all-%s/%s_-_Number_of_processing_cores__%dMIN-MAX-LOAD-PKTS-RATIO.csv" % (trace, serie, core)
                data = pandas.read_csv(fname, header=None, engine="python",usecols=range(4),delim_whitespace=True,index_col=False).to_numpy()

                #data = np.genfromtxt(fname)
                #print(fname,data)
                data = data[ (data[:,0] < 50) & (data[:,0] > 5) ]

                data_s.append(data)

            except Exception as e:
                data_s.append([])
                print("While reading trace %s, serie %s file %s" % (trace,serie,fname))
                print(e)
                print(data)
                continue

        data_s_c.append(data_s)
    plt.clf()
    plt.rcParams["figure.figsize"] = (6, 3.8 if do_legend else 3)
    fig, ax1 = plt.subplots()

    ax2 = ax1

    #rcolor = darker(colors[1])
    #ax2.set_ylabel('Packets in queues', color=rcolor)  # we already handled the x-label with ax1

    ax2.set_ylabel('Load imbalance (%)')


    for i,data_s in enumerate(data_s_c):
      try:
        scolor = tcolors[i]

        Y = [data[:,1:] for data in data_s]

        rects = ax2.plot(cores, [np.nanmedian(data) for data in Y], color=scolor,marker=tmarkers[i],label=labels[i])
        rects = ax2.fill_between(cores, [np.nanpercentile(data,25) if len(data) > 0 else np.nan for data in Y], [np.nanpercentile(data,75) if len(data) > 0 else np.nan for data in Y], color=list(scolor) + [0.25])
      except Exception as e:
        print("ERROR while plotting %s" % series[i])
        print(e)


    ax2.set_ylim(0)
    ax2.set_xlabel("Number of processing cores")
    ax2.set_xticks(np.arange(max(cores) / 2) * 2 + 1)
    ax2.set_xlim(min(cores)-0.5,max(cores) + 0.5)
    #t = np.arange(7) * 5
    #ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))

    plt.grid(True, axis="y")
    ax2.set_yscale("symlog")
    #ax2.legend()

    if do_legend:
        ax2.legend(ncol=3,bbox_to_anchor=(0.5, 1.),loc="lower center")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    #ax2.set_xticks(t)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    name='imbalance-all-%s.pdf' % trace
    print("Writing %s..." % name)
    plt.savefig(name)



plt.clf()



print("CPU load version")
series_hw= ["RSS", "Sprayer", "Metron_Dynamic", "RSSPP"]

labels_hw= ["RSS", "Sprayer", "Traffic-Class", "RSS++"]
for trace in traces:
    print("Reading trace %s" % trace)
    data_s = []
    mean_s = []
    for serie in series_hw:

        #ideal = np.genfromtxt("imbalance-%s/%sIDEAL-LOAD-PER-QUEUE-PKTS.csv" % (trace, serie))
        #ideal = ideal[ ideal[:,0] < 50 ]
        data = []
        data_r = []
        for queue in range(8):
            d = np.genfromtxt("imbalance-%s/%s_-_CPU__%dICPU.csv" % (trace,serie,queue))
            d = d[( d[:,0] < 50) & (d[:,0] > 5) ]
            #d = np.ediff1d(d[:,1])
            data_r.append(d[:,1])

        mean = np.asarray([np.mean([ data_r[q][i] for q in range(8) ]) for i in range(len(d))])

        mean_s.append(np.mean(mean))
        mmax = np.asarray([np.max([ data_r[q][i] for q in range(8) ]) for i in range(len(d))])
        for queue in range(8):
            d = mean - (data_r[queue]) # () / mmax
            data.extend(d * 100)
        data_s.append(data)
    plt.clf()
    plt.rcParams["figure.figsize"] = (6,3.5)
    fig, ax1 = plt.subplots()

    ax2 = ax1

    assert(len(data_s) == len(labels_hw))
    #rcolor = darker(colors[1])
    #ax2.set_ylabel('Packets in queues', color=rcolor)  # we already handled the x-label with ax1

    ax2.set_ylabel('CPU load (%)')

    for i,data in enumerate(data_s):
        x = [i]

        #time = data[:,0]
        #rtts = data[:,1:]
        rtts = data
        #to plot all
        #rects = ax2.boxplot(np.transpose(rtts),positions=time)
        scolor = tcolors[i]

        rects = ax2.boxplot(np.transpose(rtts),positions=x)
        plt.setp(rects['boxes'], color = scolor)
        plt.setp(rects['whiskers'], color = scolor)
        plt.setp(rects['caps'], color = scolor)
        plt.setp(rects['fliers'], color = scolor)
        plt.setp(rects['medians'], color = lighter(scolor,0.50,0))


        ax2.text((i + 0.5) / len(data_s) , 0.02, "%d%%" % (np.mean(rtts[i]) * 100), horizontalalignment="center", transform=ax2.transAxes, color=scolor, weight="bold")
    #ax2.tick_params(axis='y', labelcolor=rcolor)
    #ax2.set_ylim(0)
    ax2.set_xlim(-0.5,len(data_s) - 0.5)
    plt.xticks(np.arange(len(data_s)), labels_hw, rotation = 45)
    #t = np.arange(7) * 5
    #ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))

    plt.grid(True, axis="y")

    #ax2.set_yscale("symlog")

    #ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
    #ax2.set_xticks(t)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig('imbalance-load-%s.pdf' % trace)


plt.clf()



plt.rcParams["figure.figsize"] = (6,3.5)

print("All at once")

print("Reading trace %s" % trace)

data_t_s = []


for serie in series:
  data_s = []
  for trace in traces:
    data = np.genfromtxt("imbalance-%s/%sMIN-MAX-LOAD-PKTS-RATIO.csv" % (trace, serie))
    data = data[ (data[:,0] < 50) & (data[:,0] > 5) ]
    data_s.append(data[:,1])
  data_t_s.append(data_s)

fig, ax1 = plt.subplots()

ax2 = ax1


ax2.set_ylabel('Load imbalance (%)')

inter = 1
sspace =  len(series) + (2 * inter)

rss_idx = labels.index("RSS")
rsspp_idx = labels.index("RSS++")


print_idx = [rss_idx, rsspp_idx]
#print_idx = range(len(series))
print_below = False
for i,data in enumerate(data_t_s):

    #rtts = data
    #to plot all
    #rects = ax2.boxplot(np.transpose(rtts),positions=time)

    scolor = tcolors[i]

    pos = np.arange(len(data)) *  sspace + i + inter

    if i in print_idx:
        for j in range(len(data)):
            med = np.median(data[j])
            diff = 0
            if j == 0 and i == rss_idx:
                diff = 0
            if j == 1 and i == rsspp_idx:
                diff = 1

            plt.text(pos[j], 0.02 if print_below else (med + pow(3 + diff,log(med))) ,"%d%%" % np.mean(data[j]), horizontalalignment="center", color=scolor)
    ax2.scatter(pos, [np.median(d) for d in data], color=scolor, label=labels[i], marker=tmarkers[i])
    rects = ax2.boxplot(np.transpose(data),positions=pos, widths=[0.9]*len(data))
    plt.setp(rects['boxes'], color = scolor)
    plt.setp(rects['whiskers'], color = scolor)
    plt.setp(rects['caps'], color = scolor)
    plt.setp(rects['fliers'], color = scolor)
    plt.setp(rects['medians'], color = lighter(scolor,0.50,0))

plt.grid(True, axis="y")

#ax2.tick_params(axis='y', labelcolor=rcolor)
h = 2200
ax2.set_ylim(0,h)
ax2.set_xlim(-0.5,sspace * len(traces) - 0.5)
xpos = np.arange(len(traces)) * sspace + float(sspace - 1) / 2
plt.xticks(xpos,  traces_names, rotation = 0)
#t = np.arange(7) * 5
#ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))

b = ax2.bar(xpos , height=h, width=sspace, color=[lighter(grey,.12,1),lighter(grey,.05,1)], zorder=-99999)

ax2.set_yscale("symlog")

ax2.legend(ncol=3,bbox_to_anchor=(0.5, 1.),loc="lower center")

ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%d" % (x)))
#ax2.set_xticks(t)
fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.savefig('imbalance.pdf')

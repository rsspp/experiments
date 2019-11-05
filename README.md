RSS++ Experiments
=================

This folder contains one sub-folder per experiment. Some figures of RSS++ paper relate to the same experiment.

Experiments have "make test" and "make graph". "make" alone will do both.

All tests use NPF to orchestrate experiments. Be sure to set the path to NPF in Makefile.include. While NPF generates graph automatically, we preferred to make fine-tuned graphs using matplotlib ourselves.

NPF will download and build all dependencies, including RSS++ by itself. However there are two things you must do by yourself:

Testbed
-------
For all tests, you need two computers, one that we'll refer as the *server*, that is the device under test running RSS++ (and compared systems) and one refered to as *client*, the traffic generator that will replay the traces (or use IPerf for the Linux experiment) and compute latency when packets come back. They were interconnected with Mellanox Connect-X 5 NICs with 100G direct attach cables, we also had XL710 and 82599 Intel NICs, limited respectively to 40G and 10G. None of the results are shown in the paper, but some experiments have been reproduced with them.
In the current version of the experiment, we used only one physical NIC per machine, so the traffic would be sinked back through the same port.
While our experiment was done with a 18-cores Xeon for the DUT, results should apply for different machines. The generator uses FastClick to replay traces up to 100G. The generator is hardwired to use 8 cores, hence you need at least that number of core and enough memory to keep a good portion of the first 60 seconds of the trace in RAM.

Prerequisites
-------------

### NPF
Download NPF at (https://github.com/tbarbette/npf). Install python3 and python3-pip with your system package manager and the requirements with `pip3 install -r requirements.rxt`. In case of troubles, you may find more help on the README.md page of NPF.

You must define the servers and the NICs to be used in the cluster folder of NPF. This is our file for the server:
cluster/server0.node
```
path=/home/tom/npf/
addr=server0.kth.se
//nfs=0

0:ifname=eth0
0:pci=0000:03:00.0
0:mac=50:6b:4b:43:88:ca
```

And this is our file for the client:
cluster/client0.node
```
path=/home/tom/npf/
addr=client0.kth.se
//nfs=0

0:ifname=eth0
0:pci=0000:03:00.0
0:mac=50:6b:4b:43:80:ab
```
The `path` is the path to NPF on the given machine. It is easer to have NPF in an NFS or other mechanism to share a similar folder between the two machines, under the same path. If you don't have such a setup, uncomment nfs=0 at the top of the file.

The `addr` (address) is the address of the machine. Then we define 3 variables per NIC: the interface name, the PCIe address, and the mac address of the NIC. Note that these interfaces are real interfaces, as RSS++ is focusing on dispatching packets in hardware. You may obtain the PCIe address of the interface you want to use with `sudo lshw -c network -businfo`.

These informations are used by NPF to automatically replace references in scripts.

### Makefiles configuration
As discussed below, all experiments are easily launched using a single Makefile per experiment. As a few parameters depend on your environment (such as the path to the folder where you checked out NPF), we have a single "include" file that resides in the "includes" folder of this repository which is included by all per-experiment Makefiles to set common parameters.
You may define the required variables to in [includes/Makefile.include](includes/Makefile.include). Set `NPF_PATH=path/to/npf` correctly, and change the name of the roles only if you used a different name than "cluster/server0.node" and "cluster/client0.node" for the NPF cluster configuration files.

### Modified Kernel on the DUT
For the kernel experiment you must have our modified Kernel, available at [https://github.com/rsspp/linux](https://github.com/rsspp/linux). If you're not familiar with Kernel compilation, instructions are provided in the README.md file of that repository. It is much easier than it is said to be, and faster too if you have a SSD and append `-j8` where 8 is the number of cores on the machine to all `make` commands to build using multiple cores.

### Install DPDK on both machines
Download DPDK 19.02 at [http://dpdk.org](http://dpdk.org). To install, just use ./usertools/setup.py, then choose x86_64-native-linuxapp-gcc, then set up some huge pages, and if you use Intel NICs bind them.

### Traces
Most DPDK experiments use a trace, as a workload to various benchmarks. Unfortunately we cannot share our campus trace.
Look at the paper to find the characteristics of the trace (one trace at 4Gbps, one "accelerated" at 15Gbps in the paper). One can use CAIDA 2018 traces but its relatively small speed limits reproducibility of the experiments with their current parameter (remember RSS++ aims to keep the CPU load at a high level, if the trace runs slower, you need to use less cores/more load on the DUT to a somehow unrealistic extent, which is why we used our own). You may use [our script](traces/) to accelerate your trace. Sprayer emulation also needs the trace [to be rewritten](traces/) (for experiments imbalance, latency, drop and nat), and similarly metron emulation needs rules specific to each traces to dispatch "traffic classes".

Change the line `kthmorningsingle:trace=XX` and `kthmorningquad:trace=YY` in testie.d/traces.testie to change the path to your own trace files.


Summary of content
------------------

### Experiments
The following folders contain the Makefile for the experiment, that basically calls NPF with one of the two testies. Some experiment folders contain the generated data and plots.
All experiments folder contain a "README.md" file that explains them further.

#### Kernel
 * heatmap: Figure 1 and Figure 3, showing the iPerf2 test. It is driven by kernel.testie, that is fairly readable. This experiment does *not* needs a trace as it uses iPerf.

#### DPDK
All DPDK experiments need a trace except "shared" and "migration" that generates UDP flows. You may read about traces further below.

 * loadvslat: Figures 10a,b,c about RSS vs RSS++. Latency, throughput, drops, etc
 * dynamicscale: Figure 11 showing the dynamic scaling of CPU cores.
 * imbalance: Figures 12a and 12b showing the imbalance for the various methods, and according to the number of CPU used  
 * latency: Figure 13 about tail latency.
 * drop: Figure 14 showing the throughput of the various methods
 * shared: Figure 15 showing the importance of flow-awareness with various concurrency models 
 * migration: Figure 16 about state migration
 * (nat: Old figure 17 with the emulated NAT+FW+DPI experiment)
 * real2: Figure 17 with the NAT+FW+DPI experiment
 
### Other
 * includes: Parameters for experiments
 * testie.d: Parts of the two main testie files
 * pcap: Tools to prepare pcap files. Transform a PCAP file for Sprayer simulation (copying checksum to destination mac address) and increasing trace speed
 
Understanding the implementation
--------------------------------
Please read the [README.md file of RSS++'s code](https://github.com/rsspp/fastclick/blob/master/README.md).
 
What if something goes wrong?
-----------------------------
You may append some NPF parameters with the NPF_FLAGS variable such as `make test NPF_FLAGS="--force-retest --show-cmd --show-files --config n_runs=1 --preserve-temporaries"`.
--force-retest will force the test to be done again, even if NPF has some results in cache. --show-cmd will show commands that are launched on the client and server, --show-files will show generated file (such as Click configuration), n_runs=1 configuration parameter reduce the number of runs per tests to 1, while --preserve-temporaries will keep temporary files, scripts, etc so you can launch the test yourself if need be.

One advantage of NPF is the ability to change the defined variables, including from the command line using `--variables CPU=8 FLOW="[50-100#10]"`, for the "heatmap" experiment for example, to see what happens with 8 cores and 50, 60, ..., 100 flows.

And of course, do not hesitate to open issues or contact the authors.

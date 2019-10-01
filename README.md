RSS++ Experiments
=================

This folder contains one sub-folder per experiment. Some figures of RSS++ paper relate to the same experiment.

Experiments have "make test" and "make graph". "make" alone will do both.

All tests use NPF to orchestrate experiments. Be sure to set the path to NPF in Makefile.include. While NPF generates graph automatically, we preferred to make fine-tuned graphs using matplotlib ourselves.

NPF will download and build all dependencies, including RSS++ by itself. However there are two things you must do by yourself:

Testbed
-------
For all tests, you need two computers, one that we'll refer as the *server*, that is the device under test running RSS++ (and compared systems) and one refered to as *client*, the traffic generator that will replay the traces (or use IPerf for the Linux experiment) and compute latency when packets come back. They were interconnected with Mellanox Connect-X 5 NICs with 100G direct attach cables, we also had XL710 and 82599 Intel NICs, limited respectively to 40G and 10G. In the current version of the experiment, we used only one NIC per machine, so the traffic would be sinked back through the same port. We plan on changing the last experiment to use a second link though.
While our experiment was done with a 18-cores Xeon for the DUT, results should apply for different machines. The generator uses FastClick to replay traces up to 100G. The generator is hardwired to use 8 cores, hence you need at least that and enough memory to keep the trace in RAM.

Prerequisites
-------------

### NPF
Download NPF at (https://github.com/tbarbette/npf). Install python3 and python3-pip with your system package manager and the requirements with `pip3 install -r requirements.rxt`. In case of troubles, you may find more help on the README.md page of NPF.

You must define the servers and the NICs to be used in the cluster folder of NPF. This is one of our files:
cluster/server0.node
```
path=/home/tom/npf/
addr=server0.kth.se
//nfs=0

0:ifname=dpdk0
0:pci=0000:17:00.0
0:mac=50:6b:4b:43:88:ca

1:ifname=dpdk1
1:pci=0000:17:00.1
1:mac=50:6b:4b:43:88:cb
```
The `path` is the path to NPF on the given machine. It is easer to have NPF in an NFS or other mechanism to share a similar folder between the two machines, under the same path. If you don't have such a setup, uncomment nfs=0 at the bottom of the file.

The `address` is the address of the machine. Then we define 3 variables per NIC: the interface name, the PCIe address, and the mac address of the NIC. Currently you only need the first interface.

Then, define the required variables to find NPF from this repository in includes/Makefile.inc. Specifically do not forget to define roles, such as `SERVER=server1` and `CLIENT=server0`. You may append `CLIENT=server1,nic=1` to ignore the NIC index 0 and use the second NIC as defined above. This is useful when you plugged the wrong cable, or want to use another NIC (eg a 40G one).

### Modified Kernel on the DUT
For the kernel experiment you must have our modified Kernel, available at [https://github.com/rsspp/linux]. If you're not familiar with Kernel compilation, instructions are provided in the README.md file of that repository. It is much easier than it is said to be, and faster too if you have a SSD.

### Install DPDK on both machined
Download DPDK 19.05 at [http://dpdk.org]. To install, just use ./usertools/setup.py, then choose x86_64-native-linuxapp-gcc, then set up some huge pages, and if you use Intel NICs bind them.

Summary of content
------------------

### Experiments
The following folders contain the Makefile for the experiment, that basically calls NPF with one of the two testies. At some point we will be adding the generated data and plots. 

 * heatmap: Figure 1 and Figure 3, showing the iPerf2 test. It is driven by kernel.testie, that is fairly readable.
 * loadvslat: Figures 8a,b,c about RSS vs RSS++. Latency, throughput, drops, etc
 * dynamicscale: Figure 9 showing the dynamic scaling of CPU cores.
 * imbalance: Figures 10a and 10b showing the imbalance for the various methods, and according to the number of CPU used  
 * latency: Figure 11 about tail latency.
 * drop: Figure 12 showing the throughput of the various methods
 * shared: Figure 13 showing the importance of flow-awareness with various concurrency models 
 * migration: Figure 14 about state migration
 * nat: Figure 15 with the realistic NAT+FW experiment. This one will be modified for camera ready.
 
### Other
 * includes: Parameters for experiments
 * testie.d: Parts of the two main testie files
 
What if something goes wrong?
-----------------------------
You may append some NPF parameters with the NPF_FLAGS variable such as `make test NPF_FLAGS="--force-retest --show-cmd --show-files --config n_runs=1 --preserve-temporaries"`.
--force-retest will force the test to be done again, even if NPF has some results in cache. --show-cmd will show commands that are launched on the client and server, --show-files will show generated file (such as Click configuration), n_runs=1 configuration parameter reduce the number of runs per tests to 1, while --preserve-temporaries will keep temporary files, scripts, etc so you can launch the test yourself if need be.

One advantage of NPF is the ability to change the defined variables, including from the command line using `--variables CPU=8 FLOW="[50-100#10]"`, for the "heatmap" experiment for example, to see what happens with 8 cores and 50, 60, ..., 100 flows.


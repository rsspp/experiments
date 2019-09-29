RSS++ Experiments
=================

This folder contains one sub-folder per experiment. Some figures of RSS++ paper relate to the same experiment.

Experiments have "make test" and "make graph". "make" alone will do both.

All tests use NPF to orchestrate experiments. Be sure to set the path to NPF in Makefile.include. While NPF generates graph automatically, we preferred to make fine-tuned graphs using matplotlib ourselves.

NPF will download and build all dependencies, including RSS++ by itself. However there are two things you must do by yourself:


Prerequisites
-------------

### NPF
Download NPF at (https://github.com/tbarbette/npf). Install python3 and python3-pip with your system package manager and the requirements with pip3 install -r requirements.rxt.

You must define the servers and the NICs to be used in the cluster folder. This is one of our files:
cluster/server0.node
```
path=/home/tom/npf/
addr=nslrack11.ssvl.kth.se
//nfs=0

0:ifname=dpdk0
0:pci=0000:17:00.0
0:mac=50:6b:4b:43:88:ca

1:ifname=dpdk1
1:pci=0000:17:00.1
1:mac=50:6b:4b:43:88:cb
```
It is easer to have NPF in an NFS or other mechanism to share a similar folder between the two machines, under the same path. If you don't have such a setup, uncomment nfs=0 at the bottom of the file.

Then, define the required variables to find NPF from this repository in includes/Makefile.inc. Specifically do not forget to define roles, such as SERVER=server1 and CLIENT=server0.


### Modified Kernel on the DUT
For the kernel experiment you must have our modified Kernel, available at [https://github.com/rsspp/linux]. If you're not familiar with Kernel compilation,  instructions are provided in the README.md file of that repository. It is much easier than it is said to be.

### Install DPDK on both machined
Download DPDK 19.05 at [http://dpdk.org]. To install, just user ./usertools/setup.py then choose x86_64-native-linuxapp-gcc then set up some huge pages, and if you use Intel NICs bind them.

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
 * nat: Figure 15 with the realistic NAT+FW experiment
 
#### What if something goes wrong?
You may append some NPF parameters with the NPF_FLAGS variable such as `make test NPF_FLAGS="--force-retest --show-cmd --show-files --config n_runs=1 --preserve-temporaries"`.
--force-retest will force the test to be done again, even if NPF has some results in cache. --show-cmd will show commands that are launched on the client and server, --show-files will show generated file (such as Click configuration), n_runs=1 configuration parameter reduce the number of runs per tests (variables) to 1, while --preserve-temporaries will keep temporary files, scripts, etc so you can launch the test yourself if need be.

### Other
 * includes: Parameters for experiments
 * testie.d: Parts of the two main testie files

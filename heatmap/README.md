Heatmap experiment
==================
This experiments uses the Kernel implementation with iperf2 to show how a sharded approach is problematic with plain old RSS, and how RSS++ can rebalance flows.

The experiment is managed using NPF. The testie script used is ../kernel.testie, it is well documented.

In short, the operations are:
- Set the servers initial parameters (18 queues, equal RSS distribution), sharded (kill IRQBALANCE)
- Launch 18 iperf servers, one per core, on server, with reuse_port and the 1:1 mapping
- Launch iperf client with 100 flows

During the experiment:
- Record CPU usage while the experiment is running
- After 10 seconds, launch the Click configuration that uses the DeviceBalancer element in RSS++ mode, but with "AUTOSCALE false".
- After 10 seconds, the DriverManager Click element enables autoscale true through a Click handler.

After the experiment:
- Extract RTT from iperf server

NPF takes the recorded data and writes it in CSV files in the results folder for the CPU count, and results-3 for the 3 runs of RTT. We use a single run for CPU because the average CPU usage of many runs would be balanced of course.

Then plot.py generates the graphs you have in the paper (heatmap.pdf and rtt.pdf).

# Throughput of various dispatching methods

This experiment directly follows the "imbalance" once, showing the impact of high imbalance on the throughput.
However it also shows the iniefficiency of software-based dispatching.

For the presentation, we implemented a variant of the base test (which use the trace replayed as fast as possible) and runs the real2 experiments's firewall, replaying a portion of the trace from memory at 100G. It is using the "-fw" suffix.

As usual, this test uses the ../dpdk.testie, read by NPF. THe Makefile is only running the right command line that is already fully explained in the previous experiments.



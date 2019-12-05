# Impact of sharing data between cores
In this test we study the impact of varying the number of (UDP) flows for various testcase implemented using Sprayer, and RSS

The test case are 4:
- Do only per-packet random number generation
- Do a read on per-flow space
- Do a write on per-flow space
- Ensure a sequential write in per-flow space (protected by a lock)

During the test we also measure the packets arriving out of order, and display the proportion in shared-ooos.pdf 

make test will run the test unsing NPF and the ../dpdk.testie

make graph will do the plot

make (all) will do both

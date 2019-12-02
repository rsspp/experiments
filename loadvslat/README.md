# Load vs Latency

A study of how load affects latency. As load gets high, when the load balance is low, RSS will have some queue overloaded, while others are completely fine. Hence the latency will increase.

Like all DPDK-based tests, this test is using the testie ../dpdk.testie. The Makefile provided here is merely a convenience to se set a few parameters.

There are 3 sub-tests, which are the 3 subplots seen in the paper. The difference mostly resides in how we plot the data, the tests only vary with the timing to send.

We use 4 cores in these tests to avoid creating a lot of artificial load. because we want to observe what happens at 80~100% of CPU load. So either we accelerate traces a lot (create skew), run CPU slower (why not), or do a lot of per-packet artifical work to keep a high CPU usage even with a lot of cores (creates skew also). So despite the fact it looses the reader, this seamed to be the most realistic.

As usual "make test" will run the 3 tests. Look at the Makefile to check individual tests.

The main options of npf-compare are:
 * The mode to test, RSS and RSS++ : "rsspp+rss:RSS" "rsspp+pianorss,BALANCE_PERIOD=100:RSSPP"
 * A few variables to use 4 cores, no autoscaling, a load of 400, and 90% to 170% replay speed by step of 5 : --variables BVERBOSE=0 QUEUE=4 AUTOSCALE=0 "W=400" TIMING="[90-170#5]" SAMPLE=100 ITERATION_TIME=1

See ../dpdk.testie for internal working of the test.

Make graph will plot the graph from the generated CSVs file.

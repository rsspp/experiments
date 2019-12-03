from common import *


if True:

    series= ["RSS", "Sprayer", "RSSPP"]

    labels= ["RSS", "Sprayer", "RSS++"]
    tcolors = [ c_rss, c_sprayer, c_rsspp ]



if False:

    series= ["RSS", "Sprayer", "Software_RR_Queue", "Software_Stateful_RR", "Software_Stateful_Load", "RSSPP"]

    labels= ["RSS", "Sprayer", "SW RR", "SW Stateful RR", "SW Stateful Load", "RSS++"]
    tcolors = [ c_rss, c_sprayer, dark_orange, light_red, dark_red, c_rsspp ]

if False:

    series= ["RSS", "Sprayer", "Software_Shared_Queue", "Software_RR_Queue", "Software_Stateful_RR", "Software_Stateful_Load", "Metron_Dynamic", "RSSPP"]

    labels= ["RSS", "Sprayer", "SW Shared Queue", "SW RR Queues", "SW Stateful RR", "SW Stateful Load", "Traffic-Class", "RSS++"]
    tcolors = [ c_rss, c_sprayer, light_orange, dark_orange, light_red, dark_red, c_metron, c_rsspp ]

tmarkers = markers

tmarkers[labels.index("RSS++")] = 'd'



import numpy as np

graphcolor = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
              (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
              (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
              (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
              (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

colors = []
for i in range(int(len(graphcolor) / 2)):
    colors.append((np.asarray(graphcolor[i*2]) + np.asarray(graphcolor[i*2+1])) / 2)

#colors = [(97,146,187),(230,141,60),(88,172,82)]

grey= (0.5, 0.5, 0.5)
graphcolor = [(c1/255.0,c2/255.0,c3/255.0) for c1,c2,c3 in graphcolor]
colors = [(c1/255.0,c2/255.0,c3/255.0) for c1,c2,c3 in colors]
markers=['o', '^', 's', 'D', '*', 'x', '.', 'H', '>', '<', 'v', 'd', '_']
linestyles = ['-', '--', '-.', ':']

def lighter(c, p=0.45, n=230.0/255.0):
    return tuple(a * p + (1-p) * n for a in c)

def darker(c):
    return lighter(c, 0.45, 25.0/255.0)

def shade(c,i,t):
    if (t % 2 == 1) and (int(i) == int(t/2)):
        return c
    elif i < t /2:
        return lighter(c, 0.75, 230.0/255.0)
    else:
        return lighter(c, 0.75, 25.0/255.0)

dark_blue = c_rss = colors[0]
purple = c_rsspp = colors[4]
light_orange = graphcolor[2]
dark_orange = graphcolor[3]
light_red = graphcolor[6]
dark_red = graphcolor[7]
green = c_metron = colors[2]
c_sprayer = colors[6]

m_rss= 'o'
m_rsspp = 'd'

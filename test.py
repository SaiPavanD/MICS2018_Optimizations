from dsatur import *
from monte_carlo import *
from modified_monte_carlo import *
from scipy.sparse import lil_matrix
from timeit import default_timer as timer
from glob import glob

graph = None
g = None

# for iter in xrange(5):
#     print "Iteration number - {}".format(iter + 1)
#     print ""
for f in sorted(glob('./DIMACS_graphs/*1000*.col.txt')):
    with open(f,'r') as fp:
        num_nodes = int(fp.readline())
        graph =  lil_matrix((num_nodes, num_nodes))
        g = nx.Graph()
        g.add_nodes_from(xrange(num_nodes))
        for line in fp:
            (n1, n2) = map(lambda x: int(x) - 1 ,line.split(' '))
            graph[n1, n2] = 1
            graph[n2, n1] = 1
            g.add_edge(n1,n2)

    dsat = dsatur(graph)
    start1 = timer()
    dsat.process()
    end1 = timer()
    print f.split('/')[-1]
    print "DSATUR check - ",
    dsat.check_colors()
    print "DSATUR - {} colors in {} sec".format(max(dsat.get_colors()),end1-start1)

    mc = monte_carlo(graph)
    start2 = timer()
    mc.process()
    end2 = timer()
    print "Monte Carlo check - ",
    mc.check_colors()
    print "Monte Carlo - {} colors in {} sec".format(max(mc.get_colors()),end2-start2)

    mmc = modified_monte_carlo(g)
    start3 = timer()
    mmc.process()
    end3 = timer()
    print "Modified Monte Carlo check - ",
    mmc.check_colors()
    print "Modified Monte Carlo - {} colors in {} sec".format(max(mmc.get_colors()),end3-start3)
    print ""

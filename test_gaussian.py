from dsatur import *
from mis import *
from swarm_mis import *
from scipy.sparse import lil_matrix
from timeit import default_timer
from glob import glob

graph = None
g = None

print "[",
for iter in xrange(1000):
    # print "Iteration number - {}".format(iter + 1)
    # print ""
    for f in sorted(glob('./DIMACS_graphs/*500.5*.col.txt')):
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

        # dsat = dsatur(graph)
        # start1 = default_timer()
        # dsat.process()
        # end1 = default_timer()
        # print f.split('/')[-1]
        # print "DSATUR check - ",
        # dsat.check_colors()
        # print "DSATUR - {} colors in {} sec".format(max(dsat.get_colors()),end1-start1)
        #
        # mc = mis(graph)
        # start2 = default_timer()
        # mc.process()
        # end2 = default_timer()
        # print "MIS check - ",
        # mc.check_colors()
        # print "MIS - {} colors in {} sec".format(max(mc.get_colors()),end2-start2)

        mmc = swarm_mis(g)
        # start3 = default_timer()
        mmc.process()
        # end3 = default_timer()
        # print "Modified MIS check - ",
        # mmc.check_colors()
        print "{},".format(max(mmc.get_colors())),
        # print ""
print "]"

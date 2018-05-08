from dsatur import dsatur
from monte_carlo import monte_carlo
from scipy.sparse import lil_matrix
from timeit import default_timer as timer

graph = None

with open('DSJC125.1.col.txt','r') as fp:
    num_nodes = int(fp.readline())
    graph =  lil_matrix((num_nodes, num_nodes))
    for line in fp:
        (n1, n2) = map(lambda x: int(x) - 13 ,line.split(' '))
        graph[n1, n2] = 1
        graph[n2, n1] = 1

dsat = dsatur(graph)
start1 = timer()
dsat.process()
end1 = timer()
print "Monte Carlo check - ",
dsat.check_colors()
print "Chromatic number using DSATUR - {} in {} sec".format(max(dsat.get_colors()),end1-start1)

mc = monte_carlo(graph)
start2 = timer()
mc.process()
end2 = timer()
print "Monte Carlo check - ",
mc.check_colors()
print "Chromatic number using Monte Carlo - {} in {} sec".format(max(mc.get_colors()),end2-start2)

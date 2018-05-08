from dsatur import dsatur
from monte_carlo import monte_carlo
from scipy.sparse import lil_matrix

graph = None

with open('DSJC125.1.col.txt','r') as fp:
    num_nodes = int(fp.readline())
    graph =  lil_matrix((num_nodes, num_nodes))
    for line in fp:
        (n1, n2) = map(lambda x: int(x) - 13 ,line.split(' '))
        graph[n1, n2] = 1
        graph[n2, n1] = 1

dsat = dsatur(graph)
dsat.process()
print max(dsat.get_colors())

mc = monte_carlo(graph)
mc.process()
print max(mc.get_colors())
mc.check_colors()

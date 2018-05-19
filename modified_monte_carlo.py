from monte_carlo import *
import networkx as nx
from math import ceil
import metis
from itertools import count, ifilterfalse

class modified_monte_carlo(monte_carlo):
    def __init__(self, data):
        if not isinstance(data, nx.Graph):
            raise ValueError('Only networkx graphs are supported.')
        self._data_pointer_nx = data;
        self._data_pointer = nx.to_scipy_sparse_matrix(data)
        self._node_weights = random.sample(range(self._data_pointer.shape[0]), self._data_pointer.shape[0])
        self._colored_nodes = [0] * self._data_pointer.shape[0]
        self._color_count = []
        self._colors = [0] * self._data_pointer.shape[0]
        self._idle_nodes = [0] * self._data_pointer.shape[0]

    def process(self):
        # divide the graph into partitions such that each partition contains around 50 nodes
        (self._edgecuts, self._partitions) = metis.part_graph(self._data_pointer_nx,nparts=int(ceil(self._data_pointer_nx.number_of_nodes()/50.0)))
        self._color_count = [1] * (max(self._partitions)+1)
        # run the monte carlo on each of the partitions
        while(sum(self._colored_nodes) < self._data_pointer.shape[0]):
            self._idle_nodes = [0] * self._data_pointer.shape[0]
            for i in xrange(self._data_pointer.shape[0]):
                if self._colored_nodes[i] == 1:
                    self._idle_nodes[i] = 1
            temp_mis = self._get_mis()
            for i in temp_mis:
                self._colors[i] = self._color_count[self._partitions[i]]
                self._colored_nodes[i] = 1
            self._color_count[self._partitions[i]] += 1
        # merge the colored partitions and resolve any coloring conflicts
        # for node_index in xrange(self._data_pointer.shape[0]):
        #     self._resolve_color_conflicts(node_index)


    def _get_neighbors(self, node_index):
        return [index for index in xrange(self._data_pointer.shape[0]) if self._data_pointer[node_index,index] != 0 and self._idle_nodes[index] == 0 and self._partitions[index] == self._partitions[node_index]]

    def _resolve_color_conflicts(self, node_index):
        for index in xrange(self._data_pointer.shape[0]):
            if self._data_pointer[node_index,index] != 0 and self._partitions[index] != self._partitions[node_index] and self._colors[index] == self._colors[node_index]:
                self._assign_min_color(index, node_index)

    def _assign_min_color(self, node1, node2):
        col_list1 = set([self._colors[node1]])
        col_list2 = set([self._colors[node2]])
        for index in xrange(self._data_pointer.shape[0]):
            if self._data_pointer[node1,index] != 0:
                col_list1.add(self._colors[index])
            if self._data_pointer[node2,index] != 0:
                col_list2.add(self._colors[index])
        col1 = next(ifilterfalse(col_list1.__contains__, count(1)))
        col2 = next(ifilterfalse(col_list2.__contains__, count(1)))
        print node1, node2, self._colors[node1], col1, col2
        if col1 < col2:
            self._colors[node1] = col1
        else:
            self._colors[node2] = col2

    def check_colors(self):
        self._idle_nodes = [0] * self._data_pointer.shape[0]
        count = 0
        for i in xrange(self._data_pointer.shape[0]):
            for j in self._get_neighbors(i):
                if self._colors[i] == self._colors[j]:
                    print "Error at node - {} partition - {}, node - {} partition {} with color {}".format(i,self._partitions[i],j,self._partitions[j], self._colors[i])
                    count+=1
        if(count == 0):
            print "Success"
        return

from mis import *
import networkx as nx
from math import ceil
import metis
from itertools import count, ifilterfalse
from collections import Counter

class swarm_mis(mis):
    def __init__(self, data):
        if not isinstance(data, nx.Graph):
            raise ValueError('Only networkx graphs are supported.')
        self._data_pointer_nx = data;
        self._data_pointer = nx.adjacency_matrix(data)
        self._num_nodes = len(data)
        self._adj_list = data.adjacency_list()
        self._node_weights = random.sample(range(self._num_nodes), self._num_nodes)
        self._colored_nodes = [0] * self._num_nodes
        self._color_count = []
        self._colors = [0] * self._num_nodes
        self._idle_nodes = [0] * self._num_nodes
        self._partition_counts = None

    def process(self):
        # divide the graph into partitions such that each partition contains around 50 nodes
        (self._edgecuts, self._partitions) = metis.part_graph(self._data_pointer_nx,nparts=int(ceil(self._data_pointer_nx.number_of_nodes()/50.0)))
        self._color_count = [1] * (max(self._partitions)+1)
        # run the monte carlo on each of the partitions
        self._partition_counts = Counter(self._partitions)
        for partition_num in xrange(max(self._partitions)+1):
            while(sum([self._colored_nodes[idx] for idx in xrange(self._num_nodes) if self._partitions[idx] == partition_num]) < self._partition_counts[partition_num]):
                # print sum([self._colors[idx] for idx in xrange(self._num_nodes) if self._partitions[idx] == partition_num]), self._partition_counts[partition_num]
                self._idle_nodes = [0] * self._num_nodes
                for i in xrange(self._num_nodes):
                    if self._colored_nodes[i] == 1:
                        self._idle_nodes[i] = 1
                temp_mis = self._get_mis(partition_num)
                for i in temp_mis:
                    self._colors[i] = self._color_count[self._partitions[i]]
                    self._colored_nodes[i] = 1
                self._color_count[self._partitions[i]] += 1
        # merge the colored partitions and resolve any coloring conflicts
        self._resolve_color_conflicts()

    def _get_mis(self, partition_num):
        mis = []
        while (sum([self._idle_nodes[idx] for idx in xrange(self._num_nodes) if self._partitions[idx]==partition_num]) < self._partition_counts[partition_num]):
            temp_is = self._get_is(partition_num)
            for i in temp_is:
                self._idle_nodes[i]=1
                mis += [i]
                for j in self._get_neighbors(i,partition_num):
                    self._idle_nodes[j]=1
        return mis

    def _get_is(self, partition_num):
        ind_set = []
        for node_idx in xrange(self._num_nodes):
            if self._partitions[node_idx] == partition_num:
                if (self._is_local_max(node_idx, partition_num)):
                    ind_set += [node_idx]
        return ind_set

    def _is_local_max(self, node_idx, partition_num):
        if self._idle_nodes[node_idx] == 1:
            return False
        for i in self._get_neighbors(node_idx, partition_num):
            if(self._node_weights[i] >= self._node_weights[node_idx]):
                return False
        return True

    def _get_neighbors(self, node_index, partition_num):
        return [index for index in self._adj_list[node_index] if self._idle_nodes[index] == 0 and self._partitions[index] == partition_num ]

    def _resolve_color_conflicts(self):
        for node_index in xrange(self._num_nodes):
            for idx in self._adj_list[node_index]:
                if self._colors[idx] == self._colors[node_index]:
                        col_list1 = set([self._colors[index] for index in self._adj_list[node_index]])
                        col_list2 = set([self._colors[index] for index in self._adj_list[idx]])
                        col1 = next(ifilterfalse(col_list1.__contains__, count(1)))
                        col2 = next(ifilterfalse(col_list2.__contains__, count(1)))
                        if col1 < col2:
                            self._colors[node_index] = col1
                        else:
                            self._colors[idx] = col2
        return

    def check_colors(self):
        self._idle_nodes = [0] * self._num_nodes
        count = 0
        for i in xrange(self._num_nodes):
            for j in mis._get_neighbors(self,i):
                if self._colors[i] == self._colors[j]:
                    print "Error at node - {} partition - {}, node - {} partition {} with color {}".format(i,self._partitions[i],j,self._partitions[j], self._colors[i])
                    count+=1
        if(count == 0):
            print "Success"
        return

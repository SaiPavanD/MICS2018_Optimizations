import random
import numpy as np

class mis:
    def __init__(self, data):
        try:
            if (data.shape[0] != data.shape[1]):
                raise NameError('Only adjacency matrix graph representation is available.')
        except Exception as e:
            raise ValueError('Only numpy matrix or scipy sparse matrix are supported.')

        self._data_pointer = data;
        self._num_nodes = self._data_pointer.shape[0]
        self._set_adj_list()
        self._node_weights = random.sample(range(self._num_nodes), self._num_nodes)
        self._colored_nodes = [0] * self._num_nodes
        self._color_count = 1
        self._colors = [0] * self._num_nodes
        self._idle_nodes = [0] * self._num_nodes

    def process(self):
        while(sum(self._colored_nodes) < self._num_nodes):
            self._idle_nodes = [0] * self._num_nodes
            for i in xrange(self._num_nodes):
                if self._colored_nodes[i] == 1:
                    self._idle_nodes[i] = 1
            temp_mis = self._get_mis()
            for i in temp_mis:
                self._colors[i] = self._color_count
                self._colored_nodes[i] = 1
            self._color_count += 1
        return

    def _get_mis(self):
        mis = []
        while (sum(self._idle_nodes) < self._num_nodes):
            temp_is = self._get_is()
            for i in temp_is:
                self._idle_nodes[i]=1
                mis += [i]
                for j in self._get_neighbors(i):
                    self._idle_nodes[j]=1
        return mis

    def _get_is(self):
        ind_set = []
        for node_idx in xrange(self._num_nodes):
            if (self._is_local_max(node_idx)):
                ind_set += [node_idx]
        return ind_set

    def _is_local_max(self, node_idx):
        if self._idle_nodes[node_idx] == 1:
            return False
        for i in self._get_neighbors(node_idx):
            if(self._node_weights[i] >= self._node_weights[node_idx]):
                return False
        return True

    def _get_neighbors(self, node_index):
        return [ index for index in self._adj_list[node_index] if  self._idle_nodes[index] == 0];

    def get_colors(self):
        return self._colors

    def check_colors(self):
        self._idle_nodes = [0] * self._num_nodes
        count = 0
        for i in xrange(self._num_nodes):
            for j in self._get_neighbors(i):
                if self._colors[i] == self._colors[j]:
                    print "Error at {}, {} with color {}".format(i,j, self._colors[i])
                    count+=1
        if(count == 0):
            print "Success"
        return

    def _set_adj_list(self):
        self._adj_list = []
        for row in self._data_pointer:
            new_row = row.todense().tolist()[0]
            self._adj_list += [[idx for idx in xrange(self._num_nodes) if new_row[idx]!=0]]
        return

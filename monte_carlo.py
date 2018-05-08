import random
import numpy as np

class monte_carlo:
    def __init__(self, data):
        try:
            if (data.shape[0] != data.shape[1]):
                raise NameError('Only adjacency matrix graph representation is available.')
        except Exception as e:
            raise ValueError('Only numpy matrix or scipy sparse matrix are supported.')

        self.__data_pointer = data;
        self.__node_weights = random.sample(range(self.__data_pointer.shape[0]), self.__data_pointer.shape[0])
        self.__colored_nodes = [0] * self.__data_pointer.shape[0]
        self.__color_count = 1
        self.__colors = [0] * self.__data_pointer.shape[0]
        self.__idle_nodes = [0] * self.__data_pointer.shape[0]

    def process(self):
        while(sum(self.__colored_nodes) < self.__data_pointer.shape[0]):
            self.__idle_nodes = [0] * self.__data_pointer.shape[0]
            for i in xrange(self.__data_pointer.shape[0]):
                if self.__colored_nodes[i] == 1:
                    self.__idle_nodes[i] = 1
            temp_mis = self.__get_mis()
            for i in temp_mis:
                self.__colors[i] = self.__color_count
                self.__colored_nodes[i] = 1
            self.__color_count += 1
        return

    def __get_mis(self):
        mis = []
        while (sum(self.__idle_nodes) < self.__data_pointer.shape[0]):
            temp_is = self.__get_is()
            for i in temp_is:
                self.__idle_nodes[i]=1
                mis += [i]
                for j in self.__get_neighbors(i):
                    self.__idle_nodes[j]=1
        return mis

    def __get_is(self):
        ind_set = []
        for node_idx in xrange(self.__data_pointer.shape[0]):
            if (self.__is_local_max(node_idx)):
                ind_set += [node_idx]
        return ind_set

    def __is_local_max(self, node_idx):
        if self.__idle_nodes[node_idx] == 1:
            return False
        for i in self.__get_neighbors(node_idx):
            if(self.__node_weights[i] >= self.__node_weights[node_idx]):
                return False
        return True

    def __get_neighbors(self, node_index):
        return [ index for index in xrange(self.__data_pointer.shape[0]) if self.__data_pointer[node_index,index] != 0 and self.__idle_nodes[index] == 0];

    def get_colors(self):
        return self.__colors

    def check_colors(self):
        self.__idle_nodes = [0] * self.__data_pointer.shape[0]
        count = 0
        for i in xrange(self.__data_pointer.shape[0]):
            for j in self.__get_neighbors(i):
                if self.__colors[i] == self.__colors[j]:
                    print "Error at {}, {}".format(i,j)
                    count+=1
        if(count == 0):
            print "Success"
        return

'''
Created on Feb 11, 2016

@author: Alex
'''
import math
from simanneal import Annealer
import copy
import random
from mutable_float import MutableFloat
from coordination import the_whole_enchilada

def find_entropy(all_line_segs):
    def _get_neighbors(seg):
        return seg.get_num_neighbors() + 1
    
    sum_total_neighborhood_size = reduce(lambda x, y: x + y, \
                                         map(_get_neighbors, all_line_segs))
    
    def _probability_func(line_seg, sum_total_neighborhood_size):
        return _get_neighbors(line_seg) * 1.0 / sum_total_neighborhood_size
    
    def _single_entry_entropy(line_seg):
        prob_value = _probability_func(line_seg, sum_total_neighborhood_size)
        return prob_value * math.log(prob_value, 2)
    
    return -1 * reduce(lambda x, y: x + y, map(_single_entry_entropy, all_line_segs))

class TraclusSimulatedAnnealingState:
    def __init__(self, input_trajectories, epsilon):
        if epsilon < 0.0:
            raise ValueError("can't have a negative epsilon")
        
        Annealer.copy_strategy = 'method'
        self.input_trajectories = input_trajectories
        self.epsilon = epsilon
        self.entropy = None
        
    def get_epsilon(self):
        return self.epsilon
    
    def get_input_trajectories(self):
        return self.input_trajectories
    
    def get_entropy(self):
        if self.entropy == None:
            raise Exception()
        return self.entropy
    
    def compute_entropy(self, clusters):
        all_line_segs = []
        for single_cluster in clusters:
            all_line_segs.extend(single_cluster.get_trajectory_line_segments())
        self.entropy = find_entropy(all_line_segs=all_line_segs)
    
    def copy(self):
        return TraclusSimulatedAnnealingState(self.input_trajectories, self.epsilon)

class TraclusSimulatedAnnealer(Annealer):
    def __init__(self, initial_state, max_epsilon_step_change):
        self.max_epsilon_step_change = max_epsilon_step_change
        Annealer.__init__(self, initial_state=initial_state)
    
    def move(self):
        new_epsilon = max(0.0, self.state.get_epsilon() + \
        random.uniform(-self.max_epsilon_step_change, self.max_epsilon_step_change))
        self.state = TraclusSimulatedAnnealingState(self.state.input_trajectories, \
                                              new_epsilon)
        
    def energy(self):
        the_whole_enchilada(point_iterable_list=self.state.get_input_trajectories(), \
                            epsilon=self.state.get_epsilon(), \
                            min_neighbors=0, \
                            min_num_trajectories_in_cluster=1, \
                            min_vertical_lines=100, \
                            min_prev_dist=100, \
                            clusters_hook=self.state.compute_entropy)
        return self.state.get_entropy()
        
        

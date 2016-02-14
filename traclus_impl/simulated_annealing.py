'''
Created on Feb 13, 2016

@author: Alex
'''
'''
Created on Feb 13, 2016

@author: Alex
'''
import math
from random import random

class SimulatedAnnealingState:
    def __init__(self):
        pass
    
    def get_energy(self):
        raise NotImplementedError()
    
    def get_random_neighbor(self):
        raise NotImplementedError()

def anneal_step(steps_per_temp, cur_step, \
                max_temp, min_temp, prev_state, new_state, \
                find_next_state_func):
    t_factor = -1 * math.log(max_temp / min_temp * 1.0)
    temp = max_temp * math.exp(t_factor * cur_step / steps_per_temp)
    energy_diff = new_state.get_energy() - prev_state.get_energy()
    rand_val = random()
    print rand_val
    print math.exp(-energy_diff / temp)
    print "----"
    
    if energy_diff > 0.0 and math.exp(-energy_diff / temp) < rand_val:
        cur_state = prev_state
    else:
        cur_state = new_state
        
    return find_next_state_func(steps_per_temp, cur_step + 1, \
                          max_temp, min_temp, cur_state)
        
    
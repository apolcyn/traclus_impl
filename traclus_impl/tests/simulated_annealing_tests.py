'''
Created on Feb 13, 2016

@author: Alex
'''
import unittest
from traclus_impl.simulated_annealing import anneal_step
from traclus_impl.simulated_annealing import SimulatedAnnealingState
import random

class SimulatedAnnealingTest(unittest.TestCase):
                
    def find_next_state_func(self, steps_per_temp, cur_step, \
                          max_temp, min_temp, cur_state):
        if steps_per_temp == cur_step:
            return cur_state
        
        next_state = cur_state.get_random_neighbor()
        return anneal_step(steps_per_temp, cur_step, \
                    max_temp, min_temp, prev_state=cur_state, \
                    new_state=next_state, \
                    find_next_state_func=self.find_next_state_func)
        
    
    def test_always_moves_towards_lower_energy_when_possible(self):
        class MockSimAnnealingState(SimulatedAnnealingState):
            def __init__(self, val):
                SimulatedAnnealingState.__init__(self)
                self.val = val
                
            def get_energy(self):
                return self.val
                
            def get_random_neighbor(self):
                return MockSimAnnealingState(self.val - 1)
        
        initial_state = MockSimAnnealingState(10)
        final_state = anneal_step(steps_per_temp=10, cur_step=0, max_temp=1000, min_temp=2.5, \
                    prev_state=initial_state, new_state=initial_state, \
                    find_next_state_func=self.find_next_state_func)
        
        self.assertEqual(final_state.get_energy(), 1)
        
    def test_goes_to_higher_energy_when_temparature_at_max(self):
        class MockState(SimulatedAnnealingState):
            def __init__(self, val):
                SimulatedAnnealingState.__init__(self)
                self.val = val
                
            def get_energy(self):
                return self.val
            
            def get_random_neighbor(self):
                if self.val % 2 == 0:
                    return MockState(self.val - 3)
                else:
                    return MockState(self.val + 1)
            
        initial_state = MockState(9)
        final_state = anneal_step(steps_per_temp=3, cur_step=0, max_temp=1000, \
                                  min_temp=1, prev_state=initial_state, \
                                  new_state=initial_state, \
                                  find_next_state_func=self.find_next_state_func)
        self.assertEquals(final_state.get_energy(), 7)
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
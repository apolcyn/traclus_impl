'''
Created on Feb 14, 2016

@author: Alex
'''
import unittest
from traclus_impl.parameter_estimation import TraclusSimulatedAnnealingState
from traclus_impl.parameter_estimation import TraclusSimulatedAnnealer
from traclus_impl.geometry import Point

""" These tests might just take a few tries to pass. Simulated Annealing results
rely on some luck with random numbers, but should usually work. """
class SimulatedAnnealingTest(unittest.TestCase):

    def test_simulated_annealing_doesnt_blow_up(self):
        input_trajectories = [[Point(0, 0), Point(0, 1)], \
                              [Point(2, 0), Point(2, 1)], \
                              [Point(3, 0), Point(3, 1)]]
        initial_state = TraclusSimulatedAnnealingState(input_trajectories=input_trajectories, \
                                                       epsilon=0.5)
        traclus_sim_anneal = TraclusSimulatedAnnealer(initial_state=initial_state, \
                                                      max_epsilon_step_change=0.1)
        traclus_sim_anneal.updates = 0
        traclus_sim_anneal.steps = 5000
        best_state, best_energy = traclus_sim_anneal.anneal()
        self.assertAlmostEqual(best_state.get_epsilon(), 1.0, delta=0.7)
        
    def test_simulated_annealing_finds_good_solution_quickly(self):
        input_trajectories = [[Point(0, 0), Point(0, 1)], \
                              [Point(2, 0), Point(2, 1)], \
                              [Point(3, 0), Point(3, 1)]]
        initial_state = TraclusSimulatedAnnealingState(input_trajectories=input_trajectories, \
                                                       epsilon=0.7)
        traclus_sim_anneal = TraclusSimulatedAnnealer(initial_state=initial_state, \
                                                      max_epsilon_step_change=0.3)
        traclus_sim_anneal.updates = 0
        traclus_sim_anneal.steps = 50
        best_state, best_energy = traclus_sim_anneal.anneal()
        self.assertAlmostEqual(best_state.get_epsilon(), 1.0, delta=0.5)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
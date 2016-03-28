'''
Created on Mar 26, 2016

@author: Alex
'''
import json
import unittest
import os

from traclus_impl.coordination import the_whole_enchilada, run_traclus
from traclus_impl.geometry import Point
from traclus_impl.main import parse_input_and_run_traclus

class CampusTraclusTest(unittest.TestCase):
    INPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                              'raw_campus_trajectories.txt')
    OUTPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'campus_trajectories_traclus_output.txt')
    PARTITIONING_OUTPUT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'partitioned_stage_output.txt')
    CLUSTERS_OUTPUT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'clusters_output.txt')
    NUM_EXPECTED_TRAJECTORIES = 4
    
    def setUp(self):        
        self.expected_output = \
        self.read_trajectory_lists_from_file_input(CampusTraclusTest.OUTPUT_FILE)       
        
    def read_trajectory_lists_from_file_input(self, file_name):
        parsed_input = None
        
        with open(file_name, 'r') as raw_input:
            parsed_input = json.loads(raw_input.read())
            
        trajectory_list = parsed_input['trajectories']
        
        traclus_input = []
        for point_list in trajectory_list:
            traclus_traj_input = []
            for point_dict in point_list:
                traclus_traj_input.append(Point(**point_dict))
            traclus_input.append(traclus_traj_input)
        return traclus_input
    
    def trajectory_is_expected(self, trajectory):
        match = None
        for other_traj in self.expected_output:
            if trajectory == other_traj:
                match = other_traj
                break
        if match == None:
            return False
        
        self.expected_output.remove(match)
        return True

    def test_parses_input_and_traclus_result_is_correct(self):
        actual = parse_input_and_run_traclus(input_file=CampusTraclusTest.INPUT_FILE, 
                                             partitioned_trajectories_output_file_name=CampusTraclusTest.PARTITIONING_OUTPUT, 
                                             clusters_output_file_name=CampusTraclusTest.CLUSTERS_OUTPUT)
        
        self.assertEquals(CampusTraclusTest.NUM_EXPECTED_TRAJECTORIES, len(actual))
        for traj in actual:
            self.assertTrue(self.trajectory_is_expected(traj))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
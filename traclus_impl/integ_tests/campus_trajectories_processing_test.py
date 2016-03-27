'''
Created on Mar 26, 2016

@author: Alex
'''
import json
import unittest
import os

from traclus_impl.coordination import the_whole_enchilada, run_traclus
from traclus_impl.geometry import Point


class CampusTraclusTest(unittest.TestCase):
    EPSILON = 0.00016
    MIN_NEIGHBORS = 2
    MIN_NUM_TRAJECTORIES_IN_CLUSTER = 3
    MIN_VERTICAL_LINES = 2
    MIN_PREV_DIST = 0.0002
    
    NUM_EXPECTED_TRAJECTORIES = 4
    
    def setUp(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        input_file_name = \
        os.path.join(current_dir, 'raw_campus_trajectories.txt')
        expected_output_file_name = \
        os.path.join(current_dir, 'campus_trajectories_traclus_output.txt')
        
        self.raw_input = \
        self.read_trajectory_lists_from_file_input(input_file_name)
        self.expected_output = \
        self.read_trajectory_lists_from_file_input(expected_output_file_name)       
        
    def read_trajectory_lists_from_file_input(self, file_name):
        parsed_input = None
        
        with open(file_name, 'r') as raw_input:
            parsed_input = json.loads(raw_input.read())
            
        trajectory_list = parsed_input['trajectories']
        
        traclus_input = []
        for point_list in trajectory_list:
            traclus_traj_input = []
            for point_dict in point_list:
                traclus_traj_input.append(Point(point_dict['lat'], \
                                                point_dict['lng']))
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

    def test_traclus_result_is_correct(self):
        actual = run_traclus(point_iterable_list=self.raw_input, \
                                  epsilon=CampusTraclusTest.EPSILON, \
                                  min_neighbors=CampusTraclusTest.MIN_NEIGHBORS, \
                                  min_num_trajectories_in_cluster=CampusTraclusTest.MIN_NUM_TRAJECTORIES_IN_CLUSTER, \
                                  min_vertical_lines=CampusTraclusTest.MIN_VERTICAL_LINES, \
                                  min_prev_dist=CampusTraclusTest.MIN_PREV_DIST)
        
        self.assertEquals(CampusTraclusTest.NUM_EXPECTED_TRAJECTORIES, len(actual))
        for traj in actual:
            self.assertTrue(self.trajectory_is_expected(traj))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Feb 20, 2016

@author: Alex
'''
import unittest
from traclus_impl.processed_trajectory_connecting import compute_shortest_path


class FilteredTrajectoryGraphPathFindingTest(unittest.TestCase):
    class MockPtNode:
        def __init__(self, neighbors):
            self.neighbors = neighbors
        def get_neighbor_indices(self):
            return self.neighbors   

    def test_compute_shortest_path_in_completely_connected_graph(self):
        def dummy_pt_pt_distance_func(a_index, b_index, pt_graph):
            distances = [[0, 1, 2, 3], \
                     [1, 0, 2, 1], \
                     [2, 2, 0, 3], \
                     [3, 1, 3, 0]]
            return distances[a_index][b_index]    

        pt_graph = [self.MockPtNode([1, 2, 3]), \
                    self.MockPtNode([0, 2, 3]), \
                    self.MockPtNode([0, 1, 3]), \
                    self.MockPtNode([0, 1, 2])]
        
        start_index = 0
        end_index = 3
        expected_path = [0, 1, 3]
        expected_dist = 2.0
        
        actual_path, actual_dist = compute_shortest_path(start_node_index=start_index, \
                                                         end_node_index=end_index, \
                                                         pt_graph=pt_graph, \
                                                         pt_pt_distance_func=dummy_pt_pt_distance_func)
        self.assertEquals(expected_dist, actual_dist)
        self.assertListEqual(expected_path, actual_path)
        
    def test_returns_none_when_there_is_no_path(self):
        def dummy_pt_pt_distance_func(a_index, b_index, pt_graph):
            distances = [[0, 1, 2, None], \
                     [1, 0, 2, None], \
                     [2, 2, 0, None], \
                     [None, None, None, None]]
            return distances[a_index][b_index]  
        
        pt_graph = [self.MockPtNode([1, 2]), \
                    self.MockPtNode([0, 2]), \
                    self.MockPtNode([0, 1]), \
                    self.MockPtNode([])] 
        
        start_index = 0
        end_index = 3
        
        actual_path, actual_dist = compute_shortest_path(start_node_index=start_index, \
                                                         end_node_index=end_index, \
                                                         pt_graph=pt_graph, \
                                                         pt_pt_distance_func=dummy_pt_pt_distance_func)
        self.assertEquals(None, actual_path)
        self.assertEquals(None, actual_dist)
               
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Feb 22, 2016

@author: Alex
'''
import unittest
from traclus_impl.processed_trajectory_connecting import find_all_possible_connections

class ProcessedTrajectoryShortestConnectionTest(unittest.TestCase):
    class MockPtNode:
        def __init__(self, index, component_id):
            self.graph_component_id = component_id
            self.point = index
            self.index = index
            
    def verify_lists_equal_order_doesnt_matter(self, list_a, list_b):
        self.assertEquals(len(list_a), len(list_b), \
                          "lists differ. list a: " + str(list_a) + \
                          "list b: " + str(list_b))
        b_set = set()
        for item in list_b:
            b_set.add(item)
        for item in list_a:
            self.assertTrue(item in b_set)

    def test_finds_all_possible_connections(self):
        pt_graph = [self.MockPtNode(0, 0), \
                    self.MockPtNode(1, 1), \
                    self.MockPtNode(2, 2), \
                    self.MockPtNode(3, 0), \
                    self.MockPtNode(4, 0)]
                
        def dummy_pt_pt_distance_func(a_index, b_index):
            distances = [[0.5, 0.5, 0.5, 1.5, 1.5], \
                         None, \
                         None, \
                         None, \
                         [1.5, 1.5, 0.5, 0.5, 0.5]]
            return distances[a_index][b_index]
        
        start_pt = 0
        end_pt = 4
        max_dist_to_existing_pt = 1.0
        
        expected_connections = [(0, 3), (0, 4), (2, 2)]
        
        actual_connections = find_all_possible_connections(start_pt=start_pt, \
                                                           end_pt=end_pt, \
                                                           pt_graph=pt_graph, \
                                                           distance_func=dummy_pt_pt_distance_func, \
                                                           max_dist_to_existing_pt=max_dist_to_existing_pt)
        self.verify_lists_equal_order_doesnt_matter(expected_connections, \
                                                    actual_connections)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
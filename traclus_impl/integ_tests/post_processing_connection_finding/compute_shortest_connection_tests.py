'''
Created on Feb 22, 2016

@author: Alex
'''
import unittest
from traclus_impl.geometry import Point
from traclus_impl.processed_trajectory_connecting import FilteredTrajectory, \
    compute_graph_component_ids, find_shortest_connection, \
     build_point_graph, get_find_other_nearby_neighbors_func
from traclus_impl.tests.unit_base_tests import UnitBaseTests

class ComputeShortestConnectionTest(UnitBaseTests):

    def test_computes_shortest_connection_correctly(self):
        trajectories = [[Point(1, 2), Point(2, 2)], \
                        [Point(1, 3), Point(2, 3)], \
                        [Point(1, 4), Point(2, 4), Point(3, 4), Point(4, 4)], \
                        [Point(4, 3), Point(5, 3)], \
                        [Point(4, 2), Point(5, 2)], \
                        [Point(1, 5), Point(1, 6)], \
                        [Point(7, 4), Point(8, 4)], \
                        [Point(7, 5), Point(8, 5)]]
        filtered = []
        cur_index = 0
        for traj in trajectories:
            filtered.append(FilteredTrajectory(traj, cur_index))
            cur_index += 1
            
        max_distance_for_neighbors_in_different_trajectories = 1.0
        other_neighbors_func = get_find_other_nearby_neighbors_func(max_distance_for_neighbors_in_different_trajectories)

        pt_graph = build_point_graph(filtered, add_other_neigbors_func=other_neighbors_func)
        
        expected_neighbor_indices = [[1, 2], \
                                     [0, 3], \
                                     [0, 3, 4], \
                                     [1, 2, 5], \
                                     [2, 5, 12], \
                                     [3, 4, 6], \
                                     [5, 7], \
                                     [6, 8], \
                                     [7, 9, 10], \
                                     [8, 11], \
                                     [8, 11], \
                                     [9, 10], \
                                     [4, 13], \
                                     [12], \
                                     [15, 16], \
                                     [14, 17], \
                                     [14, 17], \
                                     [15, 16]]
        
        for pt_node in pt_graph:
            for i in expected_neighbor_indices[pt_node.index]:
                self.assertTrue(i in pt_node.get_neighbor_indices(), "node index " + \
                                str(i) + " is not in node index " + str(pt_node.index) + \
                                " neighbor list")
        
        find_other_neighbors_func = \
        get_find_other_nearby_neighbors_func(max_distance_for_neighbors_in_different_trajectories)
        
        def dummy_find_other_neighbors_func(pt_node, pt_graph):
            return []
        
        compute_graph_component_ids(pt_graph=pt_graph, \
                                    find_other_neighbors_func=dummy_find_other_neighbors_func)
        
        start_pt = Point(1.5, 2.5)
        end_pt = Point(4.5, 2.5)
        max_dist_to_existing_pt = 0.9
        
        actual_shortest_connection, actual_shortest_distance = find_shortest_connection(start_pt=start_pt, \
                                                                          end_pt=end_pt, \
                                                                          pt_graph=pt_graph, \
                                                                          max_dist_to_existing_pt=max_dist_to_existing_pt)
        
        expected_shortest_connection = [Point(2, 3), \
                                        Point(2, 4), \
                                        Point(3, 4), \
                                        Point(4, 4), \
                                        Point(4, 3)]
        
        # Note that the shortest path distance and calculation ignores
        # the initial distance to a point on the map
        expected_shortest_distance = 4.0
        
        self.assertEquals(len(expected_shortest_connection), len(actual_shortest_connection))
        exp_iter = iter(expected_shortest_connection)
        actual_iter = iter(actual_shortest_connection)
                        
        for exp_pt in exp_iter:
            act_pt = actual_iter.next()
            self.assertEquals(exp_pt.x, act_pt.x)
            self.assertEquals(exp_pt.y, act_pt.y)
            
        self.assertEquals(expected_shortest_distance, actual_shortest_distance)
        
    def test_returns_none_none_when_no_possible_connections(self):            
        max_distance_for_neighbors_in_different_trajectories = 1.0
        other_neighbors_func = get_find_other_nearby_neighbors_func(max_distance_for_neighbors_in_different_trajectories)

        pt_graph = build_point_graph([], add_other_neigbors_func=other_neighbors_func)
        
        def dummy_find_other_neighbors_func(pt_node, pt_graph):
            return []
        
        compute_graph_component_ids(pt_graph=pt_graph, \
                                    find_other_neighbors_func=dummy_find_other_neighbors_func)
        
        start_pt = Point(1.5, 2.5)
        end_pt = Point(4.5, 2.5)
        max_dist_to_existing_pt = 0.9
        
        actual_shortest_connection, actual_shortest_distance = find_shortest_connection(start_pt=start_pt, \
                                                                          end_pt=end_pt, \
                                                                          pt_graph=pt_graph, \
                                                                          max_dist_to_existing_pt=max_dist_to_existing_pt)
        
        self.assertEquals(actual_shortest_connection, None)    
        self.assertEquals(actual_shortest_distance, None)        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
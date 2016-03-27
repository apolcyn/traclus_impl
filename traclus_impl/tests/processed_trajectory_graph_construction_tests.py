'''
Created on Feb 20, 2016

@author: Alex
'''
import unittest
from traclus_impl.geometry import Point
from traclus_impl.processed_trajectory_connecting import FilteredTrajectory,\
    build_point_graph, compute_graph_component_ids
from unit_base_tests import UnitBaseTests

class FilteredPointGraphConstructionTest(UnitBaseTests):
    
    def verify_pt_graph(self, trajectories, expected_neighbors, \
                        expected_trajectory_ids, pt_graph):
        flattened_trajs = []
        for traj in trajectories:
            flattened_trajs.extend(traj)
        
        cur_index = 0
        for pt_node in pt_graph:
            self.assertEquals(pt_node.get_original_trajectory_id(), \
                              expected_trajectory_ids[cur_index])
            self.assertEquals(len(expected_neighbors[cur_index]), \
                              len(pt_node.get_neighbor_indices()))
            for index in pt_node.get_neighbor_indices():
                self.assertTrue(index in expected_neighbors[cur_index])
            self.assertEquals(flattened_trajs[cur_index], pt_node.point)
            self.assertEquals(pt_node.index, cur_index)
            self.assertEquals(pt_node.graph_component_id, None)
            cur_index += 1
            
    def test_builds_point_graph_correctly(self):
        trajectories = [[Point(0, 0), Point(1, 1), Point(2, 2)], \
                        [Point(10, 0), Point(11, 0), Point(12, 0)], \
                        [Point(0, 10), Point(0, 11), Point(0, 12)]]
        filtered_trajs = []
        cur_index = 0
        for traj in trajectories:
            filtered_trajs.append(FilteredTrajectory(traj, cur_index))
            cur_index += 1
        
        pt_graph = build_point_graph(filtered_trajectories=filtered_trajs)
        
        expected_neighbors = [set([1]), set([0, 2]), set([1]), \
                              set([4]), set([3, 5]), set([4]), \
                              set([7]), set([6, 8]), set([7])]
        expected_trajectory_ids = [0, 0, 0, \
                                   1, 1, 1, \
                                   2, 2, 2]
        self.verify_pt_graph(trajectories=trajectories, \
                        expected_neighbors=expected_neighbors, \
                        expected_trajectory_ids=expected_trajectory_ids, \
                        pt_graph=pt_graph)
        
    def test_builds_graph_correctly_with_empty_trajectories(self):
        trajectories = [[], \
                        [Point(0, 0), Point(1, 1), Point(2, 2)], \
                        [], \
                        [Point(10, 0), Point(11, 0), Point(12, 0)], \
                        [Point(0, 10), Point(0, 11), Point(0, 12)], \
                        []]  
        filtered_trajs = []
        cur_index = 0
        for traj in trajectories:
            if len(traj) > 0:
                filtered_trajs.append(FilteredTrajectory(traj, cur_index))
                cur_index += 1
        
        pt_graph = build_point_graph(filtered_trajectories=filtered_trajs)
        
        expected_neighbors = [set([1]), set([0, 2]), set([1]), \
                              set([4]), set([3, 5]), set([4]), \
                              set([7]), set([6, 8]), set([7])]
        expected_trajectory_ids = [0, 0, 0, \
                                   1, 1, 1, \
                                   2, 2, 2]
        self.verify_pt_graph(trajectories=trajectories, \
                        expected_neighbors=expected_neighbors, \
                        expected_trajectory_ids=expected_trajectory_ids, \
                        pt_graph=pt_graph)     
        
    def test_computes_components_correctly_when_all_in_same_component(self):
        trajectories = [[], \
                        [Point(0, 0), Point(1, 1), Point(2, 2)], \
                        [], \
                        [Point(10, 0), Point(11, 0), Point(12, 0)], \
                        [Point(0, 10), Point(0, 11), Point(0, 12)], \
                        []]  
        filtered_trajs = []
        cur_index = 0
        for traj in trajectories:
            if len(traj) > 0:
                filtered_trajs.append(FilteredTrajectory(traj, cur_index))
                cur_index += 1
        
        pt_graph = build_point_graph(filtered_trajectories=filtered_trajs)
        
        def dummy_find_other_neighbors_func(pt_node, pt_graph):
            other_neighbors_table = [[3], [], [], [0], [], [6], [5], [], []]
            return other_neighbors_table[pt_node.index]
        
        compute_graph_component_ids(pt_graph=pt_graph, \
                                    find_other_neighbors_func=dummy_find_other_neighbors_func)
        
        expected_component_ids = [0] * 9
        for pt_node in pt_graph:
            self.assertEquals(pt_node.graph_component_id, \
                              expected_component_ids[pt_node.index], \
                              "pt node comp id at index " + str(pt_node.index) + \
                              " is " + str(pt_node.graph_component_id) + \
                              " but expected " + \
                              str(expected_component_ids[pt_node.index]))
            
    def test_computes_components_correctly_when_multiple_components(self):
        trajectories = [[], \
                        [Point(0, 0), Point(1, 1), Point(2, 2)], \
                        [], \
                        [Point(10, 0), Point(11, 0), Point(12, 0)], \
                        [Point(0, 10), Point(0, 11), Point(0, 12)], \
                        []]  
        filtered_trajs = []
        cur_index = 0
        for traj in trajectories:
            if len(traj) > 0:
                filtered_trajs.append(FilteredTrajectory(traj, cur_index))
                cur_index += 1
        
        pt_graph = build_point_graph(filtered_trajectories=filtered_trajs)
        
        def dummy_find_other_neighbors_func(pt_node, pt_graph):
            other_neighbors_table = [[3], [], [], [], [], [], [], [], []]
            return other_neighbors_table[pt_node.index]
        compute_graph_component_ids(pt_graph=pt_graph, \
                                    find_other_neighbors_func=dummy_find_other_neighbors_func)
        
        expected_component_ids = [0] * 6
        expected_component_ids.extend([1] * 3)
        for pt_node in pt_graph:
            self.assertEquals(pt_node.graph_component_id, \
                              expected_component_ids[pt_node.index], \
                              "pt node comp id at index " + str(pt_node.index) + \
                              " is " + str(pt_node.graph_component_id) + \
                              " but expected " + \
                              str(expected_component_ids[pt_node.index]))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
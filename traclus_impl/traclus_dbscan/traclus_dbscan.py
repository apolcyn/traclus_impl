'''
Created on Dec 31, 2015

@author: Alex
'''
from traclus_impl.generic_dbscan import Cluster, ClusterCandidate, ClusterFactory
from traclus_impl.distance_functions import perpendicular_distance, angular_distance, parrallel_distance

class TrajectoryLineSegmentFactory():
    def new_trajectory_line_seg(self, line_segment, trajectory_id):
        if line_segment == None or trajectory_id == None or trajectory_id < 0:
            raise Exception("invalid arguments")
        return TrajectoryLineSegment(line_segment=line_segment, trajectory_id=trajectory_id)

class TrajectoryLineSegment(ClusterCandidate):
    def __init__(self, line_segment, trajectory_id, position_in_trajectory=None):
        ClusterCandidate.__init__(self)
        if line_segment == None or trajectory_id < 0:
            raise Exception
        
        self.line_segment = line_segment
        self.trajectory_id = trajectory_id
        self.position_in_trajectory = position_in_trajectory
        
    def distance_to_candidate(self, other_candidate):
        if other_candidate == None or other_candidate.line_segment == None or self.line_segment == None:
            raise Exception()
        return perpendicular_distance(self.line_segment, other_candidate.line_segment) + \
            angular_distance(self.line_segment, other_candidate.line_segment) + \
            parrallel_distance(self.line_segment, other_candidate.line_segment)

class TrajectoryCluster(Cluster):
    def __init__(self):
        Cluster.__init__(self)
        self.trajectories = set()
        self.trajectory_count = 0
        
    def add_member(self, item):
        Cluster.add_member(self, item)
        if not (item.trajectory_id in self.trajectories):
            self.trajectory_count += 1
            self.trajectories.add(item.trajectory_id)
        
    def num_trajectories_contained(self):
        return self.trajectory_count
    
    def get_trajectory_line_segments(self):
        return self.members
    
class TrajectoryClusterFactory(ClusterFactory):
    def new_cluster(self):
        return TrajectoryCluster()
    
    
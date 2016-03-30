'''
Created on Dec 31, 2015

@author: Alex
'''
from distance_functions import perpendicular_distance, angular_distance, parrallel_distance
from generic_dbscan import Cluster, ClusterCandidate, ClusterFactory, ClusterCandidateIndex

class TrajectoryLineSegmentFactory():
    def __init__(self):
        self.next_traj_line_seg_id = 0
        
    def new_trajectory_line_seg(self, line_segment, trajectory_id):
        if line_segment == None or trajectory_id == None or trajectory_id < 0:
            raise Exception("invalid arguments")
        next_id = self.next_traj_line_seg_id
        self.next_traj_line_seg_id += 1
        return TrajectoryLineSegment(line_segment=line_segment, 
                                     trajectory_id=trajectory_id, 
                                     id=next_id)

class TrajectoryLineSegment(ClusterCandidate):
    def __init__(self, line_segment, trajectory_id, position_in_trajectory=None, 
                 id=None):
        ClusterCandidate.__init__(self)
        if line_segment == None or trajectory_id < 0:
            raise Exception
        
        self.line_segment = line_segment
        self.trajectory_id = trajectory_id
        self.position_in_trajectory = position_in_trajectory
        self.num_neighbors = -1
        self.id = id
        
    def get_num_neighbors(self):
        if self.num_neighbors == -1:
            raise Exception("haven't counted num neighbors yet")
        return self.num_neighbors
    
    def set_num_neighbors(self, num_neighbors):
        if self.num_neighbors != -1 and self.num_neighbors != num_neighbors:
            raise Exception("neighbors count should never be changing")
        self.num_neighbors = num_neighbors
        
    def distance_to_candidate(self, other_candidate):
        if other_candidate == None or other_candidate.line_segment == None or self.line_segment == None:
            raise Exception()
        return perpendicular_distance(self.line_segment, other_candidate.line_segment) + \
            angular_distance(self.line_segment, other_candidate.line_segment) + \
            parrallel_distance(self.line_segment, other_candidate.line_segment)
            
class TrajectoryLineSegmentCandidateIndex(ClusterCandidateIndex):
    def __init__(self, candidates, epsilon):
        ClusterCandidateIndex.__init__(self, candidates, epsilon)
        
    def find_neighbors_of(self, cluster_candidate):
        neighbors = ClusterCandidateIndex.find_neighbors_of(self, cluster_candidate)
        cluster_candidate.set_num_neighbors(len(neighbors))
        return neighbors

class RtreeTrajectoryLineSegmentCandidateIndex(ClusterCandidateIndex):
    def __init__(self, candidates, epsilon):
        ClusterCandidateIndex.__init__(self, candidates, epsilon)
        self.candidates_by_ids = [None] * len(candidates)
        self.idx = index.Index()
        for cluster_candidate in candidates:
            if self.candidates_by_ids[cluster_candidate.id] != None:
                raise Exception("should have all unique ids")
            
            self.candidates_by_ids[cluster_candidate.id] = cluster_candidate
            line_seg = cluster_candidate.line_segment
            bounding_box = self.get_bounding_box_of_line_segment(line_seg)
            self.idx.insert(cluster_candidate.id, bounding_box, cluster_candidate)

    def find_neighbors_of(self, cluster_candidate):
        bounding_box = \
        self.get_bounding_box_of_line_segment(cluster_candidate.line_segment)
        possible_neighbor_ids = [n for n in self.idx.intersection(bounding_box)]
        actual_neighbors = []
        
        for id in possible_neighbor_ids:
            if id == None:
                raise Exception("ids on these need to be set")
            if id != cluster_candidate.id and \
            cluster_candidate.distance_to_candidate(self.candidates_by_ids[id]) <= \
            self.epsilon:
                actual_neighbors.append(self.candidates_by_ids[id])
                
        cluster_candidate.set_num_neighbors(len(actual_neighbors))
        return actual_neighbors 

    def get_bounding_box_of_line_segment(self, line_seg):
        btm = min(line_seg.start.y, line_seg.end.y) - self.epsilon
        top = max(line_seg.start.y, line_seg.end.y) + self.epsilon
        left = min(line_seg.start.x, line_seg.end.x) - self.epsilon
        right = max(line_seg.start.x, line_seg.end.x) + self.epsilon
        return (left, btm, right, top)

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

# Use an r tree index for line segments during dbscan if it's available, 
# otherwise use the pure python n squared dbscan.
BestAvailableClusterCandidateIndex = None
import sys, os
try:
    from rtree import index
    BestAvailableClusterCandidateIndex = RtreeTrajectoryLineSegmentCandidateIndex
    sys.stderr.write(str(os.path.realpath(__file__)) + ": rtree import succeeded." + \
                     " Using an r-tree for clustering")
except ImportError:
    BestAvailableClusterCandidateIndex = TrajectoryLineSegmentCandidateIndex
    sys.stderr.write(str(os.path.realpath(__file__)) + ": rtree import failed." + \
                     " Using plain python quadratic clustering")
    
    

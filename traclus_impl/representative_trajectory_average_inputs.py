'''
Created on Jan 1, 2016

@author: Alex
'''
from linked_list import LinkedList
from linked_list import LinkedListNode
from operator import attrgetter

DECIMAL_MAX_DIFF_FOR_EQUALITY = 0.0000001

class TrajectoryLineSegmentEndpoint:
    def __init__(self, horizontal_position, line_segment, line_segment_id, list_node):
        self.horizontal_position = horizontal_position
        self.line_segment = line_segment
        self.line_segment_id = line_segment_id
        self.list_node = list_node

def get_sorted_line_seg_endpoints(trajectory_line_segments):
    line_segment_endpoints = []
    cur_id = 0

    for traj_segment in trajectory_line_segments:
        list_node = LinkedListNode(traj_segment)
        line_segment_endpoints.append(TrajectoryLineSegmentEndpoint(traj_segment.line_segment.start.x, \
                                                                    traj_segment, cur_id, list_node))
        line_segment_endpoints.append(TrajectoryLineSegmentEndpoint(traj_segment.line_segment.end.x, \
                                                                    traj_segment, cur_id, list_node))
        cur_id += 1
        
    return sorted(line_segment_endpoints, key=attrgetter('horizontal_position'))

def numbers_within(a, b, max_diff):
    return abs(a - b) <= max_diff
    

def possibly_append_to_active_list(active_list, out, prev_pos, min_prev_dist, min_lines):
    if (len(out) == 0 or prev_pos - out[len(out) - 1]['horizontal_position'] >= min_prev_dist) and len(active_list) >= min_lines:
        temp = []
        for line_seg in active_list:
            temp.append(line_seg)
        out.append({'lines': temp, 'horizontal_position': prev_pos})
        
def line_segments_were_adjacent(trajectory_seg_a, trajectory_seg_b):
    return trajectory_seg_a.trajectory_id == trajectory_seg_b.trajectory_id and \
        abs(trajectory_seg_a.position_in_trajectory - trajectory_seg_b.position_in_trajectory) == 1
    
def same_trajectory_line_segment_connects(seg, line_seg_endpoint_list):
    for other in line_seg_endpoint_list:
        if line_segments_were_adjacent(seg, other.line_segment):
            return True
    return False
        
def remove_duplicate_points_from_adjacent_lines_of_same_trajectories(active_list, insert_list, delete_list):
    insertion_line_seg_set = set()
    for endpoint in insert_list:
        insertion_line_seg_set.add(endpoint.line_segment)
    
    deletion_keeper_list = []
    for endpoint in delete_list:
        if (not endpoint.line_segment in insertion_line_seg_set) and \
        same_trajectory_line_segment_connects(endpoint.line_segment, insert_list):
            active_list.remove_node(endpoint.list_node)
        else:
            deletion_keeper_list.append(endpoint)
            
    delete_list[:] = deletion_keeper_list

def get_representative_trajectory_average_inputs(trajectory_line_segments, min_lines, min_prev_dist):
    cur_active = [False] * len(trajectory_line_segments)
    active_list = LinkedList()        
    insert_list = [] 
    delete_list = []
    out = []
    
    line_segment_endpoints = get_sorted_line_seg_endpoints(trajectory_line_segments)
        
    i = 0
    while i < len(line_segment_endpoints):
        insert_list[:] = []
        delete_list[:] = []
        prev_pos = line_segment_endpoints[i].horizontal_position
        
        while i < len(line_segment_endpoints) and numbers_within(line_segment_endpoints[i].horizontal_position, \
                                                                 prev_pos, DECIMAL_MAX_DIFF_FOR_EQUALITY):
            if not cur_active[line_segment_endpoints[i].line_segment_id]:
                insert_list.append(line_segment_endpoints[i])
                cur_active[line_segment_endpoints[i].line_segment_id] = True
            elif cur_active[line_segment_endpoints[i].line_segment_id]:
                delete_list.append(line_segment_endpoints[i])
                cur_active[line_segment_endpoints[i].line_segment_id] = False
            i += 1
            
        for line_seg_endpoint in insert_list:
            active_list.add_last_node(line_seg_endpoint.list_node)
        possibly_append_to_active_list(active_list, out, prev_pos, min_prev_dist, min_lines)
        for line_seg in delete_list:
            active_list.remove_node(line_seg.list_node)
    
    return out
            
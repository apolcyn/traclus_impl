'''
Created on Jan 10, 2016

@author: Alex
'''
from partitioning.trajectory_partitioning import get_line_segment_from_points,\
    call_partition_trajectory
from generic_dbscan import dbscan
from traclus_dbscan.traclus_dbscan import TrajectoryLineSegmentFactory,\
    TrajectoryClusterFactory
from line_segment_averaging import get_representative_line_from_trajectory_line_segments

def the_whole_enchilada(point_iterable_list, epsilon, min_neighbors, min_num_trajectories_in_cluster, \
                        min_vertical_lines, min_prev_dist):
    trajectory_line_segment_factory = TrajectoryLineSegmentFactory()
    def _dbscan_caller(cluster_candidates):
        return dbscan(cluster_candidates=cluster_candidates, epsilon=epsilon, min_neighbors=min_neighbors, \
                      cluster_factory=TrajectoryClusterFactory())
    all_traj_segs_iter_from_all_points_caller = \
    get_all_trajectory_line_segments_iterable_from_all_points_iterable_caller(get_line_segs_from_points_func=get_trajectory_line_segments_from_points_iterable, \
                                                                              trajectory_line_segment_factory=trajectory_line_segment_factory, \
                                                                              trajectory_partitioning_func=call_partition_trajectory, \
                                                                              line_seg_from_points_func=get_line_segment_from_points)
    cluster_iter_from_points_caller = \
    get_cluster_iterable_from_all_points_iterable_caller(get_all_traj_segs_from_all_points_caller=all_traj_segs_iter_from_all_points_caller, \
                                                         dbscan_caller=_dbscan_caller)
    representative_line_from_trajectory_caller = get_representative_lines_from_trajectory_caller(min_vertical_lines=min_vertical_lines, min_prev_dist=min_prev_dist)
    return representative_line_seg_iterable_from_all_points_iterable(point_iterable_list, get_cluster_iterable_from_all_points_iterable_caller=cluster_iter_from_points_caller, \
                                                                     get_representative_line_seg_from_trajectory_caller=representative_line_from_trajectory_caller, \
                                                                     min_num_trajectories_in_cluster=min_num_trajectories_in_cluster)

def get_cluster_iterable_from_all_points_iterable_caller(get_all_traj_segs_from_all_points_caller, \
                                                  dbscan_caller):
    def _func(point_iterable_list):
        return get_cluster_iterable_from_all_points_iterable(point_iterable_list=point_iterable_list, \
                                                             get_all_traj_segs_from_all_points_caller=get_all_traj_segs_from_all_points_caller, \
                                                             dbscan_caller=dbscan_caller)
    return _func

def get_representative_lines_from_trajectory_caller(min_vertical_lines, min_prev_dist):
    def _func(trajectory_line_segs):
        return get_representative_line_from_trajectory_line_segments(trajectory_line_segments=trajectory_line_segs, \
                                                                     min_vertical_lines=min_vertical_lines, min_prev_dist=min_prev_dist)
    return _func

def representative_line_seg_iterable_from_all_points_iterable(point_iterable_list, \
                                                              get_cluster_iterable_from_all_points_iterable_caller, \
                                                              get_representative_line_seg_from_trajectory_caller, 
                                                              min_num_trajectories_in_cluster):
    rep_lines = []
    clusters = get_cluster_iterable_from_all_points_iterable_caller(point_iterable_list)
    for traj_cluster in clusters:
        if traj_cluster.num_trajectories_contained() >= min_num_trajectories_in_cluster:
            rep_lines.append(get_representative_line_seg_from_trajectory_caller(traj_cluster.get_trajectory_line_segments()))
                
    return rep_lines

def get_cluster_iterable_from_all_points_iterable(point_iterable_list,  get_all_traj_segs_from_all_points_caller, \
                                                  dbscan_caller):
    return dbscan_caller(get_all_traj_segs_from_all_points_caller(point_iterable_list))
    
def get_all_trajectory_line_segments_iterable_from_all_points_iterable_caller(get_line_segs_from_points_func, \
                                              trajectory_line_segment_factory, trajectory_partitioning_func, \
                                              line_seg_from_points_func):
    def _func(point_iterable_list):
        return get_all_trajectory_line_segments_iterable_from_all_points_iterable(point_iterable_list=point_iterable_list, \
                                                                           get_line_segs_from_points_func=get_line_segs_from_points_func, \
                                                                           trajectory_line_segment_factory=trajectory_line_segment_factory, \
                                                                           trajectory_partitioning_func=trajectory_partitioning_func, \
                                                                           line_seg_from_points_func=line_seg_from_points_func)
    return _func

def get_all_trajectory_line_segments_iterable_from_all_points_iterable(point_iterable_list, \
                                                                       get_line_segs_from_points_func, \
                                              trajectory_line_segment_factory, trajectory_partitioning_func, \
                                              line_seg_from_points_func):
    out = []
    cur_trajectory_id = 0
    for point_trajectory in point_iterable_list:
        line_segments = get_line_segs_from_points_func(point_iterable=point_trajectory, 
                                                       trajectory_line_segment_factory=trajectory_line_segment_factory, 
                                                       trajectory_id=cur_trajectory_id, 
                                                       trajectory_partitioning_func=trajectory_partitioning_func, 
                                                       line_seg_from_points_func=line_seg_from_points_func)
        temp = 0
        for traj_seg in line_segments:
            out.append(traj_seg)
            temp += 1
        if temp <= 0:
            raise Exception()
          
        cur_trajectory_id += 1
        
    return out
        

def get_trajectory_line_segments_from_points_iterable(point_iterable, trajectory_line_segment_factory, trajectory_id, \
                                                      trajectory_partitioning_func, line_seg_from_points_func):
    good_point_iterable = filter_by_indices(good_indices=trajectory_partitioning_func(trajectory_point_list=point_iterable), \
                             vals=point_iterable)
    line_segs = consecutive_item_func_iterator_getter(consecutive_item_func=line_seg_from_points_func, \
                                                      item_iterable=good_point_iterable)
    def _create_traj_line_seg(line_seg):
        return trajectory_line_segment_factory.new_trajectory_line_seg(line_seg, trajectory_id=trajectory_id)
    
    return map(_create_traj_line_seg, line_segs)

def filter_by_indices(good_indices, vals):
    return _filter_by_indices(good_indices, vals)

def _filter_by_indices(good_indices, vals):
    vals_iter = iter(vals)
    good_indices_iter = iter(good_indices)
    out_vals = []
    
    num_vals = 0
    for i in good_indices_iter:
        if i != 0:
            raise ValueError("the first index should be 0, but it was " + str(i))
        else:
            for item in vals_iter:
                out_vals.append(item)
                break
            num_vals = 1
            break
            
    max_good_index = 0
    vals_cur_index = 1
    for i in good_indices_iter:
        max_good_index = i
        for item in vals_iter:
            num_vals += 1
            if vals_cur_index == i:
                vals_cur_index += 1
                out_vals.append(item)
                break
            else:
                vals_cur_index += 1
                
    for i in vals_iter:
        num_vals += 1
                
    if num_vals < 2:
        raise ValueError("list passed in is too short")
    if max_good_index != num_vals - 1:
        raise ValueError("last index is " + str(max_good_index) + \
                         " but there were " + str(num_vals) + " vals")
    return out_vals
        
def consecutive_item_func_iterator_getter(consecutive_item_func, item_iterable):
    out_vals = []
    iterator = iter(item_iterable)
    last_item = None
    num_items = 0
    for item in iterator:
        num_items = 1
        last_item = item
        break
    if num_items == 0:
        raise ValueError("iterator doesn't have any values")
        
    for item in iterator:
        num_items += 1
        out_vals.append(consecutive_item_func(last_item, item))
        last_item = item
            
    if num_items < 2:
        raise ValueError("iterator didn't have at least two items")
        
    return out_vals
            
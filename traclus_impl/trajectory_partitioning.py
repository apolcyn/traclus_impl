'''
Created on Jan 7, 2016

@author: Alex
'''
from geometry import LineSegment
from distance_functions import perpendicular_distance, \
angular_distance
import math
from mutable_float import MutableFloat
from traclus_impl.representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY

DISTANCE_OFFSET = 0.0000000001

def call_partition_trajectory(trajectory_point_list):
    if len(trajectory_point_list) < 2:
        raise ValueError("didn't provide a trajectory with enough points")
    
    traj_line_iterable_getter = TrajectoryLineSegmentIteratorGetter(trajectory_point_list)
    
    cum_dist_getter_func = \
    cummulative_distance_function_getter_adapter(perp_distance_func=lambda x, y: perpendicular_distance(x, y), \
                                                                             angle_distance_func=lambda x, y: \
                                                                             angular_distance(x, y), \
                                                                             accumulator_wrapper=lambda x: \
                                                                             -(math.pow(2, 32) - 1) if x == 0 else math.log(x, 2), \
                                                                             accumulator_func_getter=get_number_list_reducer_that_returns_each_midway_val)

    partition_from_index_getter = get_partition_from_index_creator(get_line_segment_from_points)
    
    partition_cost_computer_func = part_cost_computer_adapter(part_cost_func=partition_cost_computer, \
                                                              line_segment_iterable_getter=traj_line_iterable_getter.get_iterable, \
                                                              partition_line_getter=partition_from_index_getter, \
                                                              distance_func_computer_getter=cum_dist_getter_func, \
                                                              line_segment_creator=get_line_segment_from_points)
    no_par_cost_computer_func = no_part_cost_computer_adapter(no_part_cost_func=no_partition_cost_computer, \
                                                              line_segment_iterable_getter=traj_line_iterable_getter.get_iterable, \
                                                              line_segment_creator=get_line_segment_from_points)
    
    return partition_trajectory(trajectory_point_list=trajectory_point_list, \
                                partition_cost_func=partition_cost_computer_func, \
                                no_partition_cost_func=no_par_cost_computer_func, \
                                get_model_cost_computer_func=get_model_cost_computer, \
                                individual_line_seg_model_cost_computer=individual_line_seg_model_cost_computer)
    
def get_model_cost_computer(individual_line_segment_cost_computer):
    return get_number_list_reducer_that_returns_each_midway_val(func=individual_line_segment_cost_computer)

def cummulative_distance_function_getter_adapter(perp_distance_func, angle_distance_func, accumulator_func_getter, \
                                                 accumulator_wrapper):
    def _func():
        return cummulative_distance_function_getter(perp_distance_func=perp_distance_func, \
                                                    angle_distance_func=angle_distance_func, \
                                                    accumulator_wrapper=accumulator_wrapper, \
                                                    accumulator_func_getter=accumulator_func_getter)
    return _func
        
def cummulative_distance_function_getter(perp_distance_func, angle_distance_func, accumulator_func_getter, \
                                         accumulator_wrapper):
    perp_dist_accumulator_func = accumulator_func_getter(lambda x: x)
    angle_dist_accumulator_func = accumulator_func_getter(lambda x: x)

    def _distance_func(line_a, line_b):
        return accumulator_wrapper(perp_dist_accumulator_func(perp_distance_func(line_a, line_b))) + \
            accumulator_wrapper(angle_dist_accumulator_func(angle_distance_func(line_a, line_b)))
    return _distance_func
        
def get_number_list_reducer_that_returns_each_midway_val(func):
    total = MutableFloat(0.0)  
    def _func(num):
        total.increment(func(num))
        return total.get_val()
    return _func
    
def individual_line_seg_model_cost_computer(line_seg):
    if line_seg.length == 0.0:
        raise ValueError("line seg has zero length: " + str(line_seg) + \
                         ". Good chance there's a sequence of points in " + \
                         " a trajectory of the form [...(x1, y1), (x2, y2), (x1, y1)...]")
    return math.log(line_seg.length, 2)

def get_partition_from_index_creator(line_segment_from_point_getter):
    def _func(list, low, high):
        if high >= len(list) or low >= high:
            raise Exception
        return line_segment_from_point_getter(list[low], list[high])
    return _func

def check_low_high_list_indices(trajectory_point_list, low_index, high_index):
    if high_index >= len(trajectory_point_list) or low_index >= high_index:
        raise IndexError

def part_cost_computer_adapter(part_cost_func, line_segment_iterable_getter, partition_line_getter, \
                               distance_func_computer_getter, line_segment_creator):
    def _func(trajectory_point_list, low_index, high_index, model_cost_computer):
        check_low_high_list_indices(trajectory_point_list=trajectory_point_list,\
                                     low_index=low_index, high_index=high_index)
        return part_cost_func(trajectory_point_list, low_index, high_index, \
                              line_segment_iterable_getter=line_segment_iterable_getter, \
                              partition_line_getter=partition_line_getter, \
                              model_cost_computer=model_cost_computer, \
                              distance_func_computer=distance_func_computer_getter(), \
                              line_segment_creator=line_segment_creator)
    return _func

def no_part_cost_computer_adapter(no_part_cost_func, line_segment_iterable_getter, line_segment_creator):
    def _func(trajectory_point_list, low_index, high_index, model_cost_computer):
        check_low_high_list_indices(trajectory_point_list=trajectory_point_list,\
                                     low_index=low_index, high_index=high_index)
        return no_part_cost_func(trajectory_point_list=trajectory_point_list, low_index=low_index, \
                                 high_index=high_index, line_segment_iterable_getter=line_segment_iterable_getter, \
                                 model_cost_computer=model_cost_computer, \
                                 line_segment_creator=line_segment_creator)
    return _func

def NEW_partition_trajectory_caller(trajectory_point_list):
    if len(trajectory_point_list) < 2:
        raise ValueError
    
    def encoding_cost_func(trajectory_line_segs, low, high, partition_line):
        return encoding_cost(trajectory_line_segs, low, high, 
                  partition_line=partition_line, 
                  angular_dist_func=angular_distance,
                  perpendicular_dist_func=perpendicular_distance)
    
    def partition_cost_func(trajectory_line_segs, low, high):
        return partition_cost(trajectory_line_segs, low, high, 
                              model_cost_func=model_cost, 
                              encoding_cost_func=encoding_cost_func)
        
    trajectory_line_segs = map(lambda i: LineSegment(trajectory_point_list[i], 
                                                     trajectory_point_list[i + 1]), 
                               range(0, len(trajectory_point_list) - 1))
    
    return partition_trajectory(trajectory_line_segs=trajectory_line_segs, 
                                partition_cost_func=partition_cost_func, 
                                no_partition_cost_func=no_partition_cost)
                                  
def partition_trajectory(trajectory_line_segs, 
                         partition_cost_func,
                         no_partition_cost_func):
    if len(trajectory_line_segs) < 1:
        raise ValueError
    low = 0
    partition_points = [0]
    last_pt = trajectory_line_segs[len(trajectory_line_segs) - 1].end
    trajectory_line_segs.append(LineSegment(last_pt, last_pt))
    
    for high in range(2, len(trajectory_line_segs)):
        if trajectory_line_segs[high - 2].unit_vector\
        .almost_equals(trajectory_line_segs[high - 1].unit_vector):
            continue
        elif trajectory_line_segs[high].start.almost_equals(trajectory_line_segs[low].start) or \
        partition_cost_func(trajectory_line_segs, low, high) > \
        no_partition_cost_func(trajectory_line_segs, low, high):
            partition_points.append(high - 1)
            low = high - 1
        
    partition_points.append(len(trajectory_line_segs) - 1)       
    return partition_points

def partition_cost(trajectory_line_segs, low, high, model_cost_func, encoding_cost_func):
    if low >= high:
        raise IndexError
    partition_line = LineSegment(trajectory_line_segs[low].start, 
                                 trajectory_line_segs[high].start)
    model_cost = model_cost_func(partition_line)
    encoding_cost = encoding_cost_func(trajectory_line_segs, low, high, partition_line)
    return model_cost + encoding_cost

def no_partition_cost(trajectory_line_segs, low, high):
    if low >= high:
        raise IndexError
    total = 0.0
    for line_seg in trajectory_line_segs[low:high]:
        total += math.log(line_seg.length, 2)
    return total

def model_cost(partition_line):
    return math.log(partition_line.length, 2)

def encoding_cost(trajectory_line_segs, low, high, 
                  partition_line, angular_dist_func, perpendicular_dist_func):
    total_angular = 0.0
    total_perp = 0.0
    for line_seg in trajectory_line_segs[low:high]:
        total_angular += angular_dist_func(partition_line, line_seg)
        total_perp += perpendicular_dist_func(partition_line, line_seg)
        
    return math.log(total_angular + DISTANCE_OFFSET, 2) + \
        math.log(total_perp + DISTANCE_OFFSET, 2)

def partition_cost_computer(trajectory_point_list, low_index, high_index, line_segment_iterable_getter, \
                            partition_line_getter, model_cost_computer, distance_func_computer, \
                            line_segment_creator):
    if low_index >= high_index:
        raise IndexError("illegal indices to partition func")
    
    partition_line = partition_line_getter(trajectory_point_list, low_index, high_index)
    model_cost = model_cost_computer(partition_line)
    
    encoding_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, \
                                                     line_segment_creator):
        encoding_cost = distance_func_computer(line_segment, partition_line)
        
    if encoding_cost == None:
        raise Exception("undefined encoding cost, there were no line segments")
        
    return model_cost + encoding_cost

def no_partition_cost_computer(trajectory_point_list, low_index, high_index, \
                               line_segment_iterable_getter, model_cost_computer, \
                               line_segment_creator):
    if low_index >= high_index:
        raise IndexError("illegal indices to no partition func")
    
    total_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, \
                                                     line_segment_creator):
        total_cost = model_cost_computer(line_segment)
        
    if total_cost == None:
        raise Exception("undefined total cost, there were no line segments")
    
    return total_cost

def get_line_segment_from_points(point_a, point_b):
    return LineSegment(point_a, point_b)

def get_trajectory_line_segment_iterator_adapter(iterator_getter, get_line_segment_from_points_func):
    def _func(list, low, high, get_line_segment_from_points_func=get_line_segment_from_points_func):
        iterator_getter(list, low, high, get_line_segment_from_points_func)
    return _func 

def get_trajectory_line_segment_iterator(list, low, high, get_line_segment_from_points_func):
    if high <= low:
        raise Exception("high must be greater than low index")
    
    line_segs = []
    cur_pos = low
        
    while cur_pos < high:
        line_segs.append(get_line_segment_from_points_func(list[cur_pos], list[cur_pos + 1]))
        cur_pos += 1
            
    return line_segs

class TrajectoryLineSegmentIteratorGetter:
    def __init__(self, points):
        self.line_list = []
        for i in xrange(0, len(points) - 1):
            self.line_list.append(get_line_segment_from_points(points[i], points[i + 1]))
    
    def get_iterable(self, unused_point_list, low, high, func=None):
        for i in xrange(low, high):
                yield self.line_list[i]
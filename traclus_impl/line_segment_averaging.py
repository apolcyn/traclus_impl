'''
Created on Jan 5, 2016

@author: Alex
'''

from representative_trajectory_average_inputs import get_representative_trajectory_average_inputs,\
    DECIMAL_MAX_DIFF_FOR_EQUALITY
from geometry import Point
from representative_line_finding import get_average_vector, get_rotated_line_segment

def get_representative_line_from_trajectory_line_segments(trajectory_line_segments, min_vertical_lines, min_prev_dist):
    average_trajectory_vector = get_average_vector(line_segment_list=map(lambda x: x.line_segment, trajectory_line_segments))
    
    for traj_line_seg in trajectory_line_segments:
        traj_line_seg.line_segment = get_rotated_line_segment(traj_line_seg.line_segment, \
                                                              - average_trajectory_vector.angle)
        
    representative_points = get_representative_line_from_rotated_line_segments(trajectory_line_segments=trajectory_line_segments, \
                                                                               min_vertical_lines=min_vertical_lines, \
                                                                               min_prev_dist=min_prev_dist)
    return map(lambda x: x.rotated(angle_in_degrees=average_trajectory_vector.angle), representative_points)

def get_representative_line_from_rotated_line_segments(trajectory_line_segments, min_vertical_lines, min_prev_dist):
    inputs = get_representative_trajectory_average_inputs(trajectory_line_segments=trajectory_line_segments, \
                                                          min_prev_dist=min_prev_dist, min_lines=min_vertical_lines)
    out = []
    for line_seg_averaging_input in inputs:
        vert_val = get_mean_vertical_coordinate_in_line_segments(line_seg_averaging_input)
        out.append(Point(line_seg_averaging_input['horizontal_position'], vert_val))
    return out

def interpolate_within_line_segment(line_segment, horizontal_coordinate):
    min_x = min(line_segment.start.x, line_segment.end.x)
    max_x = max(line_segment.start.x, line_segment.end.x)
    
    if not (min_x <= horizontal_coordinate + DECIMAL_MAX_DIFF_FOR_EQUALITY \
            and max_x >= horizontal_coordinate - DECIMAL_MAX_DIFF_FOR_EQUALITY):
        raise Exception("horizontal coordinate " + str(horizontal_coordinate) + \
                        " not within horizontal range of line segment" + \
                        " with bounds " + str(min_x) + " and " + str(max_x))
    elif line_segment.start.y - line_segment.end.y == 0.0:
        return line_segment.start.y
    elif line_segment.start.x - line_segment.end.x == 0.0:
        return (line_segment.end.y - line_segment.start.y) / 2.0 + line_segment.start.y
    else:
        return float((horizontal_coordinate - line_segment.start.x)) / (line_segment.end.x - line_segment.start.x) * \
            (line_segment.end.y - line_segment.start.y) + line_segment.start.y        
        
def line_segment_averaging_set_iterable(line_segments_to_average):
    line_segment_averaging_set = []
    horizontal_coord = line_segments_to_average['horizontal_position']
    for seg in line_segments_to_average['lines']:
        line_segment_averaging_set.append({'horizontal_pos': horizontal_coord, 'line_seg': seg.line_segment})
    
    return line_segment_averaging_set

def number_average(iter_ob, func):
    total = 0.0
    count = 0
    for item in iter_ob:
        total += func(item)
        count += 1
        
    if count == 0:
        raise Exception("no input given to take average of")
    else:
        return total / count
        
def get_mean_vertical_coordinate_in_line_segments(line_segments_to_average):
    def apply_interpolation_to_line_segment(interpolation_info):
        if interpolation_info['line_seg'] == None or interpolation_info['horizontal_pos'] == None:
            raise Exception("nil key. " + str(interpolation_info) + " was passed to apply_interpolation_to_line_segment")
        return interpolate_within_line_segment(interpolation_info['line_seg'], interpolation_info['horizontal_pos'])
       
    return number_average(line_segment_averaging_set_iterable(line_segments_to_average), \
                          apply_interpolation_to_line_segment)
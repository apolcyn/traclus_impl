'''
Created on Jan 6, 2016

@author: Alex
'''
from geometry import Vec2, LineSegment

def get_average_vector(line_segment_list):
    if len(line_segment_list) < 1:
        raise Exception("tried to get average vector of an empty line segment list")
    
    total_x = 0.0
    total_y = 0.0
    
    for segment in line_segment_list:
        if segment.end.x < segment.start.x:
            total_x += segment.start.x - segment.end.x
        else:
            total_x += segment.end.x - segment.start.x
        total_y += segment.end.y - segment.start.y
        
    return Vec2(total_x, total_y)

def get_rotated_line_segment(line_segment, angle_in_degrees):
    if angle_in_degrees > 90.0 or angle_in_degrees < -90.0:
        raise Exception("trying to rotate line segment by an illegal number of degrees: " + str(angle_in_degrees))
    
    new_start = line_segment.start.rotated(angle_in_degrees)
    new_end = line_segment.end.rotated(angle_in_degrees)
    
    return LineSegment.from_tuples((new_start.x, new_start.y), (new_end.x, new_end.y))
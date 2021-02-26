# deep_racer_framework

| Name | Datatype | Range | Accuracy | Units | AWS Param |
| :---- | :-------- | :----- | :-------- | :----- | :--------- |
| x | float | Any | Exact | Meters | x |
| y | float | Any | Exact | Meters | y |
| all_wheels_on_track | bool | True or False | Exact | | all_wheels_on_track |
| previous_waypoint_id | int | \>=0 | Exact | | closest_waypoints[0] |
| previous_waypoint_x | float | Any | Exact | Meters | |
| previous_waypoint_y | float | Any | Exact | Meters | |
| next_waypoint_id | int | \>= 0 | Exact | | closest_waypoints[1] |
| next_waypoint_x | float | Any | Exact | Meters | |
| next_waypoint_y | float | Any | Exact | Meters | |
| closest_waypoint_id | int | \>= 0 | Exact | |
| closest_waypoint_x | float |  Any | Exact | Meters | |
| closest_waypoint_y | float |  Any | Exact | Meters | |
| distance_from_closest_waypoint | float | \>=0 | Exact | Meters |
| distance_from_center | float | \>= 0.0 | Exact | Meters |
| distance_from_edge | float | \>= 0.0 | Exact | Meters |
| distance_from_extreme_edge | float | \>= 0.0 | Approximate | Meters |
| is_left_of_center | bool |  True or False | Exact |
| is_right_of_center | bool |  True or False | Exact |
| is_crashed | bool |  True or False | Exact |
| is_off_track | bool | True or False | Exact |
| is_reversed | bool |  True or False | Exact |
| steps | int | \>= 1 | Exact | Steps |
| time | float | \>= 0.0 | Approximate | Seconds |
| is_final_step | bool | True or False | Exact |
| progress | float | 0.0 to 100.0 | Exact | Percent |
| predicted_lap_time | float | \>= 0.0 | Approximate | Seconds |
| waypoints | ??LIST?? |
| track_length | float | \>= 0.0 | Exact | Meters |
| track_width | float | \>= 0.0 | Exact | Meters |
| track_speed | float | \>= 0.0 | Approximate | Meters per Second |
| progress_speed | float | \>= 0.0 | Approximate | Meters per Second |
| action_speed | float | \> 0.0 | Exact | Meters per Second |
| action_steering_angle | float | -30.0 to 30.0 | Exact | Degrees |
| action_sequence_length | int | \>= 1 | Exact | Steps |
| is_steering_left | bool | True or False | Exact |
| is_steering_right | bool | True or False | Exact |
| is_steering_straight | bool | True or False | Exact |
| heading | float | -180.0 to 180.0 | Exact | Degrees |
| track_bearing | float | -180.0 to 180.0 | Exact | Degrees |
| true_bearing | float | -180.0 to 180.0 | Approximate | Degrees |
| slide | float | -180.0 to 180.0 | Approximate | Degrees |
| skew | float | -180.0 to 180.0 | Approximate | Degrees |
| max_slide | float | -180.0 to 180.0 | Approximate | Degrees |
| max_skew | float | -180.0 to 180.0 | Approximate | Degrees |
| total_distance | float | \>= 0.0 | Approximate | Meters |


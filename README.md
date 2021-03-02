# deep_racer_framework v1.0

### Introduction

To use this framework, simply:
- Copy the **entire file** src/deep_racer_framework.py
- Scroll down to the end and write your own version of the get_reward() function
- Use one or more of the attributes from the "framework" input parameter to calculate a reward greater than zero

Notice how most IDEs, and even the editor provided in the AWS DeepRacer console itself, suggest names as you start to type attributes. This helps you write your reward function quickly and accurately.

For a few simple ideas of what's possible in a reward function, see the "src/examples" directory.

### Parameters - Summary

| Name | Datatype | Range | Accuracy | Units | AWS Param |
| :---- | :-------- | :----- | :-------- | :----- | :--------- |
| x | float | Any | Exact | Meters | x |
| y | float | Any | Exact | Meters | y |
| all_wheels_on_track | bool | True or False | Exact | | all_wheels_on_track |
| previous_waypoint_id | int | \>=0 | Exact | List index | closest_waypoints[0] |
| previous_waypoint_x | float | Any | Exact | Meters | |
| previous_waypoint_y | float | Any | Exact | Meters | |
| next_waypoint_id | int | \>= 0 | Exact | List index | closest_waypoints[1] |
| next_waypoint_x | float | Any | Exact | Meters | |
| next_waypoint_y | float | Any | Exact | Meters | |
| closest_waypoint_id | int | \>= 0 | Exact | List index |
| closest_waypoint_x | float |  Any | Exact | Meters | |
| closest_waypoint_y | float |  Any | Exact | Meters | |
| distance_from_closest_waypoint | float | \>= 0.0 | Exact | Meters |
| distance_from_center | float | \>= 0.0 | Exact | Meters | distance_from_center |
| distance_from_edge | float | \>= 0.0 | Exact | Meters |
| distance_from_extreme_edge | float | \>= 0.0 | Approximate | Meters |
| is_left_of_center | bool |  True or False | Exact | | is_left_of_center |
| is_right_of_center | bool |  True or False | Exact |
| is_crashed | bool |  True or False | Exact | | is_crashed |
| is_off_track | bool | True or False | Exact | | is_offtrack |
| is_reversed | bool |  True or False | Exact | | is_reversed |
| steps | int | \>= 1 | Exact | Steps | steps |
| time | float | \>= 0.0 | Approximate | Seconds |
| is_final_step | bool | True or False | Exact |
| progress | float | 0.0 to 100.0 | Exact | Percent | progress |
| predicted_lap_time | float | \>= 0.0 | Approximate | Seconds |
| waypoints | List | | Exact | | waypoints |
| track_length | float | \>= 0.0 | Exact | Meters | track_length |
| track_width | float | \>= 0.0 | Exact | Meters | track_width |
| track_speed | float | \>= 0.0 | Approximate | Meters per Second |
| progress_speed | float | \>= 0.0 | Approximate | Meters per Second |
| action_speed | float | \> 0.0 | Exact | Meters per Second | speed |
| action_steering_angle | float | -30.0 to 30.0 | Exact | Degrees | steering_angle |
| action_sequence_length | int | \>= 1 | Exact | Steps |
| is_steering_left | bool | True or False | Exact |
| is_steering_right | bool | True or False | Exact |
| is_steering_straight | bool | True or False | Exact |
| heading | float | -180.0 to 180.0 | Exact | Degrees | heading |
| track_bearing | float | -180.0 to 180.0 | Exact | Degrees |
| true_bearing | float | -180.0 to 180.0 | Approximate | Degrees |
| slide | float | -180.0 to 180.0 | Approximate | Degrees |
| skew | float | -180.0 to 180.0 | Approximate | Degrees |
| max_slide | float | -180.0 to 180.0 | Approximate | Degrees |
| max_skew | float | -180.0 to 180.0 | Approximate | Degrees |
| total_distance | float | \>= 0.0 | Approximate | Meters |


### Parameters - Explained

*Coming soon ...*

### Planned New Features for V2.0

Support for the remaining AWS DeepRacer native parameters and associated concepts:
- projection_distance  
- closest_objects  
- objects_distance  
- objects_distance_from_center  
- objects_heading  
- objects_left_of_center  
- objects_location  
- objects_speed  
- object_in_camera  

Plus, hopefully:
- track shape analysis
- predicted path analysis
- camera visibility analysis
- section speed calculations
- *... and hopefully lots more ideas ...*


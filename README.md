# deep_racer_framework v1.0

## Introduction

To use this framework, simply:
- Copy the **entire file** src/deep_racer_framework.py
- Scroll down to the end and write your own version of the get_reward() function
- Use one or more of the attributes from the "framework" input parameter to calculate a reward greater than zero

Notice how most IDEs, and even the editor provided in the AWS DeepRacer console itself, suggest names as you start to type attributes. This helps you write your reward function quickly and accurately.

For a few simple ideas of what's possible in a reward function, see the "src/examples" directory.

## Parameters - Summary

| Name | Datatype | Range | Accuracy | Units | AWS Param |
| :---- | :-------- | :----- | :-------- | :----- | :--------- |
| x | float | Any | Exact | Meters | x |
| y | float | Any | Exact | Meters | y |
| all_wheels_on_track | bool | True or False | Exact | | all_wheels_on_track |
| is_left_of_center | bool |  True or False | Exact | | is_left_of_center |
| is_right_of_center | bool |  True or False | Exact |
| distance_from_center | float | \>= 0.0 | Exact | Meters | distance_from_center |
| distance_from_edge | float | \>= 0.0 | Exact | Meters |
| distance_from_extreme_edge | float | \>= 0.0 | Approximate | Meters |
| waypoints | List | | Exact | | waypoints |
| closest_waypoint_id | int | \>= 0 | Exact | List index |
| closest_waypoint_x | float |  Any | Exact | Meters | |
| closest_waypoint_y | float |  Any | Exact | Meters | |
| previous_waypoint_id | int | \>=0 | Exact | List index | closest_waypoints[0] |
| previous_waypoint_x | float | Any | Exact | Meters | |
| previous_waypoint_y | float | Any | Exact | Meters | |
| next_waypoint_id | int | \>= 0 | Exact | List index | closest_waypoints[1] |
| next_waypoint_x | float | Any | Exact | Meters | |
| next_waypoint_y | float | Any | Exact | Meters | |
| distance_from_closest_waypoint | float | \>= 0.0 | Exact | Meters |
| steps | int | \>= 1 | Exact | Steps | steps |
| progress | float | 0.0 to 100.0 | Exact | Percent | progress |
| time | float | \>= 0.0 | Approximate | Seconds |
| predicted_lap_time | float | \>= 0.0 | Approximate | Seconds |
| total_distance | float | \>= 0.0 | Approximate | Meters |
| is_final_step | bool | True or False | Exact |
| is_crashed | bool |  True or False | Exact | | is_crashed |
| is_off_track | bool | True or False | Exact | | is_offtrack |
| is_reversed | bool |  True or False | Exact | | is_reversed |
| is_complete_lap | bool | True or False | Exact |
| track_speed | float | \>= 0.0 | Approximate | Meters per Second |
| progress_speed | float | \>= 0.0 | Approximate | Meters per Second |
| action_speed | float | \> 0.0 | Exact | Meters per Second | speed |
| action_steering_angle | float | -30.0 to 30.0 | Exact | Degrees | steering_angle |
| is_steering_left | bool | True or False | Exact |
| is_steering_right | bool | True or False | Exact |
| is_steering_straight | bool | True or False | Exact |
| action_sequence_length | int | \>= 1 | Exact | Steps |
| heading | float | -180.0 to 180.0 | Exact | Degrees | heading |
| track_bearing | float | -180.0 to 180.0 | Exact | Degrees |
| true_bearing | float | -180.0 to 180.0 | Approximate | Degrees |
| slide | float | -180.0 to 180.0 | Approximate | Degrees |
| skew | float | -180.0 to 180.0 | Approximate | Degrees |
| max_slide | float | -180.0 to 180.0 | Approximate | Degrees |
| max_skew | float | -180.0 to 180.0 | Approximate | Degrees |
| track_length | float | \>= 0.0 | Exact | Meters | track_length |
| track_width | float | \>= 0.0 | Exact | Meters | track_width |


## Parameters - Explained

#### Car Location
- **x** - The x co-ordinate of the car's location
- **y** - The y co-ordinate of the car's location
- **all_wheels_on_track** - Value of _True_ means all four wheels are on the track
- **is_left_of_center** - Value of _True_ means the centre of the car is left of the center line
- **is_right_of_center** - Value of _True_ means the centre of the car is right of the center line
- **distance_from_center** - xxx
- **distance_from_edge** - xxx
- **distance_from_extreme_edge** - xxx


#### Waypoints
- **waypoints** - List of all track waypoints, same as AWS DeepRacer parameter
- **closest_waypoint_x** - The x co-ordinate of the closest waypoint to the car
- **closest_waypoint_y** - The y co-ordinate of the closest waypoint to the car
- **closest_waypoint_id** - The index number of the closest waypoint to the car (index indicates position in the **waypoints** list)
- **previous_waypoint_x** / **y** / **id** - Similarly, the x, y and index of the waypoint immediately behind the car
- **next_waypoint_x** / **y** / **id** - Similarly, the x, y and index of the waypoint immediately in front of the car
- **distance_from_closest_waypoint** - The distance of the car from the closest waypoint

#### Progress Indications
- **steps** - xxx
- **progress** - xxx
- **time** - xxx
- **predicted_lap_time** - xxx
- **total_distance** - xxx
- **is_final_step** - xxx (the episode ends at this step, so this is the final chance to give / not give an appropriate reward for the final state) ... see next section for status indications

#### Episode Final Status
- **is_crashed** - Value of _true_ means the car has crashed into an object
- **is_off_track** - Value of _true_ means the car has gone off track, i.e. none of its wheels are on the track
- **is_reversed** - Value of _true_ means the car is going the wrong way round the track i.e. it probably spun and ended up pointing the wrong way!
- **is_complete_lap** - Value of _true_ means the car has finished a lap

#### Actual Speed
- **track_speed** - The speed the car is currently actually travelling at
- **progress_speed** - xxx

(note - these are real measures of the car's speed, unlike the action_speed, see below)

#### Action Chosen
- **action_speed** - The speed of the action chosen from the action space
- **action_steering_angle** - The steering angle of the action chosen from the action space
- **is_steering_left** - Value of _true_ means the chosen action is steering left
- **is_steering_right** - Value of _true_ means the chosen action is steering right
- **is_steering_straight** - Value of _true_ means the chosen action is steering straight ahead
- **action_sequence_length** - Counts number of consecutive times the same action has been chosen, including this step (hence always >= 1)

(note - a sequence length of 1 means the chosen action is different from the last step; a value >= 2 indicates the same action has been chosen again)

#### Direction of Travel etc.
- **heading** - xxx
- **track_bearing** - xxx
- **true_bearing** - xxx

####  Indications of Sliding/Skidding etc.
- **slide** - xxx
- **skew** - xxx
- **max_slide** - xxx
- **max_skew** - xxx

#### Track Characteristics
- **track_length** - xxx
- **track_width** - xxx


## Planned New Features for V2.0

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


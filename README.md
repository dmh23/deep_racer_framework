# deep_racer_framework v1.2.0

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
| just_passed_waypoint_ids | List | | Exact | List index | |
| time_at_waypoint | List | | Approximate | Seconds | |
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
| max_possible_track_speed | float | \> 0.0 | Approximate | Meters per Second |
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
| projected_distance | float | \>= 0.0 | Approximate | Meters |
| projected_progress_distance | float | \>= 0.0 | Approximate | Meters |
| projected_finish_left | bool | True or False | Approximate |
| slide | float | -180.0 to 180.0 | Approximate | Degrees |
| skew | float | -180.0 to 180.0 | Approximate | Degrees |
| max_slide | float | -180.0 to 180.0 | Approximate | Degrees |
| max_skew | float | -180.0 to 180.0 | Approximate | Degrees |
| track_length | float | \>= 0.0 | Exact | Meters | track_length |
| track_width | float | \>= 0.0 | Exact | Meters | track_width |
| has_objects | bool | True or False | Exact |
| objects_location | TODO |
| front_object_id | TODO |
| distance_to_front_object | TODO |
| front_object_is_left_of_centre | TODO |
| rear_object_id | TODO |
| distance_to_rear_object | TODO |
| rear_object_is_left_of_centre | TODO |
| step_when_passed_object | TODO |
| projected_hit_object | TODO |

## Parameters - Explained

#### Car Location
- **x** - The x co-ordinate of the car's location
- **y** - The y co-ordinate of the car's location
- **all_wheels_on_track** - Value of _True_ means all four wheels are on the track
- **is_left_of_center** - Value of _True_ means the centre of the car is left of the center line
- **is_right_of_center** - Value of _True_ means the centre of the car is right of the center line
- **distance_from_center** - The distance of the center of the car from the center line of the track
- **distance_from_edge** - The distance of the center of the car from the edge of the track (zero means the center of the car is on or beyond the edge)
- **distance_from_extreme_edge** - The _approximate_ distance of the car from actually going off track (zero means the car is either off track, or dangerously close)

Note: Regarding the edge of the track, remember that the car is still on the track so long as at least one wheel is on the track, and furthermore the car itself is quite wide relative to the track ... so when **distance_from_edge** is zero, in reality the car is still fairly safely on the track ... this is why **distance_from_extreme_edge** is also provided as a better estimate of how far the car really is from being judged off track.


#### Waypoints
- **waypoints** - List of all track waypoints, same as AWS DeepRacer parameter
- **closest_waypoint_x** - The x co-ordinate of the closest waypoint to the car
- **closest_waypoint_y** - The y co-ordinate of the closest waypoint to the car
- **closest_waypoint_id** - The index number of the closest waypoint to the car (index indicates position in the **waypoints** list)
- **previous_waypoint_x** / **y** / **id** - Similarly, the x, y and index of the waypoint immediately behind the car
- **next_waypoint_x** / **y** / **id** - Similarly, the x, y and index of the waypoint immediately in front of the car
- **distance_from_closest_waypoint** - The distance of the car from the closest waypoint
- **just_passed_waypoint_ids** - A list of waypoint index(es) just passed (each waypoint is only passed at most once per episode)
- **time_at_waypoint** - A list of the **time** when each waypoint was passed in this episode - or _None_ if the waypoint is not yet passed - the list index is the waypoint id

#### Progress Indications
- **steps** - Number of steps completed so far in this episode, including this step (so it's basically the step number)
- **progress** - Progress towards a complete lap as a percentage in the range 0 to 100
- **time** - The _approximate_ number of seconds that the car has taken so far
- **predicted_lap_time** - Estimate for complete lap time based on progress so far (e.g. if car has covered half the track in 6 secs, then the predicted lap time is 12 seconds, and so on)
- **total_distance** - Total distance travelled so far in this episode
- **is_final_step** - Value of _true_ means the car has ended this episode, this is the last call to the reward function, so this is your chance to give a special reward for a fast lap, or to penalise not finishing successfully (see next section, "Episode Final Status", to discover why the episode is ending, good or bad!)

#### Episode Final Status
- **is_crashed** - Value of _true_ means the car has crashed into an object
- **is_off_track** - Value of _true_ means the car has gone off track, i.e. none of its wheels are on the track
- **is_reversed** - Value of _true_ means the car is going the wrong way round the track i.e. it probably spun and ended up pointing the wrong way!
- **is_complete_lap** - Value of _true_ means the car has finished a lap

Note: All values of these are _false_ until the very last step, when these are set to indicate the reason for reaching the end of the episode

#### Actual Speed
- **track_speed** - The speed the car is currently actually travelling at
- **max_possible_track_speed** - An estimate of the maximum possible **track_speed** for the number of steps completed so far (it takes approximately 25 steps to reach a potential top speed of 4 m/s)
- **progress_speed** - The speed of the car relative to the center line; if the car is travelling along the centre line, then it will be the same as the **track_speed**; if it is cutting a corner, the **progress_speed** will be higher; or if it is going sideways or taking the outside of a corner, then the **progress_speed** will be lower

Note: These are real measures of the car's speed, unlike the **action_speed**, see below  
Note: More precisely, the **progress_speed** is the speed the car is effectively completing the track as measured along the waypoints / center line (it is called "progress" speed since this is the method for measuring **progress**, see above)

#### Action Chosen
- **action_speed** - The speed of the action chosen from the action space
- **action_steering_angle** - The steering angle of the action chosen from the action space
- **is_steering_left** - Value of _true_ means the chosen action is steering left
- **is_steering_right** - Value of _true_ means the chosen action is steering right
- **is_steering_straight** - Value of _true_ means the chosen action is steering straight ahead
- **action_sequence_length** - Counts number of consecutive times the same action has been chosen, including this step (hence always >= 1)

Note: A sequence length of 1 means the chosen action is different from the last step; a value >= 2 indicates the same action has been chosen again

#### Direction of Travel etc.
- **heading** - The heading of the car in degrees, which means this is where the car is "pointing" (also think of this as being the direction the camera is "looking")
- **track_bearing** - The bearing of the track in degrees, based on the waypoints / center line
- **true_bearing** - The actual bearing the car is travelling along, which might differ from the **heading** especially on bends, or if the car is out of control (spinning etc.)

#### Projections
- **projected_distance** - The remaining distance the car will travel before coming off the track or hitting an object if it continues at the current **true_bearing**
- **projected_progress_distance** - The remaining distance the car will travel relative to the centre line before coming off the track or hitting an object if it continues at the current **true_bearing**
- **projected_finish_left** - Value of _true_ means the car will come off track or hit an object on the left-hand side if it continues at the current **true_bearing**
- **projected_hit_object** - See "Object Avoidance", below

Note: The **projected_progress_distance** is a similar concept to the **progress_speed** as described above, i.e. it measures the likely "progress" of the car along the waypoints

####  Indications of Sliding/Skidding etc.
- **slide** - The difference in degrees between **heading** and **true_bearing**, you decide what is reasonable but typically somewhere between 10 and 20 degrees difference marks the change from controlled behaviour to sliding/skidding/spinning (i.e. uncontrolled, unless you want to encourage rally turns round a tight corner!)
- **skew** - The difference in degrees between **track_bearing** and **true_bearing**, so a value close to zero indicates the car is following the track center line (which might be good for straight sections), whereas higher values indicate driving across the track (which might be good for cutting corners)
- **max_slide** - The greatest value of **slide** during this episode, provided so you can reward or penalise behaviour such as skidding for the remainder of the episode (e.g. you might reward the car for recovering and continuing, or you might continue to penalise the rest of the episode to prevent loss of control in future)
- **max_skew** - Similarly, the greatest value of **skew** during this episode (probably less useful than **max_slide**?!)

#### Track Characteristics
- **track_length** - Total length of the track (measured along the waypoints / center line)
- **track_width** - Width of the track

#### Object Avoidance
- **has_objects** - Value of _true_ means there are objects to be avoided
- **objects_location** - An array of the location of every object, same as the AWS DeepRacer parameter
- **front_object_id** - The index number of the closest object in front of the car (use this index to access the **objects_location**)
- **distance_to_front_object** - The distance to the closest object in front of the car
- **front_object_is_left_of_centre** - Value of _true_ means the closest object in front of the car is on the left side
- **rear_object_id** - The index number of the closest object behind the car (use this index to access the **objects_location** or **step_when_passed_object**)
- **distance_to_rear_object** - The distance to the closest object behind the car
- **rear_object_is_left_of_centre** - Value of _true_ means the closest object behind the car is on the left side
- **step_when_passed_object** - An array indicating which at which step each object was passed (a value of _None_ means the object is not yet passed)
- **projected_hit_object** - Value of _true_ means the car is on a direct course to crash into an object (based on the **true_bearing**)



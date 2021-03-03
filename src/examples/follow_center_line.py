# Example of rewarding the agent to follow center line
# Taken from AWS DeepRacer documentation

from src.deep_racer_framework import Framework


# -----------------------------------------------------------------------------
# Firstly, here is the *ORIGINAL* version of the reward function written by AWS
# -----------------------------------------------------------------------------

def reward_function(params):
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    return float(reward)


# -----------------------------------------------------------------------------
# And now, here it is using the DRF
#
# Changes compared to the AWS original are marked with an asterisk (*)
#
# This is a trivial example but of course the framework also contains many attributes not available directly from AWS.
#
# And even this simple example is easier to type from scratch because most IDEs and editors can check the references
# to framework attributes, whereas references to AWS "params" are only checked at run-time
# -----------------------------------------------------------------------------

def get_reward(framework: Framework):      # (*) different function name and signature

    # Read input parameters
    track_width = framework.track_width                     # (*) get value from framework
    distance_from_center = framework.distance_from_center   # (*) get value from framework

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    return reward      # (*) No need to convert to a float

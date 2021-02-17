#
# DeepRacer Framework
#
# Version 1.0
#

import math


# -------------------------------------------------------------------------------
#
# CONSTANTS
#
# -------------------------------------------------------------------------------

class ParamNames:
    ALL_WHEELS_ON_TRACK = "all_wheels_on_track"
    CLOSEST_WAYPOINTS = "closest_waypoints"
    DISTANCE_FROM_CENTER = "distance_from_center"
    IS_CRASHED = "is_crashed"
    IS_LEFT_OF_CENTER = "is_left_of_center"
    IS_OFFTRACK = "is_offtrack"
    IS_REVERSED = "is_reversed"
    HEADING = "heading"
    PROGRESS = "progress"
    PROJECTION_DISTANCE = "projection_distance"
    SPEED = "speed"
    STEERING_ANGLE = "steering_angle"
    STEPS = "steps"
    TRACK_LENGTH = "track_length"
    TRACK_WIDTH = "track_width"
    WAYPOINTS = "waypoints"
    X = "x"
    Y = "y"
    CLOSEST_OBJECTS = "closest_objects"
    OBJECTS_DISTANCE = "objects_distance"
    OBJECTS_DISTANCE_FROM_CENTER = "objects_distance_from_center"
    OBJECTS_HEADING = "objects_heading"
    OBJECTS_LEFT_OF_CENTER = "objects_left_of_center"
    OBJECTS_LOCATION = "objects_location"
    OBJECTS_SPEED = "objects_speed"
    OBJECT_IN_CAMERA = "object_in_camera"


# -------------------------------------------------------------------------------
#
# GEOMETRY
#
# -------------------------------------------------------------------------------

def get_distance_between_points(first, second):
    (x1, y1) = first
    (x2, y2) = second

    x_diff = x2 - x1
    y_diff = y2 - y1

    return math.sqrt(x_diff * x_diff + y_diff * y_diff)


def get_bearing_between_points(start, finish):
    (start_x, start_y) = start
    (finish_x, finish_y) = finish

    direction_in_radians = math.atan2(finish_y - start_y, finish_x - start_x)
    return math.degrees(direction_in_radians)


def get_angle_in_proper_range(angle):
    if angle >= 180:
        return angle - 360
    elif angle <= -180:
        return 360 + angle
    else:
        return angle


def get_turn_between_directions(current, required):
    difference = required - current
    return get_angle_in_proper_range(difference)


# -------------------------------------------------------------------------------
#
# WAYPOINT INFO CACHE
#
# -------------------------------------------------------------------------------

class ProcessedWaypoint:
    def __init__(self, point):
        (self.x, self.y) = point


def get_processed_waypoints(waypoints):
    processed_waypoints = []
    for w in waypoints:
        processed_waypoints.append(ProcessedWaypoint(w))
    return processed_waypoints


# -------------------------------------------------------------------------------
#
# FRAMEWORK
#
# -------------------------------------------------------------------------------

class Framework:
    def __init__(self, params):
        # Real PRIVATE variables set here
        self._processed_waypoints = get_processed_waypoints(params[ParamNames.WAYPOINTS])
        self._history = []

        # Definitions only of variables to use in your reward method, real values are set during process_params()
        self.x = 0.0
        self.y = 0.0
        self.all_wheels_on_track = True
        self.previous_waypoint_id = 0
        self.previous_waypoint_x = 0.0
        self.previous_waypoint_y = 0.0
        self.next_waypoint_id = 0
        self.next_waypoint_x = 0.0
        self.next_waypoint_y = 0.0
        self.closest_waypoint_id = 0
        self.closest_waypoint_x = 0.0
        self.closest_waypoint_y = 0.0
        self.distance_from_closest_waypoint = 0.0
        self.distance_from_center = 0.0
        self.distance_from_edge = 0.0
        self.is_left_of_center = False
        self.is_right_of_center = False
        self.is_crashed = False
        self.is_off_track = False
        self.is_reversed = False

        # Ideas to include estimated finishing steps / time in secs
        # Actual travel direction as well as "heading" (and corresponding skew)
        # Hence also whether spinning is or has occurred (include history of whether it has gone wrong til end of episode)
        # Actual speed as well as action speed
        # Actions, including left & right steering flags for simplicity




        self.steps = 0

    def process_params(self, params):
        self.x = float(params[ParamNames.X])
        self.y = float(params[ParamNames.Y])

        self.all_wheels_on_track = bool(params[ParamNames.ALL_WHEELS_ON_TRACK])

        self.previous_waypoint_id = int(params[ParamNames.CLOSEST_WAYPOINTS][0])
        self.previous_waypoint_x, self.previous_waypoint_y = params[ParamNames.WAYPOINTS][self.previous_waypoint_id]
        self.next_waypoint_id = int(params[ParamNames.CLOSEST_WAYPOINTS][1])
        self.next_waypoint_x, self.next_waypoint_y = params[ParamNames.WAYPOINTS][self.next_waypoint_id]

        distance_to_previous_waypoint = get_distance_between_points((self.x, self.y), params[ParamNames.WAYPOINTS][self.previous_waypoint_id])
        distance_to_next_waypoint = get_distance_between_points((self.x, self.y), params[ParamNames.WAYPOINTS][self.next_waypoint_id])
        if distance_to_previous_waypoint < distance_to_next_waypoint:
            self.closest_waypoint_id = self.previous_waypoint_id
            self.closest_waypoint_x = self.previous_waypoint_x
            self.closest_waypoint_y = self.previous_waypoint_y
            self.distance_from_closest_waypoint = distance_to_previous_waypoint
        else:
            self.closest_waypoint_id = self.next_waypoint_id
            self.closest_waypoint_x = self.next_waypoint_x
            self.closest_waypoint_y = self.next_waypoint_y
            self.distance_from_closest_waypoint = distance_to_next_waypoint

        self.distance_from_center = float(params[ParamNames.DISTANCE_FROM_CENTER])
        self.distance_from_edge = float(max(0.0, params[ParamNames.TRACK_WIDTH]) / 2 - self.distance_from_center)

        self.is_left_of_center = bool(params[ParamNames.IS_LEFT_OF_CENTER])
        self.is_right_of_center = not self.is_left_of_center

        self.is_crashed = bool(params[ParamNames.IS_CRASHED])
        self.is_off_track = bool(params[ParamNames.IS_OFFTRACK])
        self.is_reversed = bool(params[ParamNames.IS_REVERSED])

        ##### Heading etc. comes next, remember history is not changed yet - those calcuations go at the end ...

        self.steps = int(round(params[ParamNames.STEPS]))



        # Cover up new bug in DeepRacer itself
        if self.steps == 0:
            self.steps = 1

        if self.steps == 1:
            # There may be some other history info to go here too that will have to be reset
            self._history = []

    def print_debug(self):
        print("steps                   ", self.steps)
        print("x                       ", self.x)
        print("y                       ", self.y)
        print("all_wheels_on_track     ", self.all_wheels_on_track)
        print("previous_waypoint_id    ", self.previous_waypoint_id)
        print("previous_waypoint_x     ", self.previous_waypoint_x)
        print("previous_waypoint_y     ", self.previous_waypoint_y)
        print("next_waypoint_id        ", self.next_waypoint_id)
        print("next_waypoint_x         ", self.next_waypoint_x)
        print("next_waypoint_y         ", self.next_waypoint_y)
        print("closest_waypoint_id     ", self.closest_waypoint_id)
        print("closest_waypoint_x      ", self.closest_waypoint_x)
        print("closest_waypoint_y      ", self.closest_waypoint_y)
        print("distance_from_closest_waypoint ", self.distance_from_closest_waypoint)
        print("distance_from_center    ", self.distance_from_center)
        print("distance_from_edge      ", self.distance_from_edge)
        print("is_left_of_center       ", self.is_left_of_center)
        print("is_right_of_center      ", self.is_right_of_center)
        print("is_crashed              ", self.is_crashed)
        print("is_off_track            ", self.is_off_track)
        print("is_reversed             ", self.is_reversed)


# -------------------------------------------------------------------------------
#
# REWARD FUNCTION MASTER WRAPPER
#
# -------------------------------------------------------------------------------

def reward_function(params):
    global framework_global
    if not framework_global:
        framework_global = Framework(params)
    framework_global.process_params(params)
    return float(get_reward(framework_global))

    ###### TODO - error if zero or negative #######


framework_global = None


# -------------------------------------------------------------------------------
#
# YOUR REWARD FUNCTION GOES HERE ... ... ... ...
#
# -------------------------------------------------------------------------------

def get_reward(framework: Framework):
    framework.print_debug()
    return framework.steps * 2

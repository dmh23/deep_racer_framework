#
# DeepRacer Framework
#
# Version 1.1.0
#
# Copyright (c) 2021 dmh23
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


class RealWorld:
    STEPS_PER_SECOND = 15

    VEHICLE_LENGTH = 0.365
    VEHICLE_WIDTH = 0.225

    BOX_OBSTACLE_WIDTH = 0.38
    BOX_OBSTACLE_LENGTH = 0.24

    MAX_SPEEDS = [None, 0.01, 0.02, 0.04, 0.1, 0.15, 0.25, 0.4, 0.55, 0.75, 0.95, 1.2, 1.4, 1.6, 1.8, 2.0,
                  2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0]


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


def is_point_between(point, start, finish):
    bearing_from_start = get_bearing_between_points(start, point)
    bearing_to_finish = get_bearing_between_points(point, finish)
    return abs(get_turn_between_directions(bearing_from_start, bearing_to_finish)) < 1


def get_point_at_bearing(start_point, bearing: float, distance: float):
    (x, y) = start_point

    radians_to_target = math.radians(bearing)

    x2 = x + math.cos(radians_to_target) * distance
    y2 = y + math.sin(radians_to_target) * distance

    return x2, y2



# Intersection of two lines comes from Wikipedia
# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line

def get_intersection_of_two_lines(line_a_point_1, line_a_point_2,
                                  line_b_point_1, line_b_point_2):
    (x1, y1) = line_a_point_1
    (x2, y2) = line_a_point_2
    (x3, y3) = line_b_point_1
    (x4, y4) = line_b_point_2

    denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

    if denominator == 0.0:
        return None

    z1 = (x1 * y2) - (y1 * x2)
    z2 = (x3 * y4) - (y3 * x4)

    x = ((z1 * (x3 - x4)) - ((x1 - x2) * z2)) / denominator
    y = ((z1 * (y3 - y4)) - ((y1 - y2) * z2)) / denominator

    return x, y


# -------------------------------------------------------------------------------
#
# WAYPOINT INFO CACHE
#
# -------------------------------------------------------------------------------

def get_edge_point(previous, mid, future, direction_offset: int, distance: float):
    assert direction_offset in [90, -90]
    assert previous != mid

    (previous_x, previous_y) = previous
    (mid_x, mid_y) = mid
    (next_x, next_y) = future

    degrees_to_mid_point = math.degrees(math.atan2(mid_y - previous_y, mid_x - previous_x))
    if mid == future:
        track_heading_degrees = degrees_to_mid_point
    else:
        degrees_from_mid_point = math.degrees(math.atan2(next_y - mid_y, next_x - mid_x))
        degrees_difference = get_turn_between_directions(degrees_to_mid_point, degrees_from_mid_point)
        track_heading_degrees = degrees_to_mid_point + degrees_difference / 2

    radians_to_edge_point = math.radians(track_heading_degrees + direction_offset)

    x = mid_x + math.cos(radians_to_edge_point) * distance
    y = mid_y + math.sin(radians_to_edge_point) * distance

    return x, y


class ProcessedWaypoint:
    def __init__(self, point, left_safe, right_safe):
        (self.x, self.y) = point
        self.left_safe = left_safe
        self.right_safe = right_safe


def get_processed_waypoints(waypoints, track_width):
    if waypoints[0] == waypoints[-1]:
        previous = waypoints[-2]
    else:
        previous = waypoints[-1]

    left_safe = previous
    right_safe = previous

    edge_error_tolerance = 0.01
    safe_car_overhang = min(RealWorld.VEHICLE_LENGTH, RealWorld.VEHICLE_WIDTH) / 2

    processed_waypoints = []

    for i, w in enumerate(waypoints):
        # Tracks often contain a repeated waypoint, suspect this is deliberate to mess up waypoint algorithms!
        if previous != w:
            if i < len(waypoints) - 1:
                future = waypoints[i + 1]
            else:
                future = waypoints[0]

            previous_left = left_safe
            previous_right = right_safe

            left_safe = get_edge_point(previous, w, future, 90, track_width / 2 + safe_car_overhang)
            if get_distance_between_points(previous_left, left_safe) < edge_error_tolerance:
                left_safe = previous_left

            right_safe = get_edge_point(previous, w, future, -90, track_width / 2 + safe_car_overhang)
            if get_distance_between_points(previous_right, right_safe) < edge_error_tolerance:
                right_safe = previous_right

            previous = w

        processed_waypoints.append(ProcessedWaypoint(w, left_safe, right_safe))

    return processed_waypoints


# -------------------------------------------------------------------------------
#
# REMEMBER A PREVIOUS STEP IN THIS EPISODE
#
# -------------------------------------------------------------------------------

class HistoricStep:
    def __init__(self, framework, previous_step):
        self.x = framework.x
        self.y = framework.y
        self.progress = framework.progress
        self.action_speed = framework.action_speed
        self.action_steering_angle = framework.action_steering_angle
        self.closest_waypoint_id = framework.closest_waypoint_id
        self.next_waypoint_id = framework.next_waypoint_id

        if previous_step:
            self.distance = get_distance_between_points((previous_step.x, previous_step.y), (self.x, self.y))
        else:
            self.distance = 0.0  # Causes issues if we use: framework.progress / 100 * framework.track_length


# -------------------------------------------------------------------------------
#
# FRAMEWORK
#
# -------------------------------------------------------------------------------

class Framework:
    def __init__(self, params):
        # Real PRIVATE variables set here
        self._processed_waypoints = get_processed_waypoints(params[ParamNames.WAYPOINTS], params[ParamNames.TRACK_WIDTH])
        self._history = []
        self._previous_front_object = -1

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
        self.distance_from_extreme_edge = 0.0
        self.is_left_of_center = False
        self.is_right_of_center = False
        self.is_crashed = False
        self.is_off_track = False
        self.is_reversed = False
        self.is_complete_lap = False
        self.steps = 0
        self.time = 0.0
        self.is_final_step = False
        self.progress = 0.0
        self.predicted_lap_time = 0.0
        self.waypoints = []
        self.track_length = 0.0
        self.track_width = 0.0
        self.track_speed = 0.0
        self.progress_speed = 0.0
        self.action_speed = 0.0
        self.action_steering_angle = 0.0
        self.action_sequence_length = 0
        self.is_steering_left = False
        self.is_steering_right = False
        self.is_steering_straight = False
        self.heading = 0.0
        self.track_bearing = 0.0
        self.true_bearing = 0.0
        self.slide = 0.0
        self.skew = 0.0
        self.max_slide = 0.0
        self.max_skew = 0.0
        self.total_distance = 0.0
        self.objects_location = []
        self.just_passed_waypoint_ids = []
        self.time_at_waypoint = []
        self.projected_distance = 0.0
        self.max_possible_track_speed = 0.0

        # New stuff for OA ################################
        self.has_objects = False
        self.step_when_passed_object = [-1] * 20
        self.front_object_id = None
        self.rear_object_id = None
        self.distance_to_front_object = None
        self.distance_to_rear_object = None
        self.front_object_is_left_of_centre = False
        self.rear_object_is_left_of_centre = False
        self.projected_hit_object = False

    def process_params(self, params):
        self.x = float(params[ParamNames.X])
        self.y = float(params[ParamNames.Y])

        self.all_wheels_on_track = bool(params[ParamNames.ALL_WHEELS_ON_TRACK])

        self.previous_waypoint_id = int(params[ParamNames.CLOSEST_WAYPOINTS][0])
        self.previous_waypoint_x, self.previous_waypoint_y = params[ParamNames.WAYPOINTS][self.previous_waypoint_id]
        self.next_waypoint_id = int(params[ParamNames.CLOSEST_WAYPOINTS][1])
        self.next_waypoint_x, self.next_waypoint_y = params[ParamNames.WAYPOINTS][self.next_waypoint_id]

        distance_to_previous_waypoint = get_distance_between_points((self.x, self.y), params[ParamNames.WAYPOINTS][
            self.previous_waypoint_id])
        distance_to_next_waypoint = get_distance_between_points(
            (self.x, self.y), params[ParamNames.WAYPOINTS][self.next_waypoint_id])
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
        self.distance_from_edge = float(max(0.0, params[ParamNames.TRACK_WIDTH] / 2 - self.distance_from_center))
        self.distance_from_extreme_edge = \
            float(max(0.0, (params[ParamNames.TRACK_WIDTH] + RealWorld.VEHICLE_WIDTH) / 2 - self.distance_from_center))

        self.is_left_of_center = bool(params[ParamNames.IS_LEFT_OF_CENTER])
        self.is_right_of_center = not self.is_left_of_center

        self.is_crashed = bool(params[ParamNames.IS_CRASHED])
        self.is_off_track = bool(params[ParamNames.IS_OFFTRACK])
        self.is_reversed = bool(params[ParamNames.IS_REVERSED])

        self.steps = int(round(params[ParamNames.STEPS]))
        self.time = self.steps / RealWorld.STEPS_PER_SECOND
        self.progress = float(params[ParamNames.PROGRESS])
        self.is_complete_lap = self.progress == 100.0
        self.is_final_step = self.is_complete_lap or self.is_crashed or self.is_off_track or self.is_reversed
        if self.progress > 0:
            self.predicted_lap_time = round(100 / self.progress * self.steps / RealWorld.STEPS_PER_SECOND, 2)
        else:
            self.predicted_lap_time = 0.0

        self.waypoints = params[ParamNames.WAYPOINTS]
        self.track_length = params[ParamNames.TRACK_LENGTH]
        self.track_width = params[ParamNames.TRACK_WIDTH]

        self.action_speed = params[ParamNames.SPEED]
        self.action_steering_angle = params[ParamNames.STEERING_ANGLE]

        self.is_steering_straight = abs(self.action_steering_angle) < 0.01
        self.is_steering_left = self.action_steering_angle > 0 and not self.is_steering_straight
        self.is_steering_right = self.action_steering_angle < 0 and not self.is_steering_straight

        self.heading = params[ParamNames.HEADING]
        self.track_bearing = get_bearing_between_points(
            (self.previous_waypoint_x, self.previous_waypoint_y),
            (self.next_waypoint_x, self.next_waypoint_y))

        self.max_possible_track_speed = RealWorld.MAX_SPEEDS[min(self.steps, len(RealWorld.MAX_SPEEDS) - 1)]

        self.objects_location = params[ParamNames.OBJECTS_LOCATION]

        #
        # Print object info for use by DRG
        #

        # Not step 1 because there's still a bug (?!) that means the reward function is not called until step 2!!!
        if self.steps == 2 and len(self.objects_location) > 0:
            print("DRG-OBJECTS:", self.objects_location)

        #
        # Record history
        #

        if self.steps <= 2:
            self._history = []
            self.time_at_waypoint = [None] * len(self.waypoints)
            self.step_when_passed_object = [-1] * 20
            self._previous_front_object = -1

        if self._history:
            previous_step = self._history[-1]
        else:
            previous_step = None

        this_step = HistoricStep(self, previous_step)
        self._history.append(this_step)

        #
        # Calculations that use the history
        #

        if previous_step:
            if previous_step.x != self.x or previous_step.y != self.y:  # Otherwise keep existing true_bearing
                if self.progress - previous_step.progress >= 0.05:
                    self.true_bearing = get_bearing_between_points((previous_step.x, previous_step.y), (self.x, self.y))
            if (previous_step.action_speed == self.action_speed and
                    previous_step.action_steering_angle == self.action_steering_angle):
                self.action_sequence_length += 1
            else:
                self.action_sequence_length = 1

            speed_calculate_steps = self._history[-6:]
            speed_calculate_distance = sum(s.distance for s in speed_calculate_steps)
            speed_calculate_time = len(speed_calculate_steps) / RealWorld.STEPS_PER_SECOND
            self.track_speed = speed_calculate_distance / speed_calculate_time

            progress_speed_distance = (self.progress - speed_calculate_steps[0].progress) / 100 * self.track_length
            progress_speed_calculate_time = (len(speed_calculate_steps) - 1) / RealWorld.STEPS_PER_SECOND
            self.progress_speed = max(0.0, progress_speed_distance / progress_speed_calculate_time)

            self.just_passed_waypoint_ids = self._get_just_passed_waypoint_ids(
                previous_step.next_waypoint_id, self.next_waypoint_id)
        else:
            self.action_sequence_length = 1
            self.true_bearing = self.heading
            self.progress_speed = 0.0
            self.track_speed = 0.0
            self.total_distance = 0.0
            self.max_skew = 0.0
            self.max_slide = 0.0

        self.slide = get_turn_between_directions(self.heading, self.true_bearing)
        self.skew = get_turn_between_directions(self.track_bearing, self.true_bearing)
        self.total_distance += this_step.distance

        if abs(self.slide) > abs(self.max_slide):
            self.max_slide = self.slide
        if abs(self.skew) > abs(self.max_skew):
            self.max_skew = self.skew

        #
        # Object Avoidance Calculations
        #

        object_locations = params[ParamNames.OBJECTS_LOCATION]
        objects_left_of_center = params[ParamNames.OBJECTS_LEFT_OF_CENTER]
        closest_objects = params[ParamNames.CLOSEST_OBJECTS]

        self.has_objects = len(object_locations) > 0
        if self.has_objects:
            self.front_object_id = int(closest_objects[1])
            self.rear_object_id = int(closest_objects[0])

            if self.rear_object_id == self._previous_front_object:
                self.step_when_passed_object[self.rear_object_id] = self.steps

            self._previous_front_object = self.front_object_id

            self.distance_to_front_object = get_distance_between_points((self.x, self.y), object_locations[self.front_object_id])
            self.distance_to_rear_object = get_distance_between_points((self.x, self.y), object_locations[self.rear_object_id])

            self.front_object_is_left_of_centre = objects_left_of_center[self.front_object_id]
            self.rear_object_is_left_of_centre = objects_left_of_center[self.rear_object_id]

        else:
            self.front_object_id = None
            self.rear_object_id = None
            self.distance_to_front_object = None
            self.distance_to_rear_object = None
            self.front_object_is_left_of_centre = False
            self.rear_object_is_left_of_centre = None

        #
        # Projected distance calculation
        #

        self.projected_hit_object = False
        self.projected_distance = self._calculate_projected_distance_on_track()
        if self.has_objects:
            object_hit_distance = self._calculate_object_hit_distance(object_locations[self.front_object_id])
            if object_hit_distance is not None and object_hit_distance < self.projected_distance:
                self.projected_distance = object_hit_distance
                self.projected_hit_object = True
            elif len(object_locations) > 1:
                second_object_id = self.front_object_id + 1
                if second_object_id == len(object_locations):
                    second_object_id = 0
                second_object_hit_distance = self._calculate_object_hit_distance(object_locations[second_object_id])
                if second_object_hit_distance is not None and second_object_hit_distance < self.projected_distance:
                    self.projected_distance = second_object_hit_distance

    def _calculate_projected_distance_on_track(self):
        heading = get_angle_in_proper_range(self.true_bearing)
        point = (self.x, self.y)

        previous_left = self._processed_waypoints[self.previous_waypoint_id].left_safe
        previous_right = self._processed_waypoints[self.previous_waypoint_id].right_safe

        for w in self._processed_waypoints[self.next_waypoint_id:] + self._processed_waypoints[:self.next_waypoint_id]:
            off_track_distance = self._get_off_track_distance(point, heading, previous_left, previous_right, w)

            if off_track_distance is None:
                previous_left = w.left_safe
                previous_right = w.right_safe
            else:
                return off_track_distance

    @staticmethod
    def _get_off_track_distance(point, heading: float, previous_left, previous_right, processed_waypoint):
        left_safe = processed_waypoint.left_safe
        right_safe = processed_waypoint.right_safe

        direction_to_left_target = get_bearing_between_points(point, left_safe)
        direction_to_right_target = get_bearing_between_points(point, right_safe)

        relative_direction_to_left_target = get_turn_between_directions(heading, direction_to_left_target)
        relative_direction_to_right_target = get_turn_between_directions(heading, direction_to_right_target)

        if relative_direction_to_left_target >= 0 and relative_direction_to_right_target <= 0:
            return None
        else:
            point2 = get_point_at_bearing(point, heading, 1)  # Just some random distance (1m)
            if left_safe == previous_left:
                off_track_left = previous_left
            else:
                off_track_left = get_intersection_of_two_lines(point, point2, left_safe, previous_left)
            if right_safe == previous_right:
                off_track_right = previous_right
            else:
                off_track_right = get_intersection_of_two_lines(point, point2, right_safe, previous_right)

            left_bearing = get_bearing_between_points(point, off_track_left)
            right_bearing = get_bearing_between_points(point, off_track_right)

            distances = []
            if abs(get_turn_between_directions(left_bearing, heading)) < 1:
                if is_point_between(off_track_left, left_safe, previous_left):
                    distances += [get_distance_between_points(point, off_track_left)]
            if abs(get_turn_between_directions(right_bearing, heading)) < 1:
                if is_point_between(off_track_right, right_safe, previous_right):
                    distances += [get_distance_between_points(point, off_track_right)]

            if len(distances) > 0:
                return max(distances)
            else:
                return 0.0

    def _calculate_object_hit_distance(self, obj_middle):
        heading = get_angle_in_proper_range(self.true_bearing)
        point = (self.x, self.y)

        point2 = get_point_at_bearing(point, heading, 1)  # Just some random distance (1m) to define line
        track_bearing = self._get_track_bearing_at_point(obj_middle)
        safe_border = min(RealWorld.VEHICLE_WIDTH, RealWorld.VEHICLE_LENGTH) / 3  # Effectively enlarge the box

        front_middle = get_point_at_bearing(obj_middle, track_bearing, RealWorld.BOX_OBSTACLE_LENGTH / 2 + safe_border)
        front_left = get_point_at_bearing(front_middle, track_bearing + 90,
                                                   RealWorld.BOX_OBSTACLE_WIDTH / 2 + safe_border)
        front_right = get_point_at_bearing(front_middle, track_bearing - 90,
                                                    RealWorld.BOX_OBSTACLE_WIDTH / 2 + safe_border)

        rear_middle = get_point_at_bearing(obj_middle, track_bearing, -RealWorld.BOX_OBSTACLE_LENGTH / 2 - safe_border)
        rear_left = get_point_at_bearing(rear_middle, track_bearing + 90, RealWorld.BOX_OBSTACLE_WIDTH / 2 + safe_border)
        rear_right = get_point_at_bearing(rear_middle, track_bearing - 90,
                                                   RealWorld.BOX_OBSTACLE_WIDTH / 2 + safe_border)

        distances = []
        for box_side in [(front_left, front_right), (rear_left, rear_right),
                         (front_left, rear_left), (front_right, rear_right)]:
            (box_point1, box_point2) = box_side
            hit_point = get_intersection_of_two_lines(point, point2, box_point1, box_point2)
            if hit_point is not None and is_point_between(hit_point, box_point1, box_point2):
                # Make sure it's in front of us!
                bearing_to_hit_point = get_bearing_between_points(point, hit_point)
                if abs(get_turn_between_directions(bearing_to_hit_point, heading)) < 1:
                    distances.append(get_distance_between_points(point, hit_point))

        if not distances:
            return None
        else:
            return min(distances)

    def _get_track_bearing_at_point(self, point):
        closest_waypoint = self._get_closest_waypoint_id(point)
        (before_waypoint, after_waypoint) = self.get_waypoint_ids_before_and_after(point, closest_waypoint)
        return get_bearing_between_points(self.waypoints[before_waypoint],
                                          self.waypoints[after_waypoint])

    def _get_closest_waypoint_id(self, point):
        distance = get_distance_between_points(self.waypoints[0], point)
        closest_id = 0
        for i, w in enumerate(self.waypoints[1:]):
            new_distance = get_distance_between_points(w, point)
            if new_distance < distance:
                distance = new_distance
                closest_id = i + 1
        return closest_id

    def get_waypoint_ids_before_and_after(self, point, closest_waypoint_id: int, prefer_forwards=False):
        assert 0 <= closest_waypoint_id < len(self.waypoints)

        previous_id = self._get_previous_waypoint_id(closest_waypoint_id)
        next_id = self._get_next_waypoint_id(closest_waypoint_id)

        previous_waypoint = self.waypoints[previous_id]
        next_waypoint = self.waypoints[next_id]
        closest_waypoint = self.waypoints[closest_waypoint_id]

        target_dist = get_distance_between_points(closest_waypoint, previous_waypoint)
        if target_dist == 0.0:
            previous_ratio = 99999.0
        else:
            previous_ratio = get_distance_between_points(point, previous_waypoint) / target_dist

        target_dist = get_distance_between_points(closest_waypoint, next_waypoint)
        if target_dist == 0.0:
            next_ratio = 99999.0
        else:
            next_ratio = get_distance_between_points(point, next_waypoint) / target_dist

        if prefer_forwards:   # Make the behind waypoint appear 5% further away
            previous_ratio *= 1.05

        if previous_ratio > next_ratio:
            return closest_waypoint_id, next_id
        else:
            return previous_id, closest_waypoint_id

    def _get_next_waypoint_id(self, waypoint_id):
        if waypoint_id >= len(self.waypoints) - 1:
            return 0
        else:
            return waypoint_id + 1

    def _get_previous_waypoint_id(self, waypoint_id):
        if waypoint_id < 1:
            return len(self.waypoints) - 1
        else:
            return waypoint_id - 1

    def _get_just_passed_waypoint_ids(self, previous_next_waypoint_id, current_next_waypoint_id):
        if previous_next_waypoint_id == current_next_waypoint_id:
            return []

        difference = current_next_waypoint_id - previous_next_waypoint_id

        if difference < -10 or 1 <= difference <= 10:
            result = []
            w = previous_next_waypoint_id
            while w != current_next_waypoint_id:
                if self.time_at_waypoint[w] is None:
                    result.append(w)
                    self.time_at_waypoint[w] = self.time
                w += 1
                if w >= len(self.waypoints):
                    w = 0

            return result
        else:
            return []

    def print_debug(self):
        print("x, y                      ", round(self.x, 3), round(self.y, 3))
        print("all_wheels_on_track       ", self.all_wheels_on_track)
        print("previous_waypoint_id      ", self.previous_waypoint_id)
        print("previous_waypoint_x, y    ", round(self.previous_waypoint_x, 3), round(self.previous_waypoint_y, 3))
        print("next_waypoint_id          ", self.next_waypoint_id)
        print("next_waypoint_x, y        ", round(self.next_waypoint_x, 3), round(self.next_waypoint_y, 3))
        print("closest_waypoint_id       ", self.closest_waypoint_id)
        print("closest_waypoint_x, y     ", round(self.closest_waypoint_x, 3), round(self.closest_waypoint_y, 3))
        print("distance_from_closest_waypoint ", round(self.distance_from_closest_waypoint, 2))
        print("distance_from_center      ", round(self.distance_from_center, 2))
        print("distance_from_edge        ", round(self.distance_from_edge, 2))
        print("distance_from_extreme_edge     ", round(self.distance_from_extreme_edge, 2))
        print("is_left/right_of_center   ", self.is_left_of_center, self.is_right_of_center)
        print("is_crashed / reversed     ", self.is_crashed, self.is_reversed)
        print("is_off_track              ", self.is_off_track)
        print("is_complete_lap           ", self.is_complete_lap)
        print("steps, is_final_step      ", self.steps, self.is_final_step)
        print("time                      ", round(self.time, 2))
        print("predicted_lap_time        ", round(self.predicted_lap_time, 2))
        print("progress                  ", round(self.progress, 2))
        print("waypoints  (SIZE)         ", len(self.waypoints))
        print("track_length, width       ", round(self.track_length, 2), round(self.track_width, 2))
        print("action_speed              ", round(self.action_speed, 2))
        print("action_steering_angle     ", round(self.action_steering_angle, 1))
        print("action_sequence_length    ", self.action_sequence_length)
        print("is_steering_left/right    ", self.is_steering_left, self.is_steering_right)
        print("is_steering_straight      ", self.is_steering_straight)
        print("heading                   ", round(self.heading, 2))
        print("track_bearing             ", round(self.track_bearing, 2))
        print("true_bearing              ", round(self.true_bearing, 2))
        print("slide  / max_slide        ", round(self.slide, 2), round(self.max_slide, 2))
        print("skew / max_skew           ", round(self.skew, 2), round(self.max_skew, 2))
        print("total_distance            ", round(self.total_distance, 2))
        print("track_speed               ", round(self.track_speed, 2))
        print("progress_speed            ", round(self.progress_speed, 2))
        print("just_passed_waypoint_ids  ", self.just_passed_waypoint_ids)
        print("time_at_waypoint          ", self.time_at_waypoint)
        print("projected_distance        ", self.projected_distance)


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
    raw_reward = float(get_reward(framework_global))
    if raw_reward > 0:
        return raw_reward
    else:
        tiny_reward = 0.0001
        print("WARNING - Invalid reward " + str(raw_reward) + " replaced with " + str(tiny_reward))
        return tiny_reward


framework_global = None


# -------------------------------------------------------------------------------
#
# YOUR REWARD FUNCTION GOES HERE ... ... ... ...
#
# -------------------------------------------------------------------------------

def get_reward(f: Framework):
    print(f.max_possible_track_speed, round(f.projected_distance, 1))
    return f.progress_speed / f.max_possible_track_speed * f.projected_distance + f.steps / 10

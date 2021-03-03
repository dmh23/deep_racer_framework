from src.deep_racer_framework import Framework


def get_reward(framework: Framework):
    speed_factor = framework.progress_speed
    if abs(framework.skew) > 40:
        speed_factor = speed_factor / 2
    elif abs(framework.skew) < 20 and abs(framework.slide) < 15:
        speed_factor += 1
    speed_factor = min(5.0, speed_factor)

    return min(1000.0, pow(framework.distance_from_extreme_edge * 10, speed_factor))
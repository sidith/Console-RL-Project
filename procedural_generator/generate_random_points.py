import random
import numpy as np


class NonOverlappingRandomPointsGenerator:
    """
    Generates a list of random points that are at least a minimum distance apart.  The maximum number of points that can be generated limited to max_coordinate ** 2.  It is possible that the number of points generated will be less than the number requested.

    Turns out it is a naturally hard problem to solve how many points can be generated in a given space with a given minimum distance. So I forwent trying to algorithmically solve that problem and instead just set a limit on the number of points that can be generated.  If you want to generate a lot of points, you ßcan increase the max_coordinate parameter.  If you want to generate a lot of points in a small space, you can decrease the min_dist parameter.
    """

    def __init__(self, num_of_points, min_dist, max_coordinate):
        self.num_of_points = num_of_points
        self.min_dist = min_dist
        self.max_coordinate = max_coordinate
        self.depth = max_coordinate**2
        self.check_values()

    @property
    def generated_points(self) -> list[tuple[int, int]]:
        potential_points = []
        while self.generating(potential_points):
            point = generate_random_point(self.max_coordinate)
            if self.point_is_acceptable(potential_points, point):
                potential_points.append(point)
            else:
                self.depth -= 1
        return potential_points

    def point_is_acceptable(
        self, potential_points: list[tuple[int, int]], point: tuple[int, int]
    ) -> bool:
        return other_points_are_min_dist_away(
            self.min_dist, potential_points, point
        ) and self.point_is_in_bounds(point)

    def generating(self, points) -> bool:
        return len(points) < self.num_of_points and self.depth > 0

    def point_is_in_bounds(self, p) -> bool:
        return (
            self.min_dist < p[0] < self.max_coordinate - self.min_dist
            and self.min_dist < p[1] < self.max_coordinate - self.min_dist
        )

    def check_values(self):
        if self.num_of_points <= 0:
            raise ValueError("Number of points must be greater than 0")
        if self.max_coordinate <= 0:
            raise ValueError("Scale must be greater than 0")
        if self.min_dist <= 0:
            raise ValueError("Minimum distance must be greater than 0")
        if self.min_dist >= self.max_coordinate:
            raise ValueError("Minimum distance must be less than max_coordinate")


def generate_random_point(max_coordinate: int) -> tuple[int, int]:
    if type(max_coordinate) != int:
        raise TypeError("Scale must be an integer")
    if max_coordinate <= 0:
        raise ValueError("Scale must be greater than 0")

    return (random.randint(0, max_coordinate), random.randint(0, max_coordinate))


def other_points_are_min_dist_away(
    min_dist: int, points: list[tuple[int:int]], point: tuple[int, int]
) -> bool:
    """
    Returns True if all points in the list are a minimum distance away from the point.  Returns False otherwise.
    """

    if min_dist <= 0:
        raise ValueError("Minimum distance must be greater than 0")
    if type(min_dist) != int:
        raise TypeError("Minimum distance must be an integer")
    if type(points) != list:
        raise TypeError("Points must be a list")
    if type(point) != tuple:
        raise TypeError("Point must be a tuple")

    return all([distance_between_points(p, point) >= min_dist for p in points])


def distance_between_points(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

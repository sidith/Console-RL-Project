import random
import numpy as np


def generate_non_overlapping_random_points(
    num_of_points: int, min_dist: int, scale: int
) -> list[tuple[int, int]]:
    """Generate a bunch of random points on a 2D plane with a catch!
    Each point must be at least `min_dist` units apart from each other.
    We'll will generate `num_of_points` but will be cut off if we request more than the maximum possible.  The `scale` is the size of the 2D plane.

    Args:
    - num_of_points (int): The number of points we want to generate. Must be greater than 0.
    - min_dist (int): The minimum distance between each point. Must be greater than 0 and less than scale.
        Measured using the pythagorean theorem.
    - scale (int): The scale of the 2D plane. Must be greater than 0.

    Raises:
    - ValueError: If num_of_points is less than or equal to 0.
    - ValueError: If scale is less than or equal to 0.
    - ValueError: If min_dist is less than or equal to 0.
    - ValueError: If min_dist is greater than the scale.
    - ValueError: If num_of_points is greater than the number of possible points.

    Returns:
    - list[tuple(int, int)]: A list of points on a 2D plane relative to the scale, with a minimum distance between each point.
    """
    try:
        assert num_of_points > 0, "Number of points must be greater than 0"
        assert scale > 0, "Scale must be greater than 0"
        assert min_dist > 0, "Minimum distance must be greater than 0"
        assert min_dist < scale, "Minimum distance must be less than scale"
        assert (
            num_of_points <= scale**2 / min_dist**2
        ), "Number of points is too large"
    except AssertionError as e:
        raise ValueError(str(e))

    points = []
    depth = num_of_points

    while len(points) < num_of_points and depth > 0:
        point = (random.randint(0, scale), random.randint(0, scale))
        if all(
            np.sqrt((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2) >= min_dist
            for p in points
        ):
            points.append(point)
        else:
            depth -= 1

    points = [
        p
        for p in points
        if min_dist < p[0] < scale - min_dist and min_dist < p[1] < scale - min_dist
    ]

    return points

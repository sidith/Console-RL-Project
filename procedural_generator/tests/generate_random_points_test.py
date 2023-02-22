import unittest
import numpy as np
from procedural_generator.generate_random_points import (
    generate_non_overlapping_random_points,
)


class TestGenerateRandomPoints(unittest.TestCase):
    def test_output_length(self):
        points = generate_non_overlapping_random_points(10, 5, 100)
        self.assertLessEqual(len(points), 10)

    def test_minimum_distance(self):
        points = generate_non_overlapping_random_points(10, 5, 100)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                self.assertGreaterEqual(
                    np.sqrt(
                        (points[i][0] - points[j][0]) ** 2
                        + (points[i][1] - points[j][1]) ** 2
                    ),
                    5,
                )

    def test_points_within_scale(self):
        points = generate_non_overlapping_random_points(10, 5, 100)
        for point in points:
            self.assertGreaterEqual(point[0], 5)
            self.assertLessEqual(point[0], 95)
            self.assertGreaterEqual(point[1], 5)
            self.assertLessEqual(point[1], 95)

    def test_zero_number_of_points_will_raise_value_error(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(0, 5, 100)

    def test_zero_scale_will_raise_value_error(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(10, 5, 0)

    def test_all_points_are_unique(self):
        points = generate_non_overlapping_random_points(10, 5, 100)
        self.assertEqual(len(set(points)), len(points))

    def test_if_minimum_distance_is_greater_than_scale(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(10, 105, 100)

    def test_negative_number_of_points(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(-10, 5, 100)

    def test_number_of_points_greater_than_possible_points(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(1000, 5, 100)

    def test_minimum_distance_equal_to_scale(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(10, 100, 100)

    def test_minimum_distance_equal_to_zero(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(10, 0, 100)

    def test_scale_equal_to_zero(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(10, 5, 0)

    def test_scale_negative(self):
        with self.assertRaises(ValueError):
            generate_non_overlapping_random_points(10, 5, -100)

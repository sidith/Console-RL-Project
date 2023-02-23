import unittest
import numpy as np
from procedural_generator.generate_random_points import (
    NonOverlappingRandomPointsGenerator,
    other_points_are_min_dist_away,
    generate_random_point,
)


class TestNonOverlappingRandomPointsGenerator(unittest.TestCase):
    def test_output_length(self):
        points = NonOverlappingRandomPointsGenerator(10, 5, 100).generated_points
        self.assertLessEqual(len(points), 10)

    def test_minimum_distance(self):
        points = NonOverlappingRandomPointsGenerator(10, 5, 100).generated_points
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                self.assertGreaterEqual(
                    np.sqrt(
                        (points[i][0] - points[j][0]) ** 2
                        + (points[i][1] - points[j][1]) ** 2
                    ),
                    5,
                )

    def test_points_within_max_coordinate(self):
        points = NonOverlappingRandomPointsGenerator(10, 5, 100).generated_points
        for point in points:
            self.assertGreaterEqual(point[0], 5)
            self.assertLessEqual(point[0], 95)
            self.assertGreaterEqual(point[1], 5)
            self.assertLessEqual(point[1], 95)

    def test_zero_number_of_points_will_raise_value_error(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(0, 5, 100).generated_points

    def test_zero_max_coordinate_will_raise_value_error(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(10, 5, 0).generated_points

    def test_all_points_are_unique(self):
        points = NonOverlappingRandomPointsGenerator(10, 5, 100).generated_points
        self.assertEqual(len(set(points)), len(points))

    def test_if_minimum_distance_is_greater_than_max_coordinate(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(10, 105, 100)

    def test_negative_number_of_points(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(-10, 5, 100)

    def test_negative_minimum_distance(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(10, -5, 100)

    def test_minimum_distance_equal_to_max_coordinate(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(10, 100, 100)

    def test_minimum_distance_equal_to_zero(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(10, 0, 100)

    def test_max_coordinate_equal_to_zero(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(10, 5, 0)

    def test_max_coordinate_negative(self):
        with self.assertRaises(ValueError):
            NonOverlappingRandomPointsGenerator(10, 5, -100)


class TestOtherPointsAreMinimumDistanceAway(unittest.TestCase):
    def test_other_points_are_minumum_distance_away_false(self):
        assert other_points_are_min_dist_away(2, [(0, 0), (2, 2)], (1, 1)) == False

    def test_other_points_are_minumum_distance_away_true(self):
        assert other_points_are_min_dist_away(2, [(0, 0), (2, 2)], (4, 4)) == True

    def test_minimum_distance_is_zero(self):
        with self.assertRaises(ValueError):
            other_points_are_min_dist_away(0, [(1, 1)], (1, 1))

    def test_min_dist_zero(self):
        with self.assertRaises(ValueError):
            other_points_are_min_dist_away(0, [(0, 0), (2, 2)], (1, 1))

    def test_min_dist_negative(self):
        with self.assertRaises(ValueError):
            other_points_are_min_dist_away(-1, [(0, 0), (2, 2)], (1, 1))

    def test_min_dist_not_integer(self):
        with self.assertRaises(TypeError):
            other_points_are_min_dist_away(2.5, [(0, 0), (2, 2)], (1, 1))

    def test_points_not_list(self):
        with self.assertRaises(TypeError):
            other_points_are_min_dist_away(2, "not a list", (1, 1))

    def test_point_not_tuple(self):
        with self.assertRaises(TypeError):
            other_points_are_min_dist_away(2, [(0, 0), (2, 2)], "not a tuple")

    def test_point_within_min_dist(self):
        assert other_points_are_min_dist_away(2, [(0, 0), (2, 2)], (1, 1)) == False

    def test_point_outside_min_dist(self):
        assert other_points_are_min_dist_away(2, [(0, 0), (2, 2)], (4, 4)) == True


class TestGenerateRandomPoint(unittest.TestCase):
    def test_generate_random_point_negative_max_coordinate(self):
        with self.assertRaises(ValueError):
            generate_random_point(-1)

    def test_generate_random_point_zero_max_coordinate(self):
        with self.assertRaises(ValueError):
            generate_random_point(0)

    def test_generate_random_point_less_than_zero_max_coordinate(self):
        with self.assertRaises(ValueError):
            generate_random_point(-100)

    def test_generate_random_point(self):
        point = generate_random_point(100)
        assert point[0] >= 0 and point[0] <= 100
        assert point[1] >= 0 and point[1] <= 100

    def test_generate_random_point_raises_type_error_string(self):
        with self.assertRaises(TypeError):
            generate_random_point("100")

    def test_generate_random_point_raises_type_error_float(self):
        with self.assertRaises(TypeError):
            generate_random_point(100.0)

    def test_return_type(self):
        point = generate_random_point(5)
        self.assertIsInstance(point, tuple)
        self.assertEqual(len(point), 2)
        self.assertIsInstance(point[0], int)
        self.assertIsInstance(point[1], int)

    def test_value_range(self):
        max_coordinate = 5
        for _ in range(100):
            point = generate_random_point(max_coordinate)
            self.assertLessEqual(point[0], max_coordinate)
            self.assertLessEqual(point[1], max_coordinate)
            self.assertGreaterEqual(point[0], 0)
            self.assertGreaterEqual(point[1], 0)

    def test_integer_max_coordinate(self):
        with self.assertRaises(TypeError):
            generate_random_point(1.5)

    def test_positive_max_coordinate(self):
        with self.assertRaises(ValueError):
            generate_random_point(-5)

from typing import List, Tuple
import unittest

import numpy as np
from procedural_generator.delaunay_triangulation import (
    DelaunayTriangulatior,
    MinimumSpanningTreeFinder,
)


import math


class TestDelaunayTriangulation(unittest.TestCase):
    def test_compute_edges_from_delaunay_triangulation(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulatior(points)
        expected_edges = [(1, 0), (1, 3), (2, 0), (3, 0), (3, 2)]
        self.assertEqual(set(dt.edges), set(expected_edges))

    def test_same_edges_in_triangulation_and_edges(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulatior(points)
        self.assertEqual(set(dt.edges), set(dt.triangulation))

    def test_no_duplicate_edges(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulatior(points)
        self.assertEqual(len(set(dt.edges)), len(dt.edges))

    def test_all_edges_have_non_negative_indices(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulatior(points)
        for edge in dt.edges:
            self.assertTrue(edge[0] >= 0 and edge[1] >= 0)

    def test_all_edges_have_valid_indices(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulatior(points)
        num_points = len(points)
        for edge in dt.edges:
            self.assertTrue(edge[0] < num_points and edge[1] < num_points)

    def test_raises_value_error_with_fewer_than_three_points(self):
        points = [(0, 0), (1, 0)]
        with self.assertRaises(ValueError):
            DelaunayTriangulatior(points)

    def test_raises_value_error_with_duplicate_points(self):
        points = [(0, 0), (1, 0), (0, 0)]
        with self.assertRaises(ValueError):
            DelaunayTriangulatior(points)

    def test_raises_type_error_with_non_tuple_points(self):
        points = [(0, 0), (1, 0), 0]
        with self.assertRaises(TypeError):
            DelaunayTriangulatior(points)

    def test_raises_value_error_for_colinear_points(self):
        points = [(0, 0), (1, 0), (2, 0)]
        with self.assertRaises(ValueError):
            DelaunayTriangulatior(points)


class TestMinimumSpanningTreeFinder(unittest.TestCase):
    def test_raise_value_error_with_fewer_than_two_points(self):
        points = [(0, 0)]
        with self.assertRaises(ValueError):
            MinimumSpanningTreeFinder(points)

    def test_raise_type_error_with_non_tuple_points(self):
        points = [(0, 0), 0]
        with self.assertRaises(TypeError):
            MinimumSpanningTreeFinder(points)

    def test_raise_value_error_with_duplicate_points(self):
        points = [(0, 0), (1, 0), (0, 0)]
        with self.assertRaises(ValueError):
            MinimumSpanningTreeFinder(points)

    def test_compute_weights(self):
        SQRT_2 = math.sqrt(2)
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        mst = MinimumSpanningTreeFinder(points)
        expected_weights = [
            [0.0, 1.0, 1.0, SQRT_2],
            [1.0, 0.0, SQRT_2, 1.0],
            [1.0, SQRT_2, 0.0, 1.0],
            [SQRT_2, 1.0, 1.0, 0.0],
        ]
        # convert to numpy array for easier comparison
        computed_weights = mst.compute_weights
        expected_weights = np.array(expected_weights)
        np.testing.assert_array_equal(computed_weights, expected_weights)

    def test_compute_minimum_spanning_tree(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        mst = MinimumSpanningTreeFinder(points)
        expected_edges = [(0, 2), (2, 3), (1, 3)]
        self.assertEqual(set(mst.compute_minimum_spanning_tree), set(expected_edges))

    def test_edges_are_always_one_less_than_points_across_many_possible_points(self):
        for i in range(100):
            # Generate n random int points in the range of 0 to 100 for each dimension  (x, y)
            points = [
                (np.random.randint(0, 100), np.random.randint(0, 100))
                for _ in range(np.random.randint(3, 100))
            ]
            points = list(set(points))
            mst = MinimumSpanningTreeFinder(points)

            self.assertEqual(len(mst.compute_minimum_spanning_tree), len(points) - 1)


def run_tests():
    unittest.main()

import unittest

from procedural_generator.triangulator import (
    Triangulator,
    DelaunayTriangulationAlgorithm as Delaunay,
)


class TestDelaunayTriangulation(unittest.TestCase):
    def test_compute_edges_from_delaunay_triangulation(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = Triangulator(points, Delaunay())
        expected_edges = [(1, 0), (1, 3), (2, 0), (3, 0), (3, 2)]
        self.assertEqual(set(dt.triangulation), set(expected_edges))

    def test_same_edges_in_triangulation_and_edges(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = Triangulator(points, Delaunay())
        self.assertEqual(set(dt.triangulation), set(dt.sorted_edges))

    def test_no_duplicate_edges(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = Triangulator(points, Delaunay())
        self.assertEqual(len(set(dt.sorted_edges)), len(dt.sorted_edges))

    def test_all_edges_have_non_negative_indices(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = Triangulator(points, Delaunay())
        for edge in dt.triangulation:
            self.assertTrue(edge[0] >= 0 and edge[1] >= 0)

    def test_all_edges_have_valid_indices(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = Triangulator(points, Delaunay())
        num_points = len(points)

        for edge in dt.triangulation:
            self.assertTrue(edge[0] < num_points and edge[1] < num_points)

    def test_raises_value_error_with_fewer_than_three_points(self):
        points = [(0, 0), (1, 0)]
        with self.assertRaises(ValueError):
            Triangulator(points, Delaunay())

    def test_raises_value_error_with_duplicate_points(self):
        points = [(0, 0), (1, 0), (0, 0)]
        with self.assertRaises(ValueError):
            Triangulator(points, Delaunay())

    def test_raises_type_error_with_non_tuple_points(self):
        points = [(0, 0), (1, 0), 0]
        with self.assertRaises(TypeError):
            Triangulator(points, Delaunay())

    def test_raises_value_error_for_colinear_points(self):
        points = [(0, 0), (1, 0), (2, 0)]
        with self.assertRaises(ValueError):
            Triangulator(points, Delaunay())

    def test_raises_type_error_for_non_numeric_points(self):
        points = [(0, 0), (1, 0), ("0", 0)]
        with self.assertRaises(TypeError):
            Triangulator(points, Delaunay())

    def test_riases_type_error_for_non_tuple_points(self):
        points = [(0, 0), (1, 0), 0]
        with self.assertRaises(TypeError):
            Triangulator(points, Delaunay())

    def test_raises_type_error_for_negative_points(self):
        points = [(0, 0), (1, 0), (-1, 0)]
        with self.assertRaises(ValueError):
            Triangulator(points, Delaunay())

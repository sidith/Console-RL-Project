import unittest

from procedural_generator.delaunay_triangulation import DelaunayTriangulator


class TestDelaunayTriangulation(unittest.TestCase):
    def test_compute_edges_from_delaunay_triangulation(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulator(points)
        expected_edges = [(1, 0), (1, 3), (2, 0), (3, 0), (3, 2)]
        self.assertEqual(set(dt.edges), set(expected_edges))

    def test_same_edges_in_triangulation_and_edges(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulator(points)
        self.assertEqual(set(dt.edges), set(dt.triangulation))

    def test_no_duplicate_edges(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulator(points)
        self.assertEqual(len(set(dt.edges)), len(dt.edges))

    def test_all_edges_have_non_negative_indices(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulator(points)
        for edge in dt.edges:
            self.assertTrue(edge[0] >= 0 and edge[1] >= 0)

    def test_all_edges_have_valid_indices(self):
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        dt = DelaunayTriangulator(points)
        num_points = len(points)
        for edge in dt.edges:
            self.assertTrue(edge[0] < num_points and edge[1] < num_points)

    def test_raises_value_error_with_fewer_than_three_points(self):
        points = [(0, 0), (1, 0)]
        with self.assertRaises(ValueError):
            DelaunayTriangulator(points)

    def test_raises_value_error_with_duplicate_points(self):
        points = [(0, 0), (1, 0), (0, 0)]
        with self.assertRaises(ValueError):
            DelaunayTriangulator(points)

    def test_raises_type_error_with_non_tuple_points(self):
        points = [(0, 0), (1, 0), 0]
        with self.assertRaises(TypeError):
            DelaunayTriangulator(points)

    def test_raises_value_error_for_colinear_points(self):
        points = [(0, 0), (1, 0), (2, 0)]
        with self.assertRaises(ValueError):
            DelaunayTriangulator(points)


def run_tests():
    unittest.main()

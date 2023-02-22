from scipy.spatial import Delaunay


class DelaunayTriangulator:
    def __init__(self, points: list[tuple[int, int]]) -> None:
        if not all(isinstance(p, tuple) for p in points):
            raise TypeError("Points must be tuples.")
        if len(points) < 3:
            raise ValueError("Not enough points to construct a Delaunay triangulation.")
        if len(set(points)) != len(points):
            raise ValueError("Duplicate points are not allowed.")
        if not all(isinstance(p[0], int) and isinstance(p[1], int) for p in points):
            raise TypeError("Points must be integers.")
        if not all(p[0] >= 0 and p[1] >= 0 for p in points):
            raise ValueError("Points must be non-negative.")
        # checks to make sure points are not in a line
        if (
            len(set([p[0] for p in points])) == 1
            or len(set([p[1] for p in points])) == 1
        ):
            raise ValueError("Points must not be in a line.")

        self.points = points
        self.triangulation = self._compute_edges_from_delaunay_triangulation()
        self.edges = self._sort_edges()

    def _compute_edges_from_delaunay_triangulation(self) -> list[tuple[int, int]]:
        tri = Delaunay(self.points)
        edges = set()
        for simplex in tri.simplices:
            for i in range(3):
                for j in range(i + 1, 3):
                    edges.add((simplex[i], simplex[j]))

        return edges

    def _sort_edges(self):
        # Define a key function that returns a tuple of the two points in the edge sorted by x and y
        def key_function(edge):
            x1, y1 = self.points[edge[0]]
            x2, y2 = self.points[edge[1]]
            if x1 < x2 or (x1 == x2 and y1 < y2):
                return (x1, y1, x2, y2)
            else:
                return (x2, y2, x1, y1)

        # Sort the edges using the key function and return them as a list
        sorted_edges = sorted(self.triangulation, key=key_function)
        return list(sorted_edges)

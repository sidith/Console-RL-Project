import numpy as np


class MinimumSpanningTreeFinder:
    def __init__(self, points: list[tuple[int, int]]) -> None:
        if not all(isinstance(p, tuple) for p in points):
            raise TypeError("Points must be tuples.")
        if len(points) < 3:
            raise ValueError(
                "At least three points are required to compute Delaunay triangulation."
            )
        if len(set(points)) != len(points):
            raise ValueError("Duplicate points are not allowed.")

        self.points = points
        self.num_points = len(self.points)

    @property
    def compute_weights(self):
        # for every point, compute the distance to every other point and store in a matrix
        weights = np.zeros((self.num_points, self.num_points))
        for i in range(self.num_points):
            for j in range(i + 1, self.num_points):
                dist = np.sqrt(
                    (self.points[i][0] - self.points[j][0]) ** 2
                    + (self.points[i][1] - self.points[j][1]) ** 2
                )
                weights[i][j] = dist
                weights[j][i] = dist
        return weights

    @property
    def compute_minimum_spanning_tree(self) -> list[tuple[int, int]]:
        # use Prim's algorithm to find the minimum spanning tree
        mst = []
        edges = set()
        weights = self.compute_weights

        # This loop adds all the edges to the set of edges with their weights
        for i in range(self.num_points):
            for j in range(i + 1, self.num_points):
                edges.add((i, j, weights[i][j]))

        # This loop sorts the edges by weight
        edges = sorted(edges, key=lambda e: e[2])

        visited = set()
        visited.add(0)  # This is the starting point
        while len(visited) != self.num_points:
            for edge in edges:
                if edge[0] in visited and edge[1] not in visited:
                    mst.append((edge[0], edge[1]))
                    visited.add(edge[1])
                    break
                elif edge[0] not in visited and edge[1] in visited:
                    mst.append((edge[0], edge[1]))
                    visited.add(edge[0])
                    break
        return mst

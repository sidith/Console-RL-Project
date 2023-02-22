import random
from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import Delaunay


from typing import List, Tuple
from scipy.spatial import Delaunay


class DelaunayTriangulatior:
    def __init__(self, points: List[Tuple[int, int]]) -> None:
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

    def _compute_edges_from_delaunay_triangulation(self) -> List[Tuple[int, int]]:
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


class MinimumSpanningTreeFinder:
    def __init__(self, points: List[Tuple[int, int]]) -> None:
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


class GraphExplorer:
    def __init__(self, graph, nodes):
        self.graph = graph
        self.nodes = nodes
        self.longest_path, self.longest_path_length = self._find_longest_path()
        self.points_of_longest_path = sorted(set(sum(self.longest_path, ())))
        self.points_of_interest = self._find_points_of_interest()

    def _find_longest_path(self):
        G = nx.DiGraph()
        for u, v in self.graph:
            dist = np.sqrt(
                (self.nodes[u][0] - self.nodes[v][0]) ** 2
                + (self.nodes[u][1] - self.nodes[v][1]) ** 2
            )
            G.add_edge(u, v, weight=dist)
            G.add_edge(v, u, weight=dist)

        paths = dict(nx.all_pairs_dijkstra_path(G))
        longest_path = []
        length = 0

        for u, u_paths in paths.items():
            for v, path in u_paths.items():
                if u != v:
                    path_length = sum(
                        G[path[i]][path[i + 1]]["weight"] for i in range(len(path) - 1)
                    )
                    if path_length > length:
                        longest_path = [
                            (path[i], path[i + 1]) for i in range(len(path) - 1)
                        ]
                        length = path_length

        return longest_path, length

    def _find_points_of_interest(self) -> List[int]:
        if len(self.longest_path) == 0:
            raise ValueError("No longest path, cannot find points of interest.")
        else:
            points_of_interest = [
                point
                for point in self.points_of_longest_path
                if any(
                    edge[0] == point
                    and edge[1] not in self.points_of_longest_path
                    or edge[1] == point
                    and edge[0] not in self.points_of_longest_path
                    for edge in self.graph
                )
            ]
        if len(points_of_interest) == 0:
            raise ValueError("No points of interest found.")
        else:
            return points_of_interest


class DelaunayMST:
    def __init__(self, points: List[Tuple[int, int]]) -> None:
        if len(points) < 3:
            raise ValueError(
                "At least three points are required to compute Delaunay triangulation."
            )
        self.points = points
        self.triangulation = DelaunayTriangulatior(points).edges
        self.num_points = len(self.points)
        self.mst_finder = MinimumSpanningTreeFinder(self.points)
        self.graph_explorer = GraphExplorer(
            self.mst_finder.compute_minimum_spanning_tree, self.points
        )
        self.longest_path = self.graph_explorer.longest_path
        self.longest_path_length = self.graph_explorer.longest_path_length
        self.points_of_longest_path = self.graph_explorer.points_of_longest_path
        self.points_of_interest = self.graph_explorer.points_of_interest

        if self.points_of_interest is not None:
            self.start_of_longest_path = self.points_of_interest[0]
        else:
            self.start_of_longest_path = None

        self.end_of_longest_path = (
            self.points_of_interest[-1] if self.points_of_interest is not None else None
        )


def plot_triangulation_mst_longest_path(
    points, triangulation, mst, longest_path, points_of_interest
):
    # create scatter plot of input points
    if points is not None:
        plt.scatter([p[0] for p in points], [p[1] for p in points], color="black")
    else:
        print("No points to plot.")

    # plot edges of triangulation in blue
    if triangulation is not None:
        for edge in triangulation:
            u, v = edge
            plt.plot(
                [points[u][0], points[v][0]], [points[u][1], points[v][1]], color="blue"
            )
    else:
        print("No triangulation to plot.")

    # plot edges of MST in green
    if mst is not None:
        for edge in mst:
            u, v = edge
            plt.plot(
                [points[u][0], points[v][0]],
                [points[u][1], points[v][1]],
                color="green",
            )
    else:
        print("No MST to plot.")

    # plot edges of longest path in red
    if longest_path is not None:
        for edge in longest_path:
            u, v = edge
            plt.plot(
                [points[u][0], points[v][0]], [points[u][1], points[v][1]], color="red"
            )
        # plot the first and last points of the longest path in pink and make them larger than the other points
        plt.scatter(
            [points[longest_path[0][0]][0], points[longest_path[-1][1]][0]],
            [points[longest_path[0][0]][1], points[longest_path[-1][1]][1]],
            color="pink",
            s=100,
        )
    else:
        print("No longest path to plot.")

    # plot points of interest in yellow
    if points_of_interest is not None:
        for point in points_of_interest:
            plt.scatter([points[point][0]], [points[point][1]], color="yellow")
    else:
        print("No points of interest to plot.")

    # set axis limits and show plot

    plt.show()


def generate_random_points(num_of_points, min_dist, scale):
    # This function generates random points on a 2D map with a given scale, and a minimum distance between points, and returns a list of points.
    # To do this it generates random points and checks if they are at least min_dist away from all other points. If they are, they are added to the list of points. If not, they are discarded. And the process is repeated until the desired number of points is reached. Finally the points that are on the boundary of the map are discarded.
    # The points such be in the form of a list of tuple (x:int, y:int), where each tuple is a point. For example, [(0, 0), (1, 1), (2, 2)] is a list of three points.

    points = []
    while len(points) < num_of_points:
        print("Generating random points: {}/{}".format(len(points), num_of_points))
        point = (random.randint(0, scale), random.randint(0, scale))
        if all(
            np.sqrt((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2) >= min_dist
            for p in points
        ):
            points.append(point)

    # remove points on the boundary of the map
    points = [p for p in points if p[0] > min_dist and p[0] < scale - min_dist]
    points = [p for p in points if p[1] > min_dist and p[1] < scale - min_dist]
    return points


def test():
    points = generate_random_points(100, 2, 100)

    delaunayMST = DelaunayMST(points)

    # compute Delaunay triangulation
    triangulation = delaunayMST.triangulation
    print("Triangulation:", triangulation)

    # compute MST from Delaunay triangulation
    mst = delaunayMST.mst_finder.compute_minimum_spanning_tree
    print(f"MST:, {mst}")

    # find longest path in MST
    longest_path, length = delaunayMST.longest_path, delaunayMST.longest_path_length
    print("Longest path:", longest_path)
    print("Longest path length:", length)

    points_of_longest_path = delaunayMST.points_of_longest_path
    print("Points of longest path:", points_of_longest_path)

    points_of_interest = delaunayMST.points_of_interest
    print("Points of interest:", points_of_interest)

    # plot triangulation, MST, and longest path
    plot_triangulation_mst_longest_path(
        points, triangulation, mst, longest_path, points_of_interest
    )

    print("Longest path length:", length)


if __name__ == "__main__":
    test()

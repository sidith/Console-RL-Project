import random
from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import Delaunay


class DelaunayMST:
    def __init__(self, points: List[Tuple[int, int]]) -> None:
        if len(points) < 3:
            raise ValueError(
                "At least three points are required to compute Delaunay triangulation.")
        self.points = points
        self.triangulation = self._compute_edges_from_delaunay_triangulation()
        self.num_points = len(self.points)
        self.mst = self._compute_minimum_spanning_tree_from_edges()
        self.longest_path, self.length = self._find_longest_path()
        self.points_of_longest_path = self._find_points_of_longest_path()
        self.points_of_interest = self._find_points_of_interest()
        self.start_of_longest_path = self.points_of_interest[0]
        self.end_of_longest_path = self.points_of_interest[-1]

    def _compute_edges_from_delaunay_triangulation(self) -> List[Tuple[int, int]]:
        tri = Delaunay(self.points)
        edges = set()
        for simplex in tri.simplices:
            for i in range(3):
                for j in range(i+1, 3):
                    edges.add((simplex[i], simplex[j]))
        return list(edges)

    def _compute_minimum_spanning_tree_from_edges(self) -> List[Tuple[int, int]]:
        if len(self.triangulation) < self.num_points - 1:
            raise ValueError(
                "Not enough edges in the Delaunay triangulation to construct an MST.")
        edges = sorted(self.triangulation, key=lambda e: ((e[0]-e[1])**2)**0.5)
        sets = [{i} for i in range(self.num_points)]
        mst = []
        for edge in edges:
            set1 = next((s for s in sets if edge[0] in s), None)
            set2 = next((s for s in sets if edge[1] in s), None)
            if set1 != set2:
                mst.append(edge)
                set1.update(set2)
                sets.remove(set2)
        return mst

    def _find_longest_path(self) -> Tuple[List[Tuple[int, int]], float]:
        if len(self.mst) < self.num_points - 1:
            raise ValueError(
                "Not enough edges in the tree to find a longest path.")

        G = nx.DiGraph()
        for u, v in self.mst:
            dist = np.sqrt((self.points[u][0] - self.points[v][0])
                           ** 2 + (self.points[u][1] - self.points[v][1]) ** 2)
            G.add_edge(u, v, weight=dist)
            G.add_edge(v, u, weight=dist)

        paths = dict(nx.all_pairs_dijkstra_path(G))
        longest_path = []
        length = 0

        for u, u_paths in paths.items():
            for v, path in u_paths.items():
                if u != v:
                    path_length = sum(G[path[i]][path[i+1]]['weight']
                                      for i in range(len(path)-1))
                    if path_length > length:
                        longest_path = [(path[i], path[i+1])
                                        for i in range(len(path)-1)]
                        length = path_length

        return longest_path, length

    def _find_points_of_longest_path(self):
        points_of_longest_path = sorted(set(sum(self.longest_path, ())))
        return points_of_longest_path

    def _find_points_of_interest(self) -> List[int]:
        points_of_interest = [point for point in self.points_of_longest_path if any(
            edge[0] == point and edge[1] not in self.points_of_longest_path
            or
            edge[1] == point and edge[0] not in self.points_of_longest_path
            for edge in self.mst)]

        return points_of_interest


def plot_triangulation_mst_longest_path(points, triangulation, mst, longest_path, points_of_interest):
    # create scatter plot of input points
    plt.scatter([p[0] for p in points], [p[1] for p in points], color='black')

    # # plot edges of triangulation in blue
    # for edge in triangulation:
    #     u, v = edge
    #     plt.plot([points[u][0], points[v][0]], [
    #              points[u][1], points[v][1]], color='blue')

    # plot edges of MST in green
    for edge in mst:
        u, v = edge
        plt.plot([points[u][0], points[v][0]], [
                 points[u][1], points[v][1]], color='green')

    # plot edges of longest path in red
    for edge in longest_path:
        u, v = edge
        plt.plot([points[u][0], points[v][0]], [
                 points[u][1], points[v][1]], color='red')
    # plot the first and last points of the longest path in pink and make them larger than the other points
    plt.scatter([points[longest_path[0][0]][0], points[longest_path[-1][1]][0]], [
                points[longest_path[0][0]][1], points[longest_path[-1][1]][1]], color='pink', s=100)

    # plot points of interest in yellow
    for point in points_of_interest:
        plt.scatter([points[point][0]], [points[point][1]], color='yellow')

    # set axis limits and show plot

    plt.show()


def generate_random_points(num_of_points, min_dist, scale):
    # This function generates random points on a 2D map with a given scale, and a minimum distance between points, and returns a list of points.
    # To do this it generates random points and checks if they are at least min_dist away from all other points. If they are, they are added to the list of points. If not, they are discarded. And the process is repeated until the desired number of points is reached. Finally the points that are on the boundary of the map are discarded.
    # The points such be in the form of a list of tuple (x:int, y:int), where each tuple is a point. For example, [(0, 0), (1, 1), (2, 2)] is a list of three points.

    points = []
    while len(points) < num_of_points:
        x = random.randint(0, scale)
        y = random.randint(0, scale)
        if all(((x - p[0])**2 + (y - p[1])**2)**0.5 >= min_dist for p in points) and x > min_dist and x < scale - min_dist and y > min_dist and y < scale - min_dist:
            points.append((x, y))

    return points


def test():

    points = generate_random_points(20, 2, 100)

    delaunayMST = DelaunayMST(points)

    # compute Delaunay triangulation
    triangulation = delaunayMST.triangulation

    # compute MST from Delaunay triangulation
    mst = delaunayMST.mst

    # find longest path in MST
    longest_path, length = delaunayMST.longest_path, delaunayMST.length

    points_of_interest = delaunayMST.points_of_interest

    # plot triangulation, MST, and longest path
    plot_triangulation_mst_longest_path(
        points, triangulation, mst, longest_path, points_of_interest)

    print("Longest path length:", length)


if __name__ == "__main__":
    test()

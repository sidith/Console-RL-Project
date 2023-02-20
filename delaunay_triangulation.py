from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import numpy as np


class PointGraph:
    def __init__(self, points):
        self.points = points
        self.tri = None
        self.mst = None
        self.path = None  # This will be a list of points that are the longest path in the graph

    def compute_triangulation(self):
        np_points = np.array(self.points)
        self.tri = Delaunay(np_points)

    def compute_minimum_spanning_tree(self):
        simplices = self.tri.simplices.copy()
        edges = []
        for simple in simplices:
            edges.append((simple[0], simple[1]))
            edges.append((simple[0], simple[2]))
            edges.append((simple[1], simple[2]))
        edges = np.array(edges)
        self.mst = minimum_spanning_tree(csr_matrix((np.ones(edges.shape[0]), (
            edges[:, 0], edges[:, 1])), shape=(len(self.points), len(self.points)))).toarray()

    def find_longest_path(self):
        pass

    def plot_graph(self):
        # This will plot the graph with the longest path highlighted in red.  The mst is plotted in black and the triangulation is plotted in blue.
        plt.figure()
        np_points = np.array(self.points)
        plt.triplot(np_points[:, 0], np_points[:, 1],
                    self.tri.simplices.copy())
        plt.plot(np_points[:, 0], np_points[:, 1], 'o')
        mst = self.mst.copy()
        for i in range(len(self.points)):
            mst[i, i] = 0
        mst = np.where(mst == 1)
        plt.plot(np_points[mst, 0], np_points[mst, 1], 'k-')
        path = np.array(self.path)

        plt.plot(np_points[path, 0], np_points[path, 1], 'r-')
        plt.show()


        # A list of 20 random points in a 100x100 grid
points = [(np.random.randint(0, 100), np.random.randint(0, 100))
          for _ in range(20)]
point_graph = PointGraph(points)
point_graph.compute_triangulation()
point_graph.compute_minimum_spanning_tree()
point_graph.find_longest_path()
point_graph.plot_graph()

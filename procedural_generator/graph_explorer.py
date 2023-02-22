import networkx as nx
import numpy as np


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

    def _find_points_of_interest(self) -> list[int]:
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

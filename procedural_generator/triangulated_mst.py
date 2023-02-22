from matplotlib import pyplot as plt

from delaunay_triangulation import DelaunayTriangulator
from graph_explorer import GraphExplorer
from minimum_spanning_tree_finder import MinimumSpanningTreeFinder
from generate_non_overlapping_random_points import (
    generate_non_overlapping_random_points,
)


class DelaunayMST:
    def __init__(self, points: list[tuple[int, int]]) -> None:
        if len(points) < 3:
            raise ValueError(
                "At least three points are required to compute Delaunay triangulation."
            )
        self.points = points
        self.triangulation = DelaunayTriangulator(points).edges
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


def plot_triangulation_mst(
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


def test():
    points = generate_non_overlapping_random_points(100, 2, 100)

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
    plot_triangulation_mst(points, triangulation, mst, longest_path, points_of_interest)

    print("Longest path length:", length)


if __name__ == "__main__":
    test()

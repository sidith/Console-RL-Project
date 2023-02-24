# This script is mainly here to help gain visual intiution for the algorithm
# and to help debug it. It is not meant to be used in the game.

from matplotlib import pyplot as plt

from graph_explorer import GraphExplorer
from minimum_spanning_tree_finder import MinimumSpanningTreeFinder
from generate_random_points import (
    NonOverlappingRandomPointsGenerator,
)
from triangulator import (
    DelaunayTriangulationAlgorithm,
    Triangulator,
)


def plot_and_show_triangulation_mst(
    points, triangulation, mst, longest_path, points_of_interest
):
    # plot_points(points)
    # plot_triangulation(points, triangulation)
    # plot_mst(points, mst)
    plot_longest_path(points, longest_path)
    plot_points_of_interest(points, points_of_interest)
    plt.show()


def plot_points_of_interest(points, points_of_interest):
    if points_of_interest is not None:
        for point in points_of_interest:
            plt.scatter([points[point][0]], [points[point][1]], color="green", s=100)
    else:
        print("No points of interest to plot.")


def plot_longest_path(points, longest_path):
    if longest_path is not None:
        for edge in longest_path:
            u, v = edge
            plt.plot(
                [points[u][0], points[v][0]], [points[u][1], points[v][1]], color="red"
            )
        plot_start_and_end_point(points, longest_path)
    else:
        print("No longest path to plot.")


def plot_start_and_end_point(points, longest_path, color="black"):
    plt.scatter(
        [points[longest_path[0][0]][0], points[longest_path[-1][1]][0]],
        [points[longest_path[0][0]][1], points[longest_path[-1][1]][1]],
        color=color,
        s=300,
    )


def plot_mst(points, mst):
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


def plot_triangulation(points, triangulation):
    if triangulation is not None:
        for edge in triangulation:
            u, v = edge
            plt.plot(
                [points[u][0], points[v][0]], [points[u][1], points[v][1]], color="blue"
            )
    else:
        print("No triangulation to plot.")


def plot_points(points):
    if points is not None:
        plt.scatter([p[0] for p in points], [p[1] for p in points], color="black")
    else:
        print("No points to plot.")


def main():
    points = NonOverlappingRandomPointsGenerator(100, 5, 100).generated_points

    triangulation = Triangulator(points, DelaunayTriangulationAlgorithm()).sorted_edges
    print("Delaunay Triangulation:\n", triangulation)

    mst = MinimumSpanningTreeFinder(points).minimum_spanning_tree
    print("Minimum Spanning Tree:\n", mst)

    graph_explorer = GraphExplorer(mst, points)
    longest_path = graph_explorer.longest_path
    length = graph_explorer.longest_path_length
    points_of_longest_path = graph_explorer.points_of_longest_path
    points_of_interest = graph_explorer.points_of_interest

    print("Longest Path:\n", longest_path)
    print("Longest Path Length:\n", length)
    print("Points of Longest Path:\n", points_of_longest_path)
    print("Points of Interest:\n", points_of_interest)

    plot_and_show_triangulation_mst(
        points, triangulation, mst, longest_path, points_of_interest
    )


if __name__ == "__main__":
    main()

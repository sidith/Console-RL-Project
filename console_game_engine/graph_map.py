
import random
from dataclasses import dataclass

from procedural_generator.procedual_gen import (RectangularRoom,
                                                create_horizontal_and_verticle_tunnel)


@dataclass()
class Edge:
    def __init__(self, l_node: RectangularRoom, r_node: RectangularRoom):
        self.l_node = l_node
        self.r_node = r_node

    def __str__(self):
        return f"({self.l_node}, {self.r_node})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Edge):
            return self.l_node == __o.r_node and self.r_node == __o.l_node
        return False


room1 = RectangularRoom(0, 0, 10, 10)
room2 = RectangularRoom(0, 0, 10, 10)
room3 = RectangularRoom(0, 0, 10, 10)


test_graph = {
    room1: [Edge(room1, room2), Edge(room1, room3)],
    room2: [Edge(room2, room1), Edge(room2, room3)],
}


def generate_rooms_from_nodes(map_width, map_height, room_min_size, room_max_size, graph):
    new_rooms = []

    for _ in graph:
        new_room = random_room(map_width, map_height,
                               room_min_size, room_max_size)

        depth = 10
        while any(room.intersects(new_room) for room in new_rooms) & depth > 0:
            new_room = random_room(map_width, map_height,
                                   room_min_size, room_max_size)
            depth -= 1

        new_rooms.append(new_room)
    return new_rooms

# This function creates a


def generate_tunnels_from_graph(graph, room_min_size, room_max_size):
    tunnels = []
    for node in graph:
        unique_edges = set([edge for edge in graph[node]])
        for edge in unique_edges:
            if edge.l_node == node:
                tunnel_pair = create_horizontal_and_verticle_tunnel(
                    edge.l_node, edge.r_node, room_min_size)
                tunnels.append(tunnel_pair[0])
                tunnels.append(tunnel_pair[1])
    return tunnels


def random_room(map_width, map_height, room_min_size, room_max_size):
    new_room = RectangularRoom(
        random.randint(0, map_width - room_max_size - 1),
        random.randint(0, map_height - room_max_size - 1),
        random.randint(room_min_size, room_max_size),
        random.randint(room_min_size, room_max_size)
    )

    return new_room


def test():
    print(test_graph[room1][0] == test_graph[room2][0])


test()

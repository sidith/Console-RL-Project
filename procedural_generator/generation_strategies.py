# generation_strategies.py | 0

from matplotlib.pyplot import plasma
from console_game_engine.game_map import GameMap
from procedural_generator.graph_explorer import GraphExplorer
from procedural_generator.minimum_spanning_tree_finder import MinimumSpanningTreeFinder
from procedural_generator.room_generation import RoomGenerator


def longest_path_in_mst_strategy(
    dungeon_width: int,
    dungeon_height: int,
    max_rooms: int,
    player_transform: tuple[int, int],
    room_min_size=3,
    room_max_size=10,
    tunnel_width=1,
) -> tuple[list, list]:
    room_generator = RoomGenerator()

    rooms = room_generator.generate_rooms(
        dungeon_width,
        dungeon_height,
        max_rooms,
        room_min_size,
        room_max_size,
        player_transform.x,
        player_transform.y,
    )

    room_centers = [room.center for room in rooms]
    mst = MinimumSpanningTreeFinder(room_centers)

    # For reach index in the list of points in longest path, get the room that
    connected_rooms = [
        rooms[i]
        for i in GraphExplorer(
            mst.minimum_spanning_tree, room_centers
        ).points_of_longest_path
    ]
    # Check to see if the the first room in the rooms list is in the connected rooms list and if it is not append it front of the list
    if rooms[0] not in connected_rooms:
        connected_rooms.insert(0, rooms[0])

    tunnels = room_generator.generate_tunnels(tunnel_width, connected_rooms)

    return rooms, tunnels


def basic_generation_strategy(
    game_map: GameMap,
    max_rooms,
    room_min_size=3,
    room_max_size=10,
    player_transform: tuple[int, int] = (0, 0),
    tunnel_width=1,
) -> tuple[list, list]:
    room_generator = RoomGenerator()
    rooms = []
    tunnels = []

    generated_rooms = room_generator.generate_rooms(
        game_map.width,
        game_map.height,
        max_rooms,
        room_min_size,
        room_max_size,
        player_transform.x,
        player_transform.y,
    )
    for room in generated_rooms:
        rooms.append(room)

    tunnels = room_generator.generate_tunnels(tunnel_width, rooms)
    return rooms, tunnels

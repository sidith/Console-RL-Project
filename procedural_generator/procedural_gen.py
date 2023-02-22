# procedual_gen.py
import logging
import random

import yaml
from numpy import block

from console_game_engine import entity, entity_factories
from console_game_engine.colors import colors
from console_game_engine.entity import Entity
from console_game_engine.game_map import GameMap
from procedural_generator.delaunay_triangulation import DelaunayMST

from .room_generation import RectangularRoom, RoomGenerator

with open("logging.yaml", "rt") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
procedrual_gen_logger = logging.getLogger("procedural_gen")


# This is the function that actualy generates the dungeon
def generate_dungeon(
    game_map: GameMap,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    player: Entity,
    max_monsters_per_room=3,
    max_items_per_room=2,
):
    dungeon_width = game_map.width
    dungeon_height = game_map.height

    procedrual_gen_logger.debug("Generating dungeom using room and tunnel gen...\n")

    # rooms, tunnels = basic_generation_strategy(
    #     game_map, max_rooms, room_min_size, room_max_size, player_transform)

    rooms, tunnels = dulaunay_triangulation_strategy(
        dungeon_width=dungeon_width,
        dungeon_height=dungeon_height,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        player_transform=player.transform,
    )
    # A string that is a list of all the rooms and tunnels sepertaed by a new line
    rooms_str = "\n".join(str(room) for room in rooms)
    tunnels_str = "\n".join(str(tunnel) for tunnel in tunnels)

    procedrual_gen_logger.debug(
        f"\n\nRooms: \n{rooms_str}" f"\n\nTunnels:\n{tunnels_str}\n"
    )

    procedrual_gen_logger.debug("Rendering rooms and tunnels...\n")
    for room in rooms:
        game_map.add_room_to_game_map(room, tile_type="floor", slice_type="inner")
    for tunnel in tunnels:
        game_map.add_room_to_game_map(tunnel, tile_type="floor", slice_type="outer")

    monsters = generate_monsters(game_map, rooms, max_monsters_per_room)

    for monster in monsters:
        game_map.entities.add(monster)


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
        player_transform,
    )
    for room in generated_rooms:
        rooms.append(room)

    tunnels = room_generator.generate_tunnels(tunnel_width, rooms)
    return rooms, tunnels


def generate_monsters(
    game_map: GameMap, rooms: list[RectangularRoom], max_monster_per_room: int
) -> list[Entity]:
    monsters = []
    for room in rooms:
        if room.room_type == "Spawn_Room":
            continue

        number_of_monsters = random.randint(0, max_monster_per_room)
        for _ in range(number_of_monsters):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if random.random() < 0.8:
                entity_factories.orc.spawn(game_map, x, y)
            else:
                entity_factories.troll.spawn(game_map, x, y)

    return monsters


def dulaunay_triangulation_strategy(
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
        player_transform,
    )

    room_centers = [room.center for room in rooms]
    delaunayMST = DelaunayMST(room_centers)

    # For reach index in the list of points in longest path, get the room that
    connected_rooms = [rooms[i] for i in delaunayMST.points_of_longest_path]
    # Check to see if the the first room in the rooms list is in the connected rooms list and if it is not append it front of the list
    if rooms[0] not in connected_rooms:
        connected_rooms.insert(0, rooms[0])

    tunnels = room_generator.generate_tunnels(tunnel_width, connected_rooms)

    return rooms, tunnels

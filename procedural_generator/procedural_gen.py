# procedual_gen.py
import logging
import random
import yaml

from console_game_engine import entity_factories
from console_game_engine.colors import colors
from console_game_engine.entity import Entity
from console_game_engine.game_map import GameMap
from procedural_generator.generation_strategies import longest_path_in_mst_strategy
from procedural_generator.graph_explorer import GraphExplorer
from procedural_generator.minimum_spanning_tree_finder import MinimumSpanningTreeFinder


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

    rooms, tunnels = longest_path_in_mst_strategy(
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


def generate_monsters(
    game_map: GameMap, rooms: list[RectangularRoom], max_monster_per_room: int
) -> list[Entity]:
    monsters = []
    for room in rooms:
        if room.room_type == "Spawn_Room":
            continue

        number_of_monsters = random.randint(0, max_monster_per_room)
        for _ in range(number_of_monsters):
            x, y = find_point_in_room(room)

            if random.random() < 0.8:
                entity_factories.orc.spawn(game_map, x, y)
            else:
                entity_factories.troll.spawn(game_map, x, y)

    return monsters


def find_point_in_room(room):
    x = random.randint(room.x1 + 1, room.x2 - 1)
    y = random.randint(room.y1 + 1, room.y2 - 1)
    return x, y

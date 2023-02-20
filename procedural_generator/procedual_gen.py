# procedual_gen.py
from optparse import Option
import random
from typing import Tuple
from console_game_engine.entity import Entity
from console_game_engine.game_map import GameMap
import logging
from procedural_generator.room_generation import RectangularRoom, RoomGenerator
from console_game_engine.colors import colors

# This function generates a room that is centered on the player
logging.basicConfig(filename='logs/proc_gen.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# This is the function that actualy generates the dungeon
def generate_dungeon(game_map: GameMap, max_rooms: int, room_min_size: int, room_max_size: int, player_transform: Tuple[int, int], debug_log: bool = False, max_monsters_per_room=3, max_items_per_room=2):

    logger.info('Generating dungeon...')
    rooms, tunnels = room_and_tunnel_generator(
        game_map, max_rooms, room_min_size, room_max_size, player_transform)
    logger.debug(f'Rooms: {rooms}, and tunnels: {tunnels}')

    logger.debug('Painting rooms and tunnels...')
    for room in rooms:
        game_map.add_room_to_game_map(
            room, tile_type='floor', slice_type='inner')
    for tunnel in tunnels:
        game_map.add_room_to_game_map(
            tunnel, tile_type='floor', slice_type='outer')
    logger.debug('Painting rooms and tunnels... Done')

    monsters = generate_monsters(rooms, max_monsters_per_room)

    for monster in monsters:
        game_map.entities.add(monster)


def room_and_tunnel_generator(game_map: GameMap, max_rooms, room_min_size=3, room_max_size=10, player_transform: Tuple[int, int] = (0, 0), tunnel_width=1) -> Tuple[list, list]:
    room_generator = RoomGenerator()
    rooms = []
    tunnels = []

    generated_rooms = room_generator.generate_rooms(
        game_map.width, game_map.height, max_rooms, room_min_size, room_max_size, player_transform, )
    for room in generated_rooms:
        rooms.append(room)

    tunnels = room_generator.generate_tunnels(tunnel_width, rooms)
    return rooms, tunnels


def generate_monsters(rooms: list[RectangularRoom], max_monster_per_room: int) -> list[Entity]:
    monsters = []
    for room in rooms:
        number_of_monsters = random.randint(0, max_monster_per_room)
        for i in range(number_of_monsters):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            monster = Entity('orc', x=x, y=y, char='o', color=colors['green'])

            monsters.append(monster)

    return monsters

import random
from turtle import color
from typing import Optional

import tcod
from console_game_engine import entity_factories

from console_game_engine.colors import colors
from console_game_engine.engine import Engine
from console_game_engine.entity import Entity
from console_game_engine.game_map import GameMap
from console_game_engine.input_handlers import EventHandler


class Configurations:
    """Class to hold the configuration parameters for the game."""

    def __init__(
        self,
        tileset_path: str = "rsrc/dejavu10x10_gs_tc.png",
        screen_width: int = 80,
        screen_height: int = 50,
        lower_margin: int = 10,
        default_room_min_size: int = 5,
        default_room_max_size: int = 10,
        default_max_rooms: int = 20,
        vsync: bool = True,
        flags: int = tcod.context.SDL_WINDOW_RESIZABLE,
        title: str = "Sidith's Roguelike",
        player_entity: Optional[Entity] = None,
        fov_algorithm=tcod.FOV_PERMISSIVE_4,
    ):
        """
        Initialize the configuration parameters.

        Args:
            tileset_path: The path to the tileset file.
            screen_width: The width of the game screen in tiles.
            screen_height: The height of the game screen in tiles.
            lower_margin: The number of tiles to reserve for the UI at the bottom of the screen.
            map_width: The width of the game map in tiles.
            map_height: The height of the game map in tiles.
            default_room_min_size: The default minimum size of a room.
            default_room_max_size: The default maximum size of a room.
            default_max_rooms: The default maximum number of rooms.
            vsync: Whether to enable vertical synchronization.
            flags: The flags to use for the game window.
            title: The title of the game window.
            player_entity: The player Entity object.
        """
        # Screen parameters
        self.tileset = tcod.tileset.load_tilesheet(
            tileset_path, 32, 8, tcod.tileset.CHARMAP_TCOD
        )
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lower_margin = lower_margin

        # Game map parameters
        self.map_width = screen_width
        self.map_height = self.screen_height - lower_margin
        self.default_room_min_size = default_room_min_size
        self.default_room_max_size = default_room_max_size
        self.default_max_rooms = default_max_rooms

        self.event_handler = EventHandler()

        # Entities
        self.entities = {}
        self.game_map = GameMap(self.map_width, self.map_height)

        self.fov_algorithm = fov_algorithm

        # Player
        self.player_entity = player_entity or entity_factories.player.spawn(
            gamemap=self.game_map,
            x=random.randint(0, self.map_width - 1),
            y=random.randint(0, self.map_height - 1),
        )

        self.engine = Engine(
            event_handler=self.event_handler,
            game_map=self.game_map,
            player=self.player_entity,
            fov_algorithm=self.fov_algorithm,
        )

        # Game window parameters
        self.vsync = vsync
        self.flags = flags
        self.title = title

    def __str__(self) -> str:
        return (
            f"Configurations(\n"
            f"    Screen parameters:\n"
            f"      tileset: {self.tileset}\n"
            f"      screen_width: {self.screen_width}\n"
            f"      screen_height: {self.screen_height}\n"
            f"      lower_margin: {self.lower_margin}\n"
            f"    Game map parameters:\n"
            f"      map_width: {self.map_width}\n"
            f"      map_height: {self.map_height}\n"
            f"      default_room_min_size: {self.default_room_min_size}\n"
            f"      default_room_max_size: {self.default_room_max_size}\n"
            f"      default_max_rooms: {self.default_max_rooms}\n"
            f"    Player and NPC entities:\n"
            f"      player_entity: {self.player_entity}\n"
            f"    Event handler and engine:\n"
            f"      event_handler: {self.event_handler}\n"
            f"      game_map: {self.game_map}\n"
            f"      entities: {self.entities}\n"
            f"      engine: {self.engine}\n"
            f"    Game window parameters:\n"
            f"      vsync: {self.vsync}\n"
            f"      flags: {self.flags}\n"
            f"      title: {self.title}\n"
            f")"
        )

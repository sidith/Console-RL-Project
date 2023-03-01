# game_map.py
from typing import TYPE_CHECKING, Optional

import numpy as np
from tcod.console import Console

from console_game_engine import tile_types
from procedural_generator.room_generation import RectangularRoom

from console_game_engine.entity import Entity


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.tiles = np.full(
            (width, height), fill_value=tile_types.tile_types["wall"], order="F"
        )
        self.entities: set(Entity) = set()

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def get_blocking_entity_at_location(self, location_x, location_y):
        for entity in self.entities:
            if entity.blocks_location(location_x, location_y):
                return entity
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        for entity in self.entities:
            transform = entity.transform
            if self.visible[transform.x, transform.y]:
                console.print(
                    x=transform.x, y=transform.y, string=entity.char, fg=entity.color
                )

    def add_room_to_game_map(
        self, room: RectangularRoom, tile_type: str, slice_type: str
    ):
        if slice_type == "inner":
            self.tiles[room.inner] = tile_types.tile_types[tile_type]
        elif slice_type == "outer":
            self.tiles[room.outer] = tile_types.tile_types[tile_type]

    def __str__(self) -> str:
        return f"GameMap with width {self.width} and height {self.height}"

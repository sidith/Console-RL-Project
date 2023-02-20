# game_map.py

from __future__ import annotations

from html import entities
from typing import TYPE_CHECKING, Iterable

import numpy as np
from tcod.console import Console

import console_game_engine.tile_types as tile_types
from console_game_engine.entity import Entity, Transform
from procedural_generator.room_generation import RectangularRoom


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity]) -> None:
        """
        Create a new game map.

        :param width: The width of the map in tiles.
        :param height: The height of the map in tiles.
        """
        self.width, self.height = width, height
        self.tiles = np.full(
            (width, height), fill_value=tile_types.wall, order="F")

        self.entities = set(entities)

        self.visible = np.full(
            (width, height), fill_value=False, order="F")
        self.explored = np.full(
            (width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:

        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Render the map.

        :param console: The console used to render the map.
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        for entity in self.entities:
            transform = entity.transform
            if self.visible[transform.x, transform.y]:
                console.print(x=transform.x, y=transform.y,
                              string=entity.char, fg=entity.color)

    def shift(self, dx: int, dy: int) -> None:
        """ This method shifts the map by the given amount.

        Args:
            dx (int): Distance to shift in the x direction.
            dy (int): Distance to shift in the y direction.
        """
        self.tiles = np.roll(self.tiles, shift=dx, axis=0)
        self.tiles = np.roll(self.tiles, shift=dy, axis=1)

    # This function adds the rooms to the map

    def add_room_to_game_map(self,  room: RectangularRoom, tile_type: str, slice_type: str):
        if slice_type == 'inner':
            self.tiles[room.inner] = tile_types.tile_types[tile_type]
        elif slice_type == 'outer':
            self.tiles[room.outer] = tile_types.tile_types[tile_type]

    def __str__(self) -> str:
        return f'GameMap with width {self.width} and height {self.height}'

# entity.py

import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from console_game_engine.colors import RGB_Color

if TYPE_CHECKING:
    from console_game_engine.game_map import GameMap

T = TypeVar("T", bound="Entity")


@dataclass
class Transform:
    x: int = 0
    y: int = 0


class Entity:
    def __init__(
        self,
        name: str = "<Unnamed>",
        char: str = "?",
        color: RGB_Color = None,
        color_rgb: tuple[int, int, int] = None,
        blocks_movement: bool = False,
    ):
        self.name = name
        self.char = char
        if color:
            self.color = color
        elif color_rgb:
            self.color = RGB_Color(color_rgb)
        else:
            self.color = RGB_Color((255, 255, 255))
        self.transform = Transform()
        self.blocks_movement = blocks_movement

    def spawn(self: T, gamemap: "GameMap", x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.transform.x = x
        clone.transform.y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int):
        self.transform.x += dx
        self.transform.y += dy

    def blocks_location(self, location_x: int, location_y: int) -> bool:
        test = (
            self.blocks_movement
            and self.transform.x == location_x
            and self.transform.y == location_y
        )
        return test

    def __str__(self) -> str:
        return f'Entity {self.name} at: "({self.transform.x}, {self.transform.y})"'

    def __repr__(self) -> str:
        return f'Entity {self.name} at: "({self.transform.x}, {self.transform.y})" at memory location {hex(id(self))}'


# Path: console_game_engine/game_map.py

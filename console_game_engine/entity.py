import copy
from dataclasses import dataclass
from typing import TypeVar

from console_game_engine.colors import RGB_Color
from console_game_engine.game_map import GameMap

T = TypeVar("T", bound="Entity")


@dataclass
class Transform:
    x: int = 0
    y: int = 0


# class Moveable:
#     def move(self, dx: int, dy: int):
#         self.transform.x += dx
#         self.transform.y += dy


class Entity:
    def __init__(self,
                 name: str = '<Unnamed>',
                 char: str = '?',
                 r: int = 255, g: int = 255, b: int = 255,
                 color: RGB_Color = None,
                 blocks_movement: bool = False
                 ):

        self.name = name
        self.char = char
        self.color = color or RGB_Color(r, g, b)
        self.transform = Transform(0, 0)
        self.blocks_movement = blocks_movement

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.transform.x = x
        clone.transform.y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int):
        self.transform.x += dx
        self.transform.y += dy

    def __str__(self) -> str:
        return f'Entity {self.name} at: "({self.transform.x}, {self.transform.y}")'

    def __repr__(self) -> str:
        return f'Entity {self.name} at: "({self.transform.x}, {self.transform.y})" at memory location {hex(id(self))}'

# Path: console_game_engine/game_map.py

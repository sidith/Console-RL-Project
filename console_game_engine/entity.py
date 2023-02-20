from dataclasses import dataclass
from typing import Tuple

from console_game_engine.colors import RGB_Color


@dataclass
class Transform:
    x: int = 0
    y: int = 0


class Moveable:
    def move(self, dx: int, dy: int):
        self.transform.x += dx
        self.transform.y += dy


class Entity:

    """
    Initialize an entity with a transform, color, and a character to represent it.

    You can either provide a `transform` object or individual `x` and `y` values. If no `transform` is provided, the entity will be initialized with a transform at (`x` or 0, `y` or 0), which is the top left corner of the screen. 

    You can either provide a `color` tuple or individual `r`, `g`, and `b` values. If no `color` is provided, the entity will be initialized with a color of (`r` or 255, `g` or 255, `b` or 255).

    You can provide a `char` to represent the entity. If no `char` is provided, the entity will be initialized with a `char` of `!`.

    """

    def __init__(self, name: str, transform: Transform = None, x: int = 0, y: int = 0, color: Tuple[int, int, int] = None, r: int = 255, g: int = 255, b: int = 255, char: str = '!'):
        if transform is not None:
            self.transform = transform
        else:
            self.transform = Transform(x, y)
        if color is not None:
            self.color = color
        else:
            self.color = RGB_Color(r, g, b)
        self.char = char

        self.name = name

    def move(self, dx: int, dy: int):
        self.transform.x += dx
        self.transform.y += dy

    def __str__(self) -> str:
        return f'Entity {self.name} at: "({self.transform.x}, {self.transform.y}")'

    def __repr__(self) -> str:
        return f'Entity {self.name} at: "({self.transform.x}, {self.transform.y})" at memory location {hex(id(self))}'


class MyClass:
    def get_class_name(self):
        return self.__class__.__name__


obj = MyClass()
print(obj.get_class_name())  # Output: "obj"

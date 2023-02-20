from typing import Tuple
import numpy as np
from console_game_engine.colors import colors

graphic_dt = np.dtype(
    [
        # Unicode codepoint.  This means that we can use any character in the Unicode standard.
        ("ch", np.int32),
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors for foreground
        ("bg", "3B"),  # 3 unsigned bytes, for RGB colors for background

    ]
)
# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  # True if this tile can be walked over
        ("transparent", np.bool_),  # True if this tile can be seen through
        ('dark', graphic_dt),  # Graphics for when this tile is not in FOV
        ('light', graphic_dt),  # Graphics for when this tile is in FOV
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:

    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


SHROUD = np.array(
    (ord("."), colors['white'], colors['black']), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord(' '),
        colors['white'],
        colors['nickel']
    ),
    light=(
        ord(' '),
        colors['white'],
        colors['amber']
    )
)


wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(
        ord(' '),
        colors['white'],
        colors['lead']
    ),
    light=(
        ord(' '),
        colors['white'],
        colors['crimson']
    )
)


tile_types = {
    'floor': floor,
    'wall': wall,
}

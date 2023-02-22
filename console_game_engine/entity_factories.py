from .entity import Entity, Transform
from .colors import colors

player = Entity(
    char="@", name="Player", color=colors["neon blue"], blocks_movement=True
)

orc = Entity(char="o", name="Orc", color=colors["teal"], blocks_movement=True)

troll = Entity(char="T", name="Troll", color=colors["olive"], blocks_movement=True)

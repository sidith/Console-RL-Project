from __future__ import annotations
import logging
import random

from typing import TYPE_CHECKING
from matplotlib.widgets import EllipseSelector

import yaml

if TYPE_CHECKING:
    from console_game_engine.engine import Engine
    from console_game_engine.entity import Entity


def setup_action_logging():
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    return logging.getLogger("actions")


# These are the lines that will be printed when the player is in combat.  They are randomly selected from this list.
funny_lines = [
    f"They feel bloodlust in their veins.",
    f"They feel the need to kill.",
    f"They feel the need to destroy.",
    f"They feel the need to maim.",
    f"They feel the need to kill.",
    f"They feel scared",
    f"They sence soemthing is not right",
    f"They lick their lips in anticipation",
    f"...",
]

action_logger = setup_action_logging()


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        action_logger.debug(f"Action performed: " + self.__class__.__name__)
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        action_logger.info("Exiting the game...")
        raise SystemExit()


class DirectionalMovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MovementAction(DirectionalMovementAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.transform.x + self.dx
        dest_y = entity.transform.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            action_logger.info(f"{entity.name}'s destination is out of bounds.")
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            action_logger.info(f"{entity.name}'s destination is blocked.")
            return  # Destination is blocked by a tile.
        entity.move(self.dx, self.dy)
        action_logger.info(f"{entity.name} moved to {dest_x}, {dest_y}")


class MeleeAction(DirectionalMovementAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.transform.x + self.dx
        dest_y = entity.transform.y + self.dy

        blocking_entity = engine.game_map.get_blocking_entity_at_location(
            dest_x, dest_y
        )
        if blocking_entity:
            # This is a bit of a hack, but it works for now
            if blocking_entity.name[0] in [
                "a",
                "e",
                "i",
                "o",
                "u",
                "A",
                "E",
                "I",
                "O",
                "U",
            ]:
                action_logger.info(
                    f"{entity.name} is blocked by an {blocking_entity.name}.\n"
                    + funny_lines[random.randint(0, len(funny_lines) - 1)]
                )
            else:
                action_logger.info(
                    f"{entity.name} is blocked by a {blocking_entity.name}.\n"
                    + funny_lines[random.randint(0, len(funny_lines) - 1)]
                )
            return


class BumpAction(DirectionalMovementAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.transform.x + self.dx
        dest_y = entity.transform.y + self.dy

        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            action_logger.info(f"Nothing interesting is the {entity.name}'s way.")
            return MovementAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MeleeAction(self.dx, self.dy).perform(engine, entity)

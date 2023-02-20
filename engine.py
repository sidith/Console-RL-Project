from typing import Any, Iterable

import tcod
from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

import procedual_gen
from entity import Entity, Transform
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self,
                 event_handler: EventHandler,
                 game_map: GameMap,
                 player: Entity,
                 fov_algorithm: int
                 ) -> None:

        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.fov_algorithm = fov_algorithm
        self.update_fov(self.player.transform, self.fov_algorithm)

    def game_loop(self, config, root_console: Console, context: Context):
        while True:
            config.engine.render(console=root_console, context=context)
            event = tcod.event.wait()
            config.engine.handle_events(event)

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:

            if event == None:
                continue

            action = self.event_handler.dispatch(event)
            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov(self.player.transform, self.fov_algorithm)

    # Update this function so that it takes in a list of entities that need to have their FOV updated.

    def update_fov(self, transform: Transform, fov_algorithm) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (transform.x, transform.y),
            radius=10,
            algorithm=fov_algorithm,
            light_walls=True)
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:

        self.game_map.render(console)

        context.present(console)
        console.clear()

    def generate_dungeon(self, max_rooms: int, min_room_size: int, max_room_size: int):
        procedual_gen.generate_dungeon(
            self.game_map, max_rooms, min_room_size, max_room_size, self.player.transform, debug_log=True)

    def __str__(self) -> str:
        return f'Engine(event_handler={self.event_handler}, game_map={self.game_map}, player={self.player})'

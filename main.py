# main.py
import logging.config

import tcod
import yaml

from configurations import Configurations


def setup_game_logging():
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    return logging.getLogger("game")


def main(config: Configurations, game_logger):
    # Use the context manager to create the terminal context and ensure that it is properly cleaned up.
    with tcod.context.new_terminal(
        config.screen_width,
        config.screen_height,
        tileset=config.tileset,
        title=config.title,
        vsync=config.vsync,
        sdl_window_flags=config.flags,
    ) as context:
        game_logger.debug(
            f"Game context created with the following configurations:\n{config}\n\n"
        )

        root_console = tcod.Console(
            config.screen_width, config.screen_height, order="F"
        )

        # Generate the default dungeon using the default configuration parameters.
        config.engine.generate_dungeon(
            config.default_max_rooms,
            config.default_room_min_size,
            config.default_room_max_size,
        )
        game_logger.debug(
            f"Dungeon generated with the following map:\n{config.engine.game_map}\n"
        )

        game_logger.debug("Starting the game loop...")
        # Start the game loop, passing in the configuration object, the root console, and the terminal context.
        config.engine.game_loop(config, root_console, context)


if __name__ == "__main__":
    game_logger = setup_game_logging()
    game_logger.debug("Cleaning up the log..." + ("\n" * 2))
    game_logger.debug("=" * 80)
    game_logger.debug("Initializing the game...")
    game_logger.debug(("=" * 80) + "\n")

    config = Configurations()
    main(config, game_logger)


# set up a logger for the game
import logging.config

import tcod
import yaml

from configurations import Configurations


def setup_logging():
    with open('logging.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    return logging.getLogger('game')


def main(config: Configurations, game_logger):
    game_logger.debug('Creating the game context.')

    # Use the context manager to create the terminal context and ensure that it is properly cleaned up.
    with tcod.context.new_terminal(
        config.screen_width,
        config.screen_height,
        tileset=config.tileset,
        title=config.title,
        vsync=config.vsync,
        sdl_window_flags=config.flags
    ) as context:
        game_logger.debug(
            f'Game context created with the following configurations: {config}\n\n')

        game_logger.debug(
            'Creating the root console')
        root_console = tcod.Console(
            config.screen_width, config.screen_height, order='F')

        # Generate the default dungeon using the default configuration parameters.
        game_logger.debug(
            f'Generating default dungeon...')
        config.engine.generate_dungeon(
            config.default_max_rooms, config.default_room_min_size, config.default_room_max_size
        )
        game_logger.debug(
            f'Dungeon generated with the following map:\n{config.engine.game_map}\n\n')

        game_logger.debug('Starting the game loop...')
        # Start the game loop, passing in the configuration object, the root console, and the terminal context.
        config.engine.game_loop(config, root_console, context)


if __name__ == '__main__':
    game_logger = setup_logging()

    game_logger.debug('='*80)
    game_logger.debug('Initializing the game...')
    game_logger.debug('='*80)

    game_logger.debug('Loading the configurations...')
    config = Configurations()
    game_logger.debug('Configurations loaded')

    main(config, game_logger)

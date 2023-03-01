# test_game_map.py

from console_game_engine import tile_types
from console_game_engine.entity import Entity
from console_game_engine.game_map import GameMap
from procedural_generator.room_generation import RectangularRoom


def test_game_map_constructor():
    # Test default constructor values
    gamemap = GameMap(width=10, height=10)
    assert gamemap.width == 10
    assert gamemap.height == 10
    assert gamemap.tiles.shape == (10, 10)
    assert gamemap.entities == set()
    assert gamemap.visible.shape == (10, 10)
    assert gamemap.explored.shape == (10, 10)


def test_game_map_in_bounds():
    gamemap = GameMap(width=10, height=10)
    assert gamemap.in_bounds(x=5, y=5) == True
    assert gamemap.in_bounds(x=11, y=5) == False
    assert gamemap.in_bounds(x=5, y=11) == False


def test_game_map_render():
    gamemap = GameMap(width=10, height=10)
    console = None  # TODO: Create a mock console for testing
    # TODO: Create entities and tiles, set visibility and explored maps, and call gamemap.render()
    # assert console.tiles_rgb is correctly set


# def test_game_map_add_room_to_game_map():
#     gamemap = GameMap(width=10, height=10)
#     room = RectangularRoom(x=0, y=0, width=5, height=5)
#     gamemap.add_room_to_game_map(room=room, tile_type="floor", slice_type="inner")
#     assert (gamemap.tiles[0:5, 0:5] == tile_types.tile_types["floor"]).all()
#     gamemap.add_room_to_game_map(room=room, tile_type="wall", slice_type="outer")
#     assert (gamemap.tiles[0:5, 0:5] == tile_types.tile_types["wall"]).all()


# def test_game_map_get_blocking_entity_at_location():
#     gamemap = GameMap(width=10, height=10)
#     player = Entity(char="@", name="Player", blocks_movement=True)
#     orc = Entity(char="o", name="Orc", blocks_movement=True)
#     gamemap.entities.add(player)
#     gamemap.entities.add(orc)
#     assert gamemap.get_blocking_entity_at_location(location_x=0, location_y=0) is None
#     assert gamemap.get_blocking_entity_at_location(location_x=1, location_y=0) == player
#     assert gamemap.get_blocking_entity_at_location(location_x=0, location_y=1) == orc

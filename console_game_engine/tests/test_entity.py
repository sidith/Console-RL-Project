# test_entity.py

from console_game_engine.entity import Entity
from console_game_engine.game_map import GameMap

# test_entity.py

from console_game_engine.entity import Entity, Transform, RGB_Color


def test_entity_constructor():
    # Test default constructor values
    entity = Entity()
    assert entity.name == "<Unnamed>"
    assert entity.char == "?"
    assert entity.color == RGB_Color((255, 255, 255))
    assert entity.transform.x == 0
    assert entity.transform.y == 0
    assert entity.blocks_movement == False

    # Test constructor with name, char, and color
    entity = Entity(name="Test Entity", char="T", color=RGB_Color((255, 0, 0)))
    assert entity.name == "Test Entity"
    assert entity.char == "T"
    assert entity.color == RGB_Color((255, 0, 0))
    assert entity.transform.x == 0
    assert entity.transform.y == 0
    assert entity.blocks_movement == False

    # Test constructor with name, char, and RGB color values
    entity = Entity(name="Test Entity", char="T", color_rgb=((255, 0, 0)))
    assert entity.name == "Test Entity"
    assert entity.char == "T"
    assert entity.color == RGB_Color((255, 0, 0))
    assert entity.transform.x == 0
    assert entity.transform.y == 0
    assert entity.blocks_movement == False


def test_entity_spawn():
    # Test spawning an entity on a game map
    from console_game_engine.game_map import GameMap

    gamemap = GameMap(width=10, height=10)
    entity = Entity()
    entity.spawn(gamemap, x=5, y=5)
    assert len(gamemap.entities) == 1
    assert gamemap.entities.pop() is not entity


def test_entity_move():
    # Test moving an entity
    entity = Entity()
    entity.move(dx=1, dy=2)
    assert entity.transform.x == 1
    assert entity.transform.y == 2


def test_entity_blocks_location():
    # Test blocking movement at a specific location
    entity = Entity(blocks_movement=True)
    entity.transform.x = 5
    entity.transform.y = 5
    assert entity.blocks_location(location_x=5, location_y=5) == True
    assert entity.blocks_location(location_x=6, location_y=5) == False
    assert entity.blocks_location(location_x=5, location_y=6) == False


def test_entity_str():
    # Test string representation of entity
    entity = Entity(name="Test Entity", char="T")
    print("entity:", entity)
    assert str(entity) == 'Entity Test Entity at: "(0, 0)"'


def test_entity_repr():
    # Test string representation of entity
    entity = Entity(name="Test Entity", char="T")
    print("entity:", repr(entity))
    assert (
        repr(entity)
        == f'Entity Test Entity at: "(0, 0)" at memory location {hex(id(entity))}'
    )


# Path: console_game_engine/tests/test_game_map.py

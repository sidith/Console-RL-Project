# import pytest
# from console_game_engine.game_map import GameMap
# from procedural_generator.generation_strategies import basic_generation_strategy


# @pytest.fixture
# def game_map():
#     width, height = 50, 50
#     return GameMap(width, height, [])


# def test_basic_generation_strategy(game_map):
#     max_rooms = 5
#     room_min_size = 5
#     room_max_size = 10
#     player_transform = (0, 0)
#     tunnel_width = 1

#     rooms, tunnels = basic_generation_strategy(
#         game_map,
#         max_rooms,
#         room_min_size=room_min_size,
#         room_max_size=room_max_size,
#         player_transform=player_transform,
#         tunnel_width=tunnel_width,
#     )

#     # Ensure the correct number of rooms was generated
#     assert len(rooms) == max_rooms

#     # Ensure all rooms are within the boundaries of the game map
#     for room in rooms:
#         assert room.x1 >= 1
#         assert room.x2 <= game_map.width - 1
#         assert room.y1 >= 1
#         assert room.y2 <= game_map.height - 1

#     # Ensure all tunnels are within the boundaries of the game map
#     for tunnel in tunnels:
#         for x, y in tunnel:
#             assert x >= 1
#             assert x < game_map.width - 1
#             assert y >= 1
#             assert y < game_map.height - 1

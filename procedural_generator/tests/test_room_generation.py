from procedural_generator.room_generation import RectangularRoom, RoomGenerator


def test_rectangular_room_center():
    room = RectangularRoom(x=1, y=1, width=3, height=3)
    assert room.center == (2, 2)


def test_rectangular_room_inner_slice():
    room = RectangularRoom(x=1, y=1, width=3, height=3)
    assert room.inner == (slice(2, 4), slice(2, 4))


def test_rectangular_room_outer_slice():
    room = RectangularRoom(x=1, y=1, width=3, height=3)
    assert room.outer == (slice(1, 4), slice(1, 4))


def test_rectangular_room_intersects():
    room1 = RectangularRoom(x=1, y=1, width=3, height=3)
    room2 = RectangularRoom(x=3, y=3, width=3, height=3)
    room3 = RectangularRoom(x=6, y=6, width=3, height=3)
    assert room1.intersects(room2) == True
    assert room1.intersects(room3) == False


def test_room_generator_generate_rooms():
    generator = RoomGenerator()
    rooms = generator.generate_rooms(
        map_width=100,
        map_height=100,
        max_rooms=10,
        room_min_size=3,
        room_max_size=5,
        spawn_x=1,
        spawn_y=1,
    )
    print(len(rooms))
    assert (len(rooms) <= 11) and (
        len(rooms) > 1
    )  # 1 room is the spawn room and the rest are randomly generated rooms up to 10


def test_room_generator_generate_tunnels():
    generator = RoomGenerator()
    rooms = [
        RectangularRoom(x=1, y=1, width=3, height=3),
        RectangularRoom(x=6, y=6, width=3, height=3),
        RectangularRoom(x=3, y=3, width=3, height=3),
    ]
    tunnels = generator.generate_tunnels(tunnel_width=1, rooms=rooms)
    assert len(tunnels) == (len(rooms) - 1) * 2  # 2 tunnel between each room

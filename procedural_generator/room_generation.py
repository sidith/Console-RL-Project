# room_generation.py
import random
from venv import create

# This file contains the code for generating the rooms and tunnels for the dungeon
# A class that represents a room in the dungeon


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int, type: str = "default"):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.room_type = type

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    @property
    def inner(self):
        return (slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2))

    @property
    def outer(self):
        return (slice(self.x1, self.x2), slice(self.y1, self.y2))

    def intersects(self, other: "RectangularRoom") -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

    def __str__(self):
        return (
            f"{self.room_type} at ({self.x1}, {self.y1}) "
            f"with width {self.width} and height {self.height} "
        )

    def __repr__(self):
        return (
            f"{self.room_type} at ({self.x1}, {self.y1}) "
            f"with width {self.width} and height {self.height} "
            f"At memory location {hex(id(self))}"
        )


class RoomGenerator:
    def generate_tunnels(
        self, tunnel_width: int, rooms: list[RectangularRoom]
    ) -> list[RectangularRoom]:
        tunnels = []

        if len(rooms) <= 1:
            return tunnels

        # This loop works by taking the first room in the list and connecting it to the second room in the list. Then it takes the second room in the list and connects it to the third room in the list. It does this until it reaches the last room in the list. Then it takes the last room in the list and connects it to the first room in the list. This creates a loop of tunnels.
        for room1, room2 in zip(rooms, rooms[1:]):
            tunnel_pair = self.create_horizontal_and_verticle_tunnel(
                room1, room2, tunnel_width
            )
            tunnels.append(tunnel_pair[0])
            tunnels.append(tunnel_pair[1])

        return tunnels

    def create_horizontal_and_verticle_tunnel(
        self,
        staring_room: RectangularRoom,
        ending_room: RectangularRoom,
        tunnel_width=1,
    ) -> list[RectangularRoom]:
        x1, y1 = staring_room.center
        x2, y2 = ending_room.center

        horizontal_tunnel = RectangularRoom(
            min(x1, x2), y1, abs(x1 - x2) + 1, tunnel_width, "Horzontal Tunnel"
        )
        vertical_tunnel = RectangularRoom(
            x2, min(y1, y2), tunnel_width, abs(y1 - y2) + 1, "Vertical Tunnel"
        )

        return [horizontal_tunnel, vertical_tunnel]

    # This function generates the rooms
    def generate_rooms(
        self,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        player_transform: tuple[int, int],
    ) -> list[RectangularRoom]:
        new_rooms = []

        spawn_room = self.create_spawn_room(player_transform)
        new_rooms.append(spawn_room)

        for _ in range(max_rooms):
            x = random.randint(0, map_width - room_max_size - 1)
            y = random.randint(0, map_height - room_max_size - 1)
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)

            new_room = RectangularRoom(x, y, w, h, "Basic_Room")
            if any(other_room.intersects(new_room) for other_room in new_rooms):
                continue
            else:
                new_rooms.append(new_room)

        return new_rooms

    # this function creates the spawn room
    def create_spawn_room(
        self, player_transform: tuple[int, int], spawn_room_size: int = 6
    ) -> RectangularRoom:
        spawn_room = RectangularRoom(
            player_transform.x - 3,
            player_transform.y - 3,
            spawn_room_size,
            spawn_room_size,
            "Spawn_Room",
        )
        return spawn_room

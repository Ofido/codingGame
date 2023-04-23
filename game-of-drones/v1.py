import math
import sys

# default values
# A zone is a circle with a radius of 100 units.
ZONE_RADIO_LENGHT: int = 100

# p: number of players in the game (2 to 4 players)
# _id: ID of your player (0, 1, 2, or 3)
# d: number of drones in each team (3 to 11)
# z: number of zones on the map (4 to 8)
PLAYERS_QUANTITY, MY_ID, DRONES_NUMBER_OF_EACH_ONE, NUMBER_OF_ZONES = [
    int(i) for i in input().split()
]

print(f"PLAYERS_QUANTITY {PLAYERS_QUANTITY}", file=sys.stderr, flush=True)
print(f"MY_ID {MY_ID}", file=sys.stderr, flush=True)
print(
    f"DRONES_NUMBER_OF_EACH_ONE {DRONES_NUMBER_OF_EACH_ONE}",
    file=sys.stderr,
    flush=True,
)
print(f"NUMBER_OF_ZONES {NUMBER_OF_ZONES}", file=sys.stderr, flush=True)


# my classes
class drone:
    id: int = 0
    old_x: int = 0
    old_y: int = 0
    old_future_x: int = 0
    old_future_y: int = 0
    x: int = 0
    y: int = 0
    future_x: int = 0
    future_y: int = 0
    in_zone: int = -1
    lowest_zone: int = 0
    dist_zones: dict = {}
    player: int = 0

    def __init__(self, player: int, id: int) -> None:
        self.player = player
        self.id = id
        self.old_x = 0
        self.old_y = 0
        self.old_future_x = 0
        self.old_future_y = 0
        self.x = 0
        self.y = 0
        self.future_x = 0
        self.future_y = 0
        self.in_zone = -1
        self.lowest_zone = 0
        self.dist_zones = {}
        print(f"drone {id}, player {player} init", file=sys.stderr, flush=True)

    def move(self, x: int, y: int) -> None:
        self.reset()
        print(
            f"drone {self.id} move, player: {self.player}", file=sys.stderr, flush=True
        )
        self.x = x
        self.y = y
        if self.player == MY_ID:
            print(f"my drone {self.id} check move", file=sys.stderr, flush=True)
            self.check_moves()

    def check_moves(self):
        # se ele ainda não chegou em seu destino vá
        # TODO melhorar checagem futura para verificar mudança de destino
        # TODO como se comportar quando já esta dentro da circunferencia do seu obj?
        if (self.old_future_x != self.x or self.old_future_y != self.y) and (
            self.old_future_x != 0 or self.old_future_y != 0
        ):
            self.future_x = self.old_future_x
            self.future_y = self.old_future_y
            return

        self.check_distances()

        # TODO como se comportar quando já esta dentro da circunferencia do seu obj?
        self.future_x = ZONES[self.lowest_zone].center_x
        self.future_y = ZONES[self.lowest_zone].center_y

    def check_distances(self):
        for zone_id in range(NUMBER_OF_ZONES):
            self.distance_zone(ZONES[zone_id])
        lowest = self.dist_zones[0]
        lowest_id = 0
        for zone_id in list(self.dist_zones):
            if (dist := self.dist_zones[zone_id]) < lowest:
                lowest = dist
                lowest_id = zone_id
        self.lowest_zone = lowest_id

    def reset(self) -> None:
        self.old_x = self.x
        self.old_y = self.y
        self.old_future_x = self.future_x
        self.old_future_y = self.future_y
        self.lowest_zone = 0
        self.dist_zones = {}
        self.future_x = 0
        self.future_y = 0
        self.in_zone = 0

    def distance_zone(self, zone):
        dist = zone.distance(self)
        if dist <= ZONE_RADIO_LENGHT:
            self.in_zone = zone.id
        self.dist_zones[zone.id] = dist

    def get_location(self):
        return self.x, self.y

    def get_future_location(self):
        return self.future_x, self.future_y

    def do_move(self):
        print(
            f"drone {self.id} is moving to {self.future_x} {self.future_y}",
            file=sys.stderr,
            flush=True,
        )
        return f"{self.future_x} {self.future_y}"


class player:
    id: int = 0
    me: bool
    drones: dict[int, drone] = {}

    def __init__(self, id) -> None:
        self.id = id

    def its_me(self) -> None:
        print(f"my id is {self.id}", file=sys.stderr, flush=True)
        self.me = True

    def move_drone(self, id, x, y) -> None:
        print(f"try drone {id} move", file=sys.stderr, flush=True)
        self.drones[id].move(x, y)


class zone:
    id: int = 0
    controled_by: int = -1
    center_x: int = 0
    center_y: int = 0
    drones_inside: list = []

    def __init__(self, id, center_x, center_y) -> None:
        self.id = id
        self.center_x = center_x
        self.center_y = center_y

    def get_center(self):
        return self.center_x, self.center_y

    def distance(self, drone):
        dist = math.dist(self.get_center(), drone.get_location())
        if dist <= ZONE_RADIO_LENGHT:
            self.drones_inside.append(drone)
        return dist


PLAYERS: dict[int, player] = {}
ZONES: dict[int, zone] = {}

for player_id in range(PLAYERS_QUANTITY):
    PLAYERS[player_id] = player(player_id)
    PLAYERS[player_id].drones = {
        drone_id: drone(player_id, drone_id)
        for drone_id in range(DRONES_NUMBER_OF_EACH_ONE)
    }

PLAYERS[MY_ID].its_me()

for zone_id in range(NUMBER_OF_ZONES):
    # x y: corresponds to the position of the center of a zone.
    x, y = [int(j) for j in input().split()]
    ZONES[zone_id] = zone(zone_id, x, y)

# game loop
while True:
    # ID of the team controlling the zone (0, 1, 2, or 3)
    # -1 if it is not controlled.
    # The zones are given in the same order as in the initialization.
    for zone_id in range(NUMBER_OF_ZONES):
        ZONES[zone_id].controled_by = int(input())
    # dx: The first D lines contain the coordinates of drones of a player with the ID 0,
    # the following D lines those of the drones of player 1, and thus it continues until
    # the last player.vscode
    for player_id in range(PLAYERS_QUANTITY):
        for drone_id in range(DRONES_NUMBER_OF_EACH_ONE):
            dx, dy = [int(k) for k in input().split()]
            PLAYERS[player_id].move_drone(drone_id, dx, dy)

    # desicion part make to each drone

    # output a destination point to be reached by one of your drones.
    # The first line corresponds to the first of your drones
    # that you were provided as input, the next to the second, etc.
    for drone_id in range(DRONES_NUMBER_OF_EACH_ONE):
        print(PLAYERS[MY_ID].drones[drone_id].do_move())

# To debug: print("Debug messages...", file=sys.stderr, flush=True)

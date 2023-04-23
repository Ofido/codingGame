# import math
import sys

# set default values
GAME_ZONE_WIDE = 16000
GAME_ZONE_HIGH = 9000

PLAYER_SPEED = 1000
PLAYER_KILL_RADIUS = 2000

ZOMBIE_SPEED = 400
ZOMBIE_KILL_RADIUS = 400


def aux(x, y) -> str:
    return f"{x} {y}"


# objects
class human:
    id: int
    old_x: int
    old_y: int
    pos_x: int
    pos_y: int
    is_alive: bool
    is_secure: bool
    have_zombie_comming: bool

    def __init__(self, id: int, pos_x: int, pos_y: int) -> None:
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.old_x = 0
        self.old_y = 0
        self.is_alive = True
        self.is_secure = True

    def move(self, pos_x: int, pos_y: int) -> None:
        self.old_x = self.pos_x
        self.old_y = self.pos_y
        self.pos_x = pos_x
        self.pos_y = pos_y

    def att_zombie_comming(self, zombie) -> None:
        self.have_zombie_comming = zombie.line_equ(self.pos_x, self.pos_y)

    def get_pos(self) -> tuple:
        return self.pos_x, self.pos_y

    def __to_dict__(self) -> dict:
        return {
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "is_alive": self.is_alive,
            "is_secure": self.is_secure,
        }

    def __str__(self) -> str:
        return f"human {self.id} att: {self.__to_dict__()}"


class humans:
    list_of_humans: dict[int, human]
    died_humans: dict[int, human]
    turn_movies: list[int]

    def __init__(self, list_of_humans: list) -> None:
        self.list_of_humans = {}
        self.died_humans = {}
        self.turn_movies = []
        for a in list_of_humans:
            hu = human(*a)
            self.list_of_humans[hu.id] = hu

    def move_someone(self, id, x, y):
        self.list_of_humans[id].move(x, y)
        self.turn_movies.append(id)

    def zombie_move(self, zombie):
        for hu in self.list_of_humans:
            self.list_of_humans[hu].is_secure = not zombie.line_equ(
                *self.list_of_humans[hu].get_pos()
            )

    def quantity_humans(self):
        return len(self.list_of_humans)

    def get_survivor_pos(self):
        return self.list_of_humans[list(self.list_of_humans)[0]].get_pos()

    def reset_turn(self):
        all_humans_alive = list(self.list_of_humans)
        for human_movies in self.turn_movies:
            all_humans_alive.remove(human_movies)
        for died_human in all_humans_alive:
            self.died_humans[died_human] = self.list_of_humans[died_human]
            del self.list_of_humans[died_human]

    def __str__(self) -> str:
        return "\n".join([str(self.list_of_humans[hu]) for hu in self.list_of_humans])


class zombie:
    id: int
    pos_x: int
    pos_y: int
    future_x: int
    future_y: int
    is_alive: bool
    kill_chance: list[str]

    def __init__(
        self, id: int, pos_x: int, pos_y: int, future_x: int, future_y: int
    ) -> None:
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.future_x = future_x
        self.future_y = future_y
        self.is_alive = True
        self.kill_chance = []

    def get_pos(self) -> tuple:
        return self.future_x, self.future_y

    def move(self, pos_x: int, pos_y: int, future_x: int, future_y: int) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.future_x = future_x
        self.future_y = future_y

    def line_equ(self, x, y) -> bool:
        # determinante --> equaçãoda reta de movimentação do zumbi sendo x e y o humano
        return (
            (self.pos_x * self.future_y)
            + (self.pos_y * x)
            + (self.future_x * y)
            - (x * self.future_y)
            - (y * self.pos_x)
            - (self.future_x * self.pos_y)
        ) == 0

    def __to_dict__(self):
        return {
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "future_x": self.future_x,
            "future_y": self.future_y,
            "kill_chance": self.kill_chance,
        }

    def __str__(self) -> str:
        return f"zombie {self.id} att: {self.__to_dict__()}"


class zombies:
    list_of_zombies: dict[int, zombie]

    def __init__(self, list_of_zombies: list) -> None:
        self.list_of_zombies = {}
        for a in list_of_zombies:
            zo = zombie(*a)
            self.list_of_zombies[zo.id] = zo

    def get_survivor_pos(self):
        return self.list_of_zombies[list(self.list_of_zombies)[0]].get_pos()

    def get_zombies(self):
        return (self.list_of_zombies[z] for z in list(self.list_of_zombies))

    def move_someone(
        self, id: int, pos_x: int, pos_y: int, future_x: int, future_y: int
    ):
        self.list_of_zombies[id].move(pos_x, pos_y, future_x, future_y)

    def __str__(self) -> str:
        return "\n".join([str(self.list_of_zombies[zo]) for zo in self.list_of_zombies])


class player:
    old_x: int
    old_y: int
    pos_x: int
    pos_y: int
    future_x: int
    future_y: int
    kill_chance: list[str]
    save_chance: list[str]

    def __init__(self, x, y) -> None:
        self.old_x: int = 0
        self.old_y: int = 0
        self.pos_x: int = x
        self.pos_y: int = y
        self.future_x: int = 0
        self.future_y: int = 0
        self.kill_chance: list[str] = []
        self.save_chance: list[str] = []

    def move(self, new_x: int, new_y: int) -> None:
        print("player move", file=sys.stderr, flush=True)
        # set old
        self.old_x = self.pos_x
        self.old_y = self.pos_y

        # set new
        self.pos_x = new_x
        self.pos_y = new_y

        # FIXME reset future?
        self.future_x = 0
        self.future_y = 0

    def get_pos(self) -> tuple:
        return self.pos_x, self.pos_y

    def __to_dict__(self):
        return {
            "old_x": self.old_x,
            "old_y": self.old_y,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "future_x": self.future_x,
            "future_y": self.future_y,
            "kill_chance": self.kill_chance,
            "save_chance": self.save_chance,
        }

    def __str__(self) -> str:
        return f"player att: {self.__to_dict__()}"


# set dict of entities
# 'first' game loop
print("first", file=sys.stderr, flush=True)
PLAYER: player = player(*[int(i) for i in input().split()])
print(f"player {PLAYER}", file=sys.stderr, flush=True)
HUMANS: humans = humans(
    [[int(j) for j in input().split()] for _ in range(int(input()))]
)
print(f"humans {HUMANS}", file=sys.stderr, flush=True)
ZOMBIES: zombies = zombies(
    [[int(j) for j in input().split()] for _ in range(int(input()))]
)
print(f"zombies {ZOMBIES}", file=sys.stderr, flush=True)
print(aux(*PLAYER.get_pos()))
# game loop
while True:
    output = ""
    print("game loop", file=sys.stderr, flush=True)
    print("set vars", file=sys.stderr, flush=True)
    print("set player", file=sys.stderr, flush=True)
    PLAYER.move(*[int(i) for i in input().split()])
    human_count = int(input())
    print("set human", file=sys.stderr, flush=True)
    for i in range(human_count):
        HUMANS.move_someone(*[int(j) for j in input().split()])

    zombie_count = int(input())
    print("set zombie", file=sys.stderr, flush=True)
    for i in range(zombie_count):
        ZOMBIES.move_someone(*[int(j) for j in input().split()])

    print("desicions", file=sys.stderr, flush=True)

    if HUMANS.quantity_humans() == 0:
        output = aux(*ZOMBIES.get_survivor_pos())
    if HUMANS.quantity_humans() == 1 and not output:
        output = aux(*HUMANS.get_survivor_pos())

    if not output:
        for z in ZOMBIES.get_zombies():
            HUMANS.zombie_move(z)

        # TODO: VERIFICAR HUMANO MAIS PROXIMO DE UM ZUMBI
        # TODO: IR ATÉ O PONTO MÉDIO DO CAMINHO PARA SER MAIS RAPIDO

    # Your destination coordinates
    print(output)
    output = ""
    HUMANS.reset_turn()

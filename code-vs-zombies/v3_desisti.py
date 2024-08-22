import math
import sys


class Entity:
    def __init__(self, entity_id: int, x: int, y: int):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        print(f"Debug: Created Entity ID {entity_id} at ({x}, {y})", file=sys.stderr, flush=True)

    def update_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        print(f"Debug: Updated Entity ID {self.entity_id} to new position ({x}, {y})", file=sys.stderr, flush=True)

    def distance_to(self, other: "Entity") -> float:
        if isinstance(other, Zombie):
            return math.sqrt((self.x - other.next_x) ** 2 + (self.y - other.next_y) ** 2)
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Human(Entity):
    pass


class Zombie(Entity):
    def __init__(self, entity_id: int, x: int, y: int, next_x: int = None, next_y: int = None):
        super().__init__(entity_id, x, y)
        self.next_x = next_x
        self.next_y = next_y
        print(
            f"Debug: Zombie ID {self.entity_id} - Next Position ({self.next_x}, {self.next_y})",
            file=sys.stderr,
            flush=True,
        )

    def update_position(self, x: int, y: int, next_x: int, next_y: int) -> None:
        super().update_position(x, y)
        self.next_x = next_x
        self.next_y = next_y
        print(
            f"Debug: Updated Zombie ID {self.entity_id} - Next Position ({self.next_x}, {self.next_y})",
            file=sys.stderr,
            flush=True,
        )

    def future_position(self) -> tuple[int, int]:
        return self.next_x, self.next_y


class Ash(Entity):
    def move_towards(self, target_x: int, target_y: int) -> None:
        dist = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        if dist <= 1000:
            self.x, self.y = target_x, target_y
        else:
            direction_x = (target_x - self.x) / dist
            direction_y = (target_y - self.y) / dist
            self.x += int(direction_x * 1000)
            self.y += int(direction_y * 1000)
        print(f"Debug: Ash moving towards ({self.x}, {self.y})", file=sys.stderr, flush=True)


class Humans:
    def __init__(self, list_of_humans: list):
        self.humans = [Human(*human) for human in list_of_humans]

    def update_humans(self, list_of_humans: list) -> None:
        self.humans = [Human(*human) for human in list_of_humans]

    def find_most_threatened(self, zombies: "Zombies", ash: Ash) -> Human:
        savable_humans = []

        for human in self.humans:
            closest_distance = min(
                a if a > 0 else float("inf") for a in [human.distance_to(zombie) for zombie in zombies.zombies]
            )
            dist_to_ash = ash.distance_to(human)

            # Verifique se o humano está dentro da área de proteção
            print(f"Debug savable_humans {human.entity_id}", file=sys.stderr, flush=True)
            print(f"{closest_distance=}", file=sys.stderr, flush=True)
            print(f"{closest_distance / 400=}", file=sys.stderr, flush=True)
            print(f"{dist_to_ash=}", file=sys.stderr, flush=True)
            print(f"{dist_to_ash / 1000=}", file=sys.stderr, flush=True)
            if closest_distance / 400 > dist_to_ash / 1000:
                savable_humans.append(human)

        print(f"Debug: humans count = {len(self.humans)}", file=sys.stderr, flush=True)
        print(f"Debug: savable_humans count = {len(savable_humans)}", file=sys.stderr, flush=True)
        print(f"Debug: {savable_humans=}", file=sys.stderr, flush=True)

        if savable_humans:
            return min(savable_humans, key=lambda h: ash.distance_to(h))
        else:
            return min(self.humans, key=lambda h: ash.distance_to(h))


class Zombies:
    def __init__(self, list_of_zombies: list):
        self.zombies = [Zombie(*zombie) for zombie in list_of_zombies]

    def update_zombies(self, list_of_zombies: list) -> None:
        self.zombies = [Zombie(*zombie) for zombie in list_of_zombies]


def main():
    ash_x, ash_y = map(int, input().split())
    if "ash" not in globals():
        global ash
        ash = Ash(None, ash_x, ash_y)
    else:
        ash.update_position(ash_x, ash_y)

    humans_input = [[int(j) for j in input().split()] for _ in range(int(input()))]
    if "humans" not in globals():
        global humans
        humans = Humans(humans_input)
    else:
        humans.update_humans(humans_input)

    zombies_input = [[int(j) for j in input().split()] for _ in range(int(input()))]
    if "zombies" not in globals():
        global zombies
        zombies = Zombies(zombies_input)
    else:
        zombies.update_zombies(zombies_input)

    # Encontrar o humano mais ameaçado ou possível de salvar
    most_threatened_human = humans.find_most_threatened(zombies, ash)

    if most_threatened_human:
        print(f"Debug:{most_threatened_human=}", file=sys.stderr, flush=True)
        target_x, target_y = most_threatened_human.x + 1, most_threatened_human.y + 1
    else:
        target_x, target_y = ash.x, ash.y  # Nenhum humano está ameaçado, fique no lugar

    # Movimentar Ash em direção ao humano mais ameaçado
    ash.move_towards(target_x, target_y)

    # Imprimir o comando de movimento para Ash
    print(f"{ash.x} {ash.y}")


while True:
    main()

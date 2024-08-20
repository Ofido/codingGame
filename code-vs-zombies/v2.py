import math
import sys
from typing import Optional


class Entity:
    def __init__(self, entity_id: Optional[int], x: int, y: int):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        print(f"Debug: Created Entity ID {self.entity_id} at ({self.x}, {self.y})", file=sys.stderr, flush=True)

    def update_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        print(
            f"Debug: Updated Entity ID {self.entity_id} to new position ({self.x}, {self.y})",
            file=sys.stderr,
            flush=True,
        )

    def distance_to(self, other: "Entity") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Human(Entity):
    def __init__(self, entity_id: int, x: int, y: int):
        super().__init__(entity_id, x, y)


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
    def __init__(self, x: int, y: int):
        super().__init__(None, x, y)

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
    def __init__(self, list_of_humans: list[list[int]]):
        self.humans = [Human(*human) for human in list_of_humans]

    def update_humans(self, list_of_humans: list[list[int]]) -> None:
        self.humans = [Human(*human) for human in list_of_humans]

    def find_most_threatened(self, zombies: "Zombies") -> Optional[Human]:
        closest_human = None
        closest_distance = float("inf")

        for human in self.humans:
            for zombie in zombies.zombies:
                dist = human.distance_to(Zombie(None, *zombie.future_position()))
                if dist < closest_distance:
                    closest_distance = dist
                    closest_human = human

        return closest_human


class Zombies:
    def __init__(self, list_of_zombies: list[list[int]]):
        self.zombies = [Zombie(*zombie) for zombie in list_of_zombies]

    def update_zombies(self, list_of_zombies: list[list[int]]) -> None:
        self.zombies = [Zombie(*zombie) for zombie in list_of_zombies]


def can_save_human(human: Human, zombies: Zombies, ash: Ash) -> bool:
    min_zombie_distance = float("inf")
    for zombie in zombies.zombies:
        zombie_distance = zombie.distance_to(human)
        if zombie_distance < min_zombie_distance:
            min_zombie_distance = zombie_distance

    time_to_zombie = min_zombie_distance / 400  # 400 units per turn for zombies
    time_to_ash = ash.distance_to(human) / 1000  # 1000 units per turn for Ash

    return time_to_ash < time_to_zombie + 0.5  # Add a buffer to make saving more likely


def main():
    ash_x, ash_y = map(int, input().split())
    if "ash" not in globals():
        global ash
        ash = Ash(ash_x, ash_y)
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

    savable_humans = [human for human in humans.humans if can_save_human(human, zombies, ash)]
    print(f"Debug: savable_humans count = {len(savable_humans)}", file=sys.stderr, flush=True)

    if savable_humans:
        for human in savable_humans:
            closest_zombie_dist = min(z.distance_to(human) for z in zombies.zombies)
            print(
                f"Debug: Human {human.entity_id} - Closest Zombie Distance = {closest_zombie_dist}",
                file=sys.stderr,
                flush=True,
            )

        most_threatened_human = min(savable_humans, key=lambda h: min(z.distance_to(h) for z in zombies.zombies))
        target_x, target_y = most_threatened_human.x, most_threatened_human.y
        print(
            f"Debug: Moving towards Human {most_threatened_human.entity_id} at ({target_x}, {target_y})",
            file=sys.stderr,
            flush=True,
        )
    else:
        # New logic: move towards the human closest to Ash if no humans can be saved
        closest_human = min(humans.humans, key=lambda h: ash.distance_to(h))
        target_x, target_y = closest_human.x, closest_human.y
        print(
            "Debug: No savable humans, moving towards closest Human "
            + f"{closest_human.entity_id} at ({target_x}, {target_y})",
            file=sys.stderr,
            flush=True,
        )

    ash.move_towards(target_x, target_y)
    print(f"{ash.x} {ash.y}")


while True:
    main()

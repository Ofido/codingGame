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

    def is_moving_towards(self, target: "Entity") -> bool:
        current_distance = self.distance_to(target)
        future_distance = math.sqrt((self.next_x - target.x) ** 2 + (self.next_y - target.y) ** 2)
        return future_distance < current_distance


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

    def is_protecting(self, human: "Human", zombie: "Zombie") -> bool:
        # Verifica se Ash está entre o humano e o zumbi
        return self.distance_to(human) < human.distance_to(zombie)


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
                dist = human.distance_to(zombie)
                if dist < closest_distance:
                    closest_distance = dist
                    closest_human = human

        return closest_human

    def is_between(self, human: Human, ash: Ash, zombie: Zombie) -> bool:
        # Verifica se o ponto `b` (Ash) está entre `a` (humano) e `c` (zumbi) em uma linha reta

        # Caso especial para linhas horizontais ou verticais
        if (human.x == zombie.x and human.x == ash.x) or (human.y == zombie.y and human.y == ash.y):
            return min(human.x, zombie.x) <= ash.x <= max(human.x, zombie.x) and min(human.y, zombie.y) <= ash.y <= max(
                human.y, zombie.y
            )

        # Verificação geral para outros casos
        area = (ash.y - human.y) * (zombie.x - human.x) - (ash.x - human.x) * (zombie.y - human.y)
        if area != 0:
            return False

        return min(human.x, zombie.x) <= ash.x <= max(human.x, zombie.x) and min(human.y, zombie.y) <= ash.y <= max(
            human.y, zombie.y
        )

    def are_humans_protected(self, zombies: "Zombies", ash: Ash) -> list[Human]:
        unprotected_humans = []
        for human in self.humans:
            is_protected = False
            for zombie in zombies.zombies:
                # Verifica se Ash está entre o humano e o zumbi
                if self.is_between(human, ash, zombie) and zombie.is_moving_towards(human):
                    is_protected = True
                    break  # Se o humano está protegido, não precisa continuar verificando
            if not is_protected:
                unprotected_humans.append(human)
        return unprotected_humans


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

    # Verifica se os humanos estão protegidos
    unprotected_humans = humans.are_humans_protected(zombies, ash)
    print(f"Debug: unprotected_humans count = {len(unprotected_humans)}", file=sys.stderr, flush=True)

    if unprotected_humans:
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
    else:
        # Se todos os humanos estão protegidos, mova para a posição onde Ash pode matar mais zumbis de uma vez
        best_position = None
        max_kill_count = 0
        for zombie in zombies.zombies:
            kill_count = sum(1 for z in zombies.zombies if zombie.distance_to(z) <= 2000)
            if kill_count > max_kill_count:
                max_kill_count = kill_count
                best_position = zombie
        if best_position:
            target_x, target_y = best_position.x, best_position.y
            print(
                f"Debug: All humans are protected, moving to kill zombies at ({target_x}, {target_y})",
                file=sys.stderr,
                flush=True,
            )

    ash.move_towards(target_x, target_y)
    print(f"{ash.x} {ash.y}")


while True:
    main()

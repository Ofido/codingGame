import math


class Entity:
    def __init__(self, entity_id, x, y):
        self.entity_id = entity_id
        self.x = x
        self.y = y

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Human(Entity):
    def __init__(self, entity_id, x, y):
        super().__init__(entity_id, x, y)

    def update_position(self, x, y):
        super().__init__(x, y)


class Zombie(Entity):
    def __init__(self, entity_id, x, y, next_x, next_y):
        super().__init__(entity_id, x, y)
        self.next_x = next_x
        self.next_y = next_y

    def update_position(self, x, y, next_x, next_y):
        super().__init__(x, y)
        self.next_x = next_x
        self.next_y = next_y

    def future_position(self):
        return (self.next_x, self.next_y)


class Ash(Entity):
    def __init__(self, x, y):
        super().__init__(None, x, y)

    def update_position(self, x, y):
        super().__init__(x, y)

    def move_towards(self, target_x, target_y):
        dist = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        if dist <= 1000:
            self.x, self.y = target_x, target_y
        else:
            direction_x = (target_x - self.x) / dist
            direction_y = (target_y - self.y) / dist
            self.x += int(direction_x * 1000)
            self.y += int(direction_y * 1000)


class Humans:
    def __init__(self, list_of_humans: list):
        self.humans = [Human(*human) for human in list_of_humans]

    def update_humans(self, list_of_humans: list):
        self.humans = [Human(*human) for human in list_of_humans]

    def find_most_threatened(self, zombies):
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
    def __init__(self, list_of_zombies: list):
        self.zombies = [Zombie(*zombie) for zombie in list_of_zombies]

    def update_zombies(self, list_of_zombies: list):
        self.zombies = [Zombie(*zombie) for zombie in list_of_zombies]


def main():
    # Ler e inicializar as variáveis de Ash, humanos e zumbis apenas na primeira iteração
    ash_x, ash_y = map(int, input().split())
    if "ash" not in globals():
        global ash
        ash: Ash = Ash(ash_x, ash_y)
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

    # Encontrar o humano mais ameaçado
    most_threatened_human = humans.find_most_threatened(zombies)

    if most_threatened_human:
        target_x, target_y = most_threatened_human.x, most_threatened_human.y
    else:
        target_x, target_y = ash.x, ash.y  # Nenhum humano está ameaçado, fique no lugar

    # Movimentar Ash em direção ao humano mais ameaçado
    ash.move_towards(target_x, target_y)

    # Imprimir o comando de movimento para Ash
    print(f"{ash.x} {ash.y}")


# Este loop é usado para rodar o jogo até que ele termine
while True:
    main()

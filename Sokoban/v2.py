import sys
import heapq
from collections import deque, namedtuple

# Estado: conjunto de caixas + posição do pusher
State = namedtuple("State", ["boxes", "pusher"])

# Lê mapa estático (paredes e alvos)
width, height, box_count = map(int, sys.stdin.readline().split())
walls, targets = set(), set()
for y in range(height):
    row = sys.stdin.readline().rstrip()
    for x, ch in enumerate(row):
        if ch == '#':
            walls.add((x, y))
        elif ch == '*':
            targets.add((x, y))

# Função para verificar deadlocks
def is_deadlock(boxes):
    for box in boxes:
        # Verifica se a caixa está em um canto não alvo
        if box not in targets:
            x, y = box
            if ((x + 1, y) in walls or (x - 1, y) in walls) and \
               ((x, y + 1) in walls or (x, y - 1) in walls):
                return True
    return False

# A* otimizado com memoization
def astar_path(start, goal, walls, boxes, cache={}):
    key = (start, goal, frozenset(boxes))
    if key in cache:
        return cache[key]

    def h(p): return abs(p[0] - goal[0]) + abs(p[1] - goal[1])
    open_set = [(h(start), 0, start)]
    g_score = {start: 0}
    move_from = {}
    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            # Reconstrói o caminho
            path = []
            while current != start:
                mv = move_from[current]
                path.append(mv)
                dx, dy = {"U": (0, 1), "D": (0, -1), "L": (1, 0), "R": (-1, 0)}[mv]
                current = (current[0] + dx, current[1] + dy)
            cache[key] = list(reversed(path))
            return cache[key]
        for dx, dy, mv in [(1, 0, "R"), (-1, 0, "L"), (0, 1, "D"), (0, -1, "U")]:
            nb = (current[0] + dx, current[1] + dy)
            if nb in walls or nb in boxes or not (0 <= nb[0] < width and 0 <= nb[1] < height):
                continue
            tentative = cost + 1
            if tentative < g_score.get(nb, float("inf")):
                g_score[nb] = tentative
                move_from[nb] = mv
                heapq.heappush(open_set, (tentative + h(nb), tentative, nb))
    cache[key] = None
    return None

# Gera sucessores de push
def get_push_successors(state):
    pusher = state.pusher
    boxes = set(state.boxes)
    succs = []
    for bx, by in boxes:
        for dx, dy, push_mv in [(1, 0, "R"), (-1, 0, "L"), (0, 1, "D"), (0, -1, "U")]:
            from_cell = (bx - dx, by - dy)
            to_cell = (bx + dx, by + dy)
            if to_cell in walls or to_cell in boxes or not (0 <= to_cell[0] < width and 0 <= to_cell[1] < height):
                continue
            path = astar_path(pusher, from_cell, walls, boxes)
            if path is None:
                continue
            new_boxes = frozenset((to_cell if (x, y) == (bx, by) else (x, y)) for x, y in boxes)
            if is_deadlock(new_boxes):  # Verifica deadlock
                continue
            new_state = State(new_boxes, (bx, by))
            succs.append((new_state, path + [push_mv]))
    return succs

# BFS otimizado
def solve_sokoban(pusher_start, boxes_start):
    start = State(frozenset(boxes_start), pusher_start)
    if set(start.boxes) == targets:
        return []
    queue = deque([(start, [])])
    visited = { (start.pusher, start.boxes) }
    while queue:
        state, moves_so_far = queue.popleft()
        for succ, new_moves in get_push_successors(state):
            key = (succ.pusher, succ.boxes)
            if key in visited:
                continue
            visited.add(key)
            total_moves = moves_so_far + new_moves
            if set(succ.boxes) == targets:
                return total_moves
            queue.append((succ, total_moves))
    return None

# Loop do jogo
commands = None
cmd_idx = 0

while True:
    data = sys.stdin.readline().split()
    if not data:
        break
    pusher = (int(data[0]), int(data[1]))
    boxes = [tuple(map(int, sys.stdin.readline().split())) for _ in range(box_count)]

    if commands is None:
        commands = solve_sokoban(pusher, boxes)
        if commands is None:
            commands = []
        cmd_idx = 0

    if cmd_idx < len(commands):
        print(commands[cmd_idx], flush=True)
        cmd_idx += 1
    else:
        print("U", flush=True)

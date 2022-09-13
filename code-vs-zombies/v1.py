# https://www.youtube.com/watch?v=4uSzNfy8RMA
import sys
import math
import copy

global pontuacao_old
global movimentos_old
pontuacao_old:int = -10
movimentos_old:list = []

def fibonnacci(x):
    fib = [0,1,2,4,7,12,20,33,54,88,143,232,376,609,986,1596,2583,4180,6764,10945,17710,28656,46367,75024,121392,196417,317810,514228,832039,1346268,2178308]
    return fib[min(x, 30)]

def get_pontuacao_atual():
    global pontuacao_old
    print(f'pontuacao_old - get_pontuacao_atual', file = sys.stderr)
    print(pontuacao_old, file = sys.stderr)
    return pontuacao_old

def set_pontuacao_atual(pontuacao:int):
    global pontuacao_old
    print(f'pontuacao_old - set_pontuacao_atual', file = sys.stderr)
    print(pontuacao_old, file = sys.stderr)
    print(f'pontuacao - set_pontuacao_atual', file = sys.stderr)
    print(pontuacao, file = sys.stderr)
    pontuacao_old = pontuacao

def pop_movimentos_atual():
    global movimentos_old
    print(f'movimentos_old - pop_movimentos_atual', file = sys.stderr)
    print(movimentos_old, file = sys.stderr)
    return movimentos_old.pop(0)

def get_movimentos_atual():
    global movimentos_old
    print(f'movimentos_old - get_movimentos_atual', file = sys.stderr)
    print(movimentos_old, file = sys.stderr)
    return movimentos_old

def set_movimentos_atual(movimentos:list):
    global movimentos_old
    print(f'movimentos_old - set_movimentos_atual', file = sys.stderr)
    print(movimentos_old, file = sys.stderr)
    print(f'movimentos - set_movimentos_atual', file = sys.stderr)
    print(movimentos, file = sys.stderr)
    movimentos_old = movimentos

def movimentos_validos(posicao_atual) -> list:
    distancia = 1000
    direcoes = 16
    movimentos_validos = [posicao_atual]
    for deg in range(0, 360, 360//direcoes):
        x = math.floor(posicao_atual[0] + math.sin(math.radians(deg))*distancia)
        y = math.floor(posicao_atual[1] - math.cos(math.radians(deg))*distancia)
        if x < 0:
            x = 0
        if x > 16000:
            x = 16000
        if y < 0:
            y = 0
        if y > 9000:
            y = 9000
        movimentos_validos.append([x, y])
    return movimentos_validos

# Save humans, destroy zombies!
def melhores_movimentos(eu:list[int], humanos:list, zumbis:list, profundidade:int) -> tuple[list, int]:
    if profundidade <= 0:
        return [], 0

    possibilidades = movimentos_validos(eu)
    movimentos = []
    melhor_pontuacao = -1

    # verifica para saber a melhor jogada
    for possibilidade in possibilidades:
        agora_humanos, agora_zumbis = verifica_possibilidade(possibilidade, humanos, zumbis)
        pontuacao_possivel = calc_pontuacao_possivel(possibilidade, humanos, zumbis)
        movimentos_interno, pontuacao_interno = melhores_movimentos(possibilidade, agora_humanos, agora_zumbis, profundidade - 1)
        if (pontuacao_soma := pontuacao_possivel + pontuacao_interno) > melhor_pontuacao:
            melhor_pontuacao = pontuacao_soma
            movimentos_interno.insert(0, possibilidade)
            movimentos = movimentos_interno


    print(f'profundidade - return - melhores_movimentos', file = sys.stderr)
    print(profundidade, file = sys.stderr)
    print(f'melhor_pontuacao - return - melhores_movimentos', file = sys.stderr)
    print(melhor_pontuacao, file = sys.stderr)
    print(f'movimentos - return - melhores_movimentos', file = sys.stderr)
    print(movimentos, file = sys.stderr)

    return movimentos, melhor_pontuacao

def get_zumbis_longe(me, zumbis):
    # if not zumbis:
    #     return []
    distancia_player = 2000
    zumbis_longe = []
    for zumbi in zumbis:
        if math.dist(zumbi[3:], me) > distancia_player:
            zumbis_longe.append(zumbi)

    return zumbis_longe

def calc_pontuacao_possivel(me, humanos, zumbis):
    zumbis_perto = len(zumbis) - len(get_zumbis_longe(me, zumbis))
    score = fibonnacci(zumbis_perto) * len(humanos) * len(humanos) * 10
    return score

#idk
def getNearestHuman(zombie, humanpos, playerpos):
    playerpos = copy.deepcopy(playerpos)
    dist = float("inf")
    closest = []
    for human in humanpos:
        d = math.dist(human[1:], zombie[3:])
        if d < dist:
            closest = human
            dist = d
    d = math.dist(playerpos, zombie[3:])
    if d < dist:
        closest = playerpos
        closest.insert(0, -1)
        dist = d
    return closest

def verifica_possibilidade(me, humanos, zumbis):
    zumbis_longe = get_zumbis_longe(me, zumbis)
    novos_humanos = []

    for zombie in zumbis_longe:
        for human in humanos:
            if human[1] == zombie[1] and human[2] == zombie[2]:
                continue
            else:
                novos_humanos.append(human)

    zumbi_movimentado = []

    for zumbi in zumbis_longe:
        newpos = getNearestHuman(zumbi, novos_humanos, me)
        zumbi_movimentado.append([zumbi[0], 0, 0, newpos[0], newpos[1]])

    return novos_humanos, zumbi_movimentado

# game loop
profundidade = 80
while True:
    humanos = []
    zumbis = []
    eu = [int(i) for i in input().split()]
    human_count = int(input())
    for i in range(human_count):
        humanos.append([int(j) for j in input().split()])
    zombie_count = int(input())
    for i in range(zombie_count):
        zumbis.append([int(j) for j in input().split()])

    movimentos, pontuacao = melhores_movimentos(eu, humanos, zumbis, profundidade)
    if pontuacao > get_pontuacao_atual():
        set_pontuacao_atual(pontuacao)
        set_movimentos_atual(movimentos)

    x, y = pop_movimentos_atual()

    print(f'{x} {y}')

import sys
import math

# Pare esse jogo temos duas possiveis soluções, fazer baseado no tabuleiro onde por si só ele já escolheria uma melhor opção
# a segunda é tratar a ordenação da escolha dos melhor comando possivel referente a cada estágio.
# inicialmente vou tratar os comandos por não ter que lidar muito com a IA, e após isso melhorarei o codigo baseado no tabuleiro.


def ordenaComandos(command):
    # Percebi que simplesmente ordenar os comandos possiveis, abre a possibilidade de fazer jogadas de 3 para
    # eliminar uma peça adversária sempre, já que o comando para colocar e pegar ou mover e pegar é maior que
    # o comando de apenas mover ou apenas pegar, priorizando assim a "melhor jogada" inicial. Com isso,
    # conseguir chegar no nivel de Madeira, porem preciso chegar ao nivel de bronze para uma conquista, então preciso
    # pensar em como melhorar a ordenação para ganhar.
    # Caminhos:
    # 1 - olhar como o oponente começa e analisar isso para o proximo passo.
    # 2 - analisar se for o primeiro a jogar ou o segundo e fazer um pensamento estático somente para alcançar a proxima classificação.
    command.sort()

player_id = int(input())  # playerId (0,1)
fields = int(input())  # number of fields
neighbors = []
for i in range(fields):
    neighbors.append(input())  # neighbors of a field (ex: A1:A4;D1)

# game loop
while True:
    op_move = input()  # The last move executed from the opponent
    board = input()  # Current Board and state(0:Player0 | 1:Player1 | 2:Empty) in format field:state and separated by ;
    nbr = int(input())  # Number of valid moves proposed.
    command = []
    for i in range(nbr):
        # TODO tratar a entrada para os tipos diferentes de jogadas possiveis
        command.append(input())  # An executable command line

    ordenaComandos(command)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print("player_id", file=sys.stderr, flush=True)
    print(player_id, file=sys.stderr, flush=True)
    print(type(player_id), file=sys.stderr, flush=True)
    print("fields", file=sys.stderr, flush=True)
    print(fields, file=sys.stderr, flush=True)
    print(type(fields), file=sys.stderr, flush=True)
    print("neighbors", file=sys.stderr, flush=True)
    print(neighbors, file=sys.stderr, flush=True)
    print(type(neighbors), file=sys.stderr, flush=True)
    print("op_move", file=sys.stderr, flush=True)
    print(op_move, file=sys.stderr, flush=True)
    print(type(op_move), file=sys.stderr, flush=True)
    print("board", file=sys.stderr, flush=True)
    print(board, file=sys.stderr, flush=True)
    print(type(board), file=sys.stderr, flush=True)
    print("nbr", file=sys.stderr, flush=True)
    print(nbr, file=sys.stderr, flush=True)
    print(type(nbr), file=sys.stderr, flush=True)
    print("command", file=sys.stderr, flush=True)
    print(command, file=sys.stderr, flush=True)
    print(type(command), file=sys.stderr, flush=True)

    print(command[0])

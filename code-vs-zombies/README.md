# Jogo Code vs Zombies
https://www.codingame.com/ide/puzzle/code-vs-zombies
Optimization

## 'Rules':

## Input:

## Output:

# Solution way:
## brain way:

primeiro eu pensei em tentar fazer um objeto para cada elemento para melhor interação, mas desisti dessa ideia por ser muito complicado.
entrei no github para ver se achava algo e descobri esse código:
https://github.com/the-archer/codevszombies
parti para a implementação (sem testar) e já fazendo algumas melhorias.
Acabou não funcionando...
Partindo do zero novamente...
ai fui pesquisar no YouTube e assisti esse vídeo:

https://www.youtube.com/watch?v=4uSzNfy8RMA

que acabou me encorajando a tentar procurar uma solução sozinho!

## checklist:
- tentar colocar o código que fiz para funcionar (ps, quando um zumbi entra no range o personagem vai na direção oposta e ele fica parado)
- coletar as entradas dos humanos, removendo os ids
- coletar as entradas dos zumbis, removendo os ids
  - pensar se irei usar a direção de movimentação para prever o proximo alvo
    - (distancia vetorial entre x,y e x_next,y_next)
  - se não irei coletar pensar em qual das duas usar
- coletar os meus dados
  - 'range'
  - posição
  - vetor de movimento?
- fazer a analise de melhor movimento:
  - baseado em calculo recursivo de score (acho que é monte pascal o nome disso)
  - baseado em calculo relativo vetorial ?
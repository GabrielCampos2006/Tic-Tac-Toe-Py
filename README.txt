Como Jogar?
Para ser possível jogar o TicTacToe implementado neste github, será necessário a instalação do python e do pygame, instruções mais específicas se encontram em https://www.python.org/downloads/ e https://www.pygame.org/docs/;
Após instalado o pygame, é preciso estar em um ambiente preparado para a compilação do código python baixado, seja a IDLE base, ou outro compilador como o VSCODE com extensões criadas para tanto.

Como funciona?
Através do código apresentado, até agora, é possível escolher entre 4 opções de um jogo da velha 3x3 simples:

- A Manual: Onde duas pessoas podem jogar localmente, a cada entrada de posição do marcador é trocado automaticamente até finalizar o jogo (empate ou linha completada);

- O MinMax Básico: É criado uma árvore de busca recursiva que cria e avalia todas as ramificações, ou jogadas possíveis, e então ela sempre vai escolher a situação de valor máximo (situação em que ela ganha) de cada ramificação (+1) ao fazer sua jogada, ou empate caso seja a unica possível, e a estrutura da árvore para a sua jogada em um ramo que voce vence sempre ser a minimizadora (-1), a menor local da ramificação.
    A Condição de parada se dá ao ultimo ser maximizador (vitoria da IA), minimizador (vitoria do jogador), ou 0 onde seria uma situação de empate;
- O MinMax AlfaBeta: É criado uma árvore de busca recursiva que cria todas as ramificações, ou jogadas possíveis, mas na avaliação ele faz uma "poda" das ramificações para não precisar visitar todos, e gerar mais trabalho. Para tanto ele utiliza uma lógica em que sempre tem um pai maximizador, ele verifica as folhas do pai, em ordem da direita pra esquerda, pega o maior valor, seja +1, 0 ou -1, e verifica os filhos do pai a esquerda, se o primeiro já for maior que o da direita, ele já ignora as outras folhas e sobre o nível para os avôs, e assim sucessivamente acontece a poda.
Dessa forma a condição de parada é a mesma, o ultimo ser maximizador (vitoria da IA), minimizador (vitoria do jogador), ou 0 onde seria uma situação de empate;

Ganho de Desempenho (Poda Alfa-Beta)
Rodando o Teste Automatizado de 100 partidas para cada algoritmo, extraímos os seguintes dados de esforço computacional (nós da árvore visitados):
*Minimax Básico: 6.220.380 nós avaliados (Média de 62.203 por partida).
*Minimax Alfa-Beta: 397.504 nós avaliados (Média de 3.975 por partida).
*Teste Automatizado (Comprovação de Robustez):Uma rotina que executa o agente contra 100 partidas de jogadas aleatórias para atestar sua invencibilidade.
*Conclusão:A implementação da Poda Alfa-Beta resultou em uma redução massiva de 5.822.876 nós processados ao longo de 100 jogos. O agente manteve sua robustez absoluta (0 derrotas em ambos os testes), provando a eficiência da otimização.
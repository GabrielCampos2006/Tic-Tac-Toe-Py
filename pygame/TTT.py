import pygame
import sys
import random


def Vitoria(campo):
    vencedor = None

    #verifica se tem vitória de forma horizontal
    for linha in range(0, 3):
        if((campo[linha][0] == campo[linha][1] == campo[linha][2]) and (campo[linha][0] is not None)):
            vencedor = campo[linha][0]

            #caso tiver um linha horizontal, vai colocar a imagem vencedora
            for i in range(0, 3):
                campo_grafico[linha][i][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
                tela.blit(campo_grafico[linha][i][0], campo_grafico[linha][i][1])

            pygame.display.update()

            return vencedor

    #verifica se tem vitoria vertical
    for coluna in range(0, 3):
        if((campo[0][coluna] == campo[1][coluna] == campo[2][coluna]) and (campo[0][coluna] is not None)):
            vencedor = campo[0][coluna]

            for j in range(0, 3):
                campo_grafico[j][coluna][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
                tela.blit(campo_grafico[j][coluna][0], campo_grafico[j][coluna][1])

            pygame.display.update()

            return vencedor

    #verifica se tem vitoria na diagonal principal
    if (campo[0][0] == campo[1][1] == campo[2][2]) and (campo[0][0] is not None):
        vencedor =  campo[0][0]

        campo_grafico[0][0][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
        tela.blit(campo_grafico[0][0][0], campo_grafico[0][0][1])

        campo_grafico[1][1][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
        tela.blit(campo_grafico[1][1][0], campo_grafico[1][1][1])

        campo_grafico[2][2][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
        tela.blit(campo_grafico[2][2][0], campo_grafico[2][2][1])
        pygame.display.update()

        return vencedor

    #verifica se tem vitória na diagonal secundária
    if (campo[0][2] == campo[1][1] == campo[2][0]) and (campo[0][2] is not None):
        vencedor =  campo[0][2]

        campo_grafico[0][2][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
        tela.blit(campo_grafico[0][2][0], campo_grafico[0][2][1])

        campo_grafico[1][1][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
        tela.blit(campo_grafico[1][1][0], campo_grafico[1][1][1])

        campo_grafico[2][0][0] = pygame.image.load(f"pygame/assets/Ganha_{vencedor}.png")
        tela.blit(campo_grafico[2][0][0], campo_grafico[2][0][1])

        pygame.display.update()

        return vencedor

    #verifica se não vitoria, causando em empate
    if vencedor is None:
        for i in range(len(campo)):
            for j in range(len(campo)):
                if campo[i][j] is None:
                    return None
        return "EMPATE"


def Campo_Renderizado(campo, img_x, img_o):
    global campo_grafico

    for i in range(3):
        for j in range(3):

            #está implementado a imagem no jogo
            if campo[i][j] == "X":
                campo_grafico[i][j][0] = img_x
                campo_grafico[i][j][1] = img_x.get_rect(center=(j * 300 + 150, i * 300 + 150))
            elif campo[i][j] == "O":
                campo_grafico[i][j][0] = img_o
                campo_grafico[i][j][1] = img_o.get_rect(center=(j * 300 + 150, i * 300 + 150))


def X_ou_O(campo, campo_grafico, mover):
    #comando que retorna a posição atual do mouse
    posicao_atual = pygame.mouse.get_pos()
    #Divisão inteira  por 300 pixels resolve o clique exato
    coluna = posicao_atual[0] // 300
    linha = posicao_atual[1] // 300

    #evita erro de índice caso o clique seja na linha de borda final
    if coluna == 3: coluna = 2
    if linha == 3: linha = 2

    #verifica se o campo está vazio
    if campo[linha][coluna] is None:
        campo[linha][coluna] = mover

        if mover == "O":
            mover = "X"
        else:
            mover = "O"

    Campo_Renderizado(campo, IMG_X, IMG_O)

    for a in range(3):
        for b in range(3):
            if campo_grafico[a][b][0] is not None:
                tela.blit(campo_grafico[a][b][0], campo_grafico[a][b][1])

    return campo, mover

# --- INÍCIO DO MINIMAX BASICO ---

nos_avaliados_basico = 0

def avaliar_estado_silencioso(tabuleiro):
    # Verifica linhas e colunas
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] and tabuleiro[i][0] is not None:
            return tabuleiro[i][0]
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] and tabuleiro[0][i] is not None:
            return tabuleiro[0][i]
            
    # Verifica diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] is not None:
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] is not None:
        return tabuleiro[0][2]
        
    # Verifica empate
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] is None:
                return None # O jogo ainda não acabou
    return "EMPATE"

def algoritmo_minimax_basico(tabuleiro, maximizando):
    global nos_avaliados_basico
    nos_avaliados_basico += 1
    
    resultado = avaliar_estado_silencioso(tabuleiro)
    
    if resultado == "O": return 1  # IA ganha
    if resultado == "X": return -1 # Pessoa ganha
    if resultado == "EMPATE": return 0
    
    if maximizando:
        melhor_valor = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "O" # Simula a jogada da IA
                    valor = algoritmo_minimax_basico(tabuleiro, False)
                    tabuleiro[i][j] = None # Desfaz a jogada
                    melhor_valor = max(melhor_valor, valor)
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "X" # Simula a jogada do Pessoa
                    valor = algoritmo_minimax_basico(tabuleiro, True)
                    tabuleiro[i][j] = None # Desfaz a jogada
                    melhor_valor = min(melhor_valor, valor)
        return melhor_valor

def obter_melhor_jogada_basico(tabuleiro):
    global nos_avaliados_basico
    nos_avaliados_basico = 0
    melhor_valor = -float('inf')
    melhor_movimento = None
    
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] is None:
                tabuleiro[i][j] = "O"
                valor = algoritmo_minimax_basico(tabuleiro, False)
                tabuleiro[i][j] = None
                
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_movimento = (i, j)
                    
    return melhor_movimento, nos_avaliados_basico
# --- INICIO DO MINIMAX ALFABETA ---
nos_avaliados_poda = 0

def algoritmo_minimax_alfa_beta(tabuleiro, maximizando, alfa, beta):
    global nos_avaliados_poda
    nos_avaliados_poda += 1
    
    resultado = avaliar_estado_silencioso(tabuleiro)
    
    if resultado == "O": return 1  # IA ganha
    if resultado == "X": return -1 # Pessoa ganha
    if resultado == "EMPATE": return 0
    
    if maximizando:
        melhor_valor = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "O" # Simula a jogada da IA
                    valor = algoritmo_minimax_alfa_beta(tabuleiro, False, alfa, beta)
                    tabuleiro[i][j] = None # Desfaz a jogada
                    
                    melhor_valor = max(melhor_valor, valor)
                    alfa = max(alfa, melhor_valor)
                    
                    # Poda: Se o adversário já tem uma jogada melhor garantida, ignora o resto
                    if beta <= alfa:
                        return melhor_valor 
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "X" # Simula a jogada do Pessoa
                    valor = algoritmo_minimax_alfa_beta(tabuleiro, True, alfa, beta)
                    tabuleiro[i][j] = None # Desfaz a jogada
                    
                    melhor_valor = min(melhor_valor, valor)
                    beta = min(beta, melhor_valor)
                    
                    # Poda: Se a IA já achou uma jogada melhor antes, corta este caminho
                    if beta <= alfa:
                        return melhor_valor
        return melhor_valor

def obter_melhor_jogada_alfa_beta(tabuleiro):
    global nos_avaliados_poda
    nos_avaliados_poda = 0
    melhor_valor = -float('inf')
    melhor_movimento = None
    alfa = -float('inf')
    beta = float('inf')
    
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] is None:
                tabuleiro[i][j] = "O"
                valor = algoritmo_minimax_alfa_beta(tabuleiro, False, alfa, beta)
                tabuleiro[i][j] = None
                
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_movimento = (i, j)
                
                alfa = max(alfa, melhor_valor)
                    
    return melhor_movimento, nos_avaliados_poda

def obter_movimento_aleatorio(tabuleiro):
    movimentos_disponiveis = []

    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] is None:
                movimentos_disponiveis.append((i, j))

    if movimentos_disponiveis:
        return random.choice(movimentos_disponiveis)

    return None

def jogar_partida_automatizada(algoritmo):
    tabuleiro = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    jogador_atual = "X"
    total_nos = 0

    while True:
        if jogador_atual == "X":
            movimento = obter_movimento_aleatorio(tabuleiro)

            if movimento is not None:
                linha, coluna = movimento
                tabuleiro[linha][coluna] = "X"
        else:
            if algoritmo == "MINIMAX":
                movimento, nos = obter_melhor_jogada_basico(tabuleiro)
            else:
                movimento, nos = obter_melhor_jogada_alfa_beta(tabuleiro)

            total_nos += nos

            if movimento is not None:
                linha, coluna = movimento
                tabuleiro[linha][coluna] = "O"
        
        resultado = avaliar_estado_silencioso(tabuleiro)

        if resultado is not None:
            return resultado, total_nos

        if jogador_atual == "X":
            jogador_atual = "O"
        else:
            jogador_atual = "X"


def executar_teste(algoritmo, quantidade_partidas=100):
    vitorias_ia = 0
    derrotas_ia = 0
    empates = 0
    total_nos = 0

    for partida in range(quantidade_partidas):
        resultado, nos = jogar_partida_automatizada(algoritmo)

        total_nos += nos

        if resultado == "O":
            vitorias_ia += 1
        elif resultado == "X":
            derrotas_ia += 1
        elif resultado == "EMPATE":
            empates += 1

    media_nos = total_nos / quantidade_partidas

    return {
        "algoritmo": algoritmo,
        "partidas": quantidade_partidas,
        "vitorias_ia": vitorias_ia,
        "derrotas_ia": derrotas_ia,
        "empates": empates,
        "total_nos": total_nos,
        "media_nos": media_nos
    }


def jogar_manual():
    global campo, campo_grafico
    #as grid do jogo da velha
    campo = [[None, None, None], [None, None, None], [None, None, None]]
    campo_grafico = [[[None, None], [None, None], [None, None]], 
                        [[None, None], [None, None], [None, None]], 
                        [[None, None], [None, None], [None, None]]]
    jogo_finalizado = False

    #está implemetando a cor no jogo e desenhando os formatos do jogo
    tela.fill(cor_da_tela)
    tela.blit(VELHA, (64, 64))

    #atualizando o jogo para implementar as mudanças
    pygame.display.update()

    mover = "X"
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #quando clicar no jogo aparece ou o X ou o O
            if evento.type == pygame.MOUSEBUTTONDOWN:
                #código para quando for reiniciar o jogo
                if jogo_finalizado:
                    campo = [[None, None, None], [None, None, None], [None, None, None]]
                    campo_grafico = [[[None, None], [None, None], [None, None]], 
                                        [[None, None], [None, None], [None, None]], 
                                        [[None, None], [None, None], [None, None]]]

                    mover = "X"

                    tela.fill(cor_da_tela)
                    tela.blit(VELHA, (64, 64))

                    jogo_finalizado = False

                    pygame.display.update()
                else:
                    campo, mover = X_ou_O(campo, campo_grafico, mover)

                    if Vitoria(campo) is not None:
                        jogo_finalizado = True

                pygame.display.update()



def jogar_minimax_basico():
    global campo, campo_grafico
    
    # Prepara o jogo
    campo = [[None, None, None], [None, None, None], [None, None, None]]
    campo_grafico = [[[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]]]
    jogo_finalizado = False
    mover = "X" # Pessoa começa

    tela.fill(cor_da_tela)
    tela.blit(VELHA, (64, 64))
    pygame.display.update()

    while True:
        # --- TURNO DA IA (O) ---
        if mover == "O" and not jogo_finalizado:
            print("IA (Minimax Básico) pensando...")
            
            movimento, nos = obter_melhor_jogada_basico(campo)
            
            if movimento is not None:
                linha, coluna = movimento
                print(f"Nós avaliados nesta jogada: {nos}")
                
                campo[linha][coluna] = "O"
                mover = "X"
                
                # Atualiza a tela com a jogada da IA
                Campo_Renderizado(campo, IMG_X, IMG_O)
                for a in range(3):
                    for b in range(3):
                        if campo_grafico[a][b][0] is not None:
                            tela.blit(campo_grafico[a][b][0], campo_grafico[a][b][1])
                
                # Usa a função Vitoria original para desenhar a linha vermelha se a IA ganhar
                if Vitoria(campo) is not None:
                    jogo_finalizado = True
                    
                pygame.display.update()

        # --- EVENTOS DA JANELA E TURNO Da Pessoa (X) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if jogo_finalizado:
                    # Reinicia
                    campo = [[None, None, None], [None, None, None], [None, None, None]]
                    campo_grafico = [[[None, None], [None, None], [None, None]], 
                                     [[None, None], [None, None], [None, None]], 
                                     [[None, None], [None, None], [None, None]]]
                    mover = "X"
                    tela.fill(cor_da_tela)
                    tela.blit(VELHA, (64, 64))
                    jogo_finalizado = False
                    pygame.display.update()
                
                elif mover == "X":
                    # Pessoa joga
                    campo, mover = X_ou_O(campo, campo_grafico, mover)
                    if Vitoria(campo) is not None:
                        jogo_finalizado = True
                
                pygame.display.update()
def jogar_minimax_poda():
    global campo, campo_grafico
    
    # Prepara o jogo
    campo = [[None, None, None], [None, None, None], [None, None, None]]
    campo_grafico = [[[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]]]
    jogo_finalizado = False
    mover = "X" # Pessoa começa

    tela.fill(cor_da_tela)
    tela.blit(VELHA, (64, 64))
    pygame.display.update()

    while True:
        # --- TURNO DA IA COM PODA ALFA-BETA ---
        if mover == "O" and not jogo_finalizado:
            print("IA (Alfa-Beta) pensando...")
            
            movimento, nos = obter_melhor_jogada_alfa_beta(campo)
            
            if movimento is not None:
                linha, coluna = movimento
                print(f"Nós avaliados nesta jogada (COM PODA): {nos}")
                
                campo[linha][coluna] = "O"
                mover = "X"
                
                Campo_Renderizado(campo, IMG_X, IMG_O)
                for a in range(3):
                    for b in range(3):
                        if campo_grafico[a][b][0] is not None:
                            tela.blit(campo_grafico[a][b][0], campo_grafico[a][b][1])
                
                if Vitoria(campo) is not None:
                    jogo_finalizado = True
                    
                pygame.display.update()

        # --- EVENTOS DA JANELA E TURNO Da Pessoa ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if jogo_finalizado:
                    campo = [[None, None, None], [None, None, None], [None, None, None]]
                    campo_grafico = [[[None, None], [None, None], [None, None]], 
                                     [[None, None], [None, None], [None, None]], 
                                     [[None, None], [None, None], [None, None]]]
                    mover = "X"
                    tela.fill(cor_da_tela)
                    tela.blit(VELHA, (64, 64))
                    jogo_finalizado = False
                    pygame.display.update()
                
                elif mover == "X":
                    campo, mover = X_ou_O(campo, campo_grafico, mover)
                    if Vitoria(campo) is not None:
                        jogo_finalizado = True
                
                pygame.display.update()

def teste_automatizado():
    print("\n" + "=" * 60)
    print("TESTE AUTOMATIZADO - MINIMAX")
    print("=" * 60)

    resultado_minimax = executar_teste("MINIMAX", 100)

    print(f"Partidas: {resultado_minimax['partidas']}")
    print(f"Vitórias da IA: {resultado_minimax['vitorias_ia']}")
    print(f"Derrotas da IA: {resultado_minimax['derrotas_ia']}")
    print(f"Empates: {resultado_minimax['empates']}")
    print(f"Total de nós avaliados: {resultado_minimax['total_nos']}")
    print(f"Média de nós por partida: {resultado_minimax['media_nos']:.2f}")

    print("\n" + "=" * 60)
    print("TESTE AUTOMATIZADO - ALPHA-BETA")
    print("=" * 60)

    resultado_alfa_beta = executar_teste("ALFA_BETA", 100)

    print(f"Partidas: {resultado_alfa_beta['partidas']}")
    print(f"Vitórias da IA: {resultado_alfa_beta['vitorias_ia']}")
    print(f"Derrotas da IA: {resultado_alfa_beta['derrotas_ia']}")
    print(f"Empates: {resultado_alfa_beta['empates']}")
    print(f"Total de nós avaliados: {resultado_alfa_beta['total_nos']}")
    print(f"Média de nós por partida: {resultado_alfa_beta['media_nos']:.2f}")

    print("\n" + "=" * 60)
    print("COMPARAÇÃO")
    print("=" * 60)

    diferenca = (
        resultado_minimax["total_nos"]
        - resultado_alfa_beta["total_nos"]
    )

    print(f"Minimax: {resultado_minimax['total_nos']} nós")
    print(f"Alpha-Beta: {resultado_alfa_beta['total_nos']} nós")
    print(f"Redução com Alpha-Beta: {diferenca} nós")

def _normalizar_tabuleiro(tabuleiro):
    return [[v if v in ("X", "O") else None for v in linha] for linha in tabuleiro]

def _trocar_simbolos(tabuleiro):
    troca = {"X": "O", "O": "X"}
    return [[troca.get(v, v) for v in linha] for linha in tabuleiro]

def obter_jogada_ia(tabuleiro, simbolo_ia, usar_poda=True):
    tabuleiro_calculo = _normalizar_tabuleiro(tabuleiro)
    if simbolo_ia != "O":
        tabuleiro_calculo = _trocar_simbolos(tabuleiro_calculo)
    if usar_poda:
        return obter_melhor_jogada_alfa_beta(tabuleiro_calculo)
    return obter_melhor_jogada_basico(tabuleiro_calculo)

if __name__ == "__main__":
    #comando para iniciar o jogo
    pygame.init()

    largura, altura = 900, 900

    #Codigos Básicos
    #tamanho do nosso jogo
    tela = pygame.display.set_mode((largura, altura))

    #nome do jogo
    pygame.display.set_caption("Jogo da Velha")

    #as imagens
    VELHA = pygame.image.load('assets/Board.png')
    IMG_X = pygame.image.load('assets/X.png')
    IMG_O = pygame.image.load('assets/O.png')

    #cor, por formato RGB
    cor_da_tela = (214, 201, 227)

    #as grid do jogo da velha
    campo = [[None, None, None], [None, None, None], [None, None, None]]
    campo_grafico = [[[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]]]
    print("-" * 50)
    print(" ESCOLHA O MODO DE JOGO ")
    print("-" * 50)
    print("1. Jogo Manual (2 Jogadores)")
    print("2. Teste Automatizado (100 partidas)")
    print("3. Jogar contra Minimax Básico")
    print("4. Jogar contra Minimax Poda Alfa-Beta")
    print("-" * 50)

    escolha = input("Digite o número da opção desejada no terminal: ")

    if escolha == '1':
        print("Abra a janela do Pygame para jogar!")
        jogar_manual()
    elif escolha == '2':
        teste_automatizado()
    elif escolha == '3':
        print("Abra a janela do Pygame para jogar!")
        jogar_minimax_basico()
    elif escolha == '4':
        print("Abra a janela do Pygame para jogar!")
        jogar_minimax_poda()
    else:
        print("Opção inválida. Encerrando...")
        pygame.quit()
        sys.exit()
import pygame
import sys
import random
import io
import contextlib
import os

PASTA_DO_JOGO = os.path.dirname(os.path.abspath(__file__))

def caminho_asset(nome_arquivo):
    return os.path.join(PASTA_DO_JOGO, "assets", nome_arquivo)

# --- INÍCIO DA LÓGICA DE IA (MINIMAX E PODA ALFA-BETA) ---
nos_avaliados_basico = 0
nos_avaliados_poda = 0

def avaliar_estado_silencioso(tabuleiro):
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] and tabuleiro[i][0] is not None:
            return tabuleiro[i][0]
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] and tabuleiro[0][i] is not None:
            return tabuleiro[0][i]
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] is not None:
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] is not None:
        return tabuleiro[0][2]
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] is None:
                return None 
    return "EMPATE"

def algoritmo_minimax_basico(tabuleiro, maximizando):
    global nos_avaliados_basico
    nos_avaliados_basico += 1
    
    resultado = avaliar_estado_silencioso(tabuleiro)
    if resultado == "O": return 1  
    if resultado == "X": return -1 
    if resultado == "EMPATE": return 0
    
    if maximizando:
        melhor_valor = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "O" 
                    valor = algoritmo_minimax_basico(tabuleiro, False)
                    tabuleiro[i][j] = None 
                    melhor_valor = max(melhor_valor, valor)
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "X" 
                    valor = algoritmo_minimax_basico(tabuleiro, True)
                    tabuleiro[i][j] = None 
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

def algoritmo_minimax_alfa_beta(tabuleiro, maximizando, alfa, beta):
    global nos_avaliados_poda
    nos_avaliados_poda += 1
    
    resultado = avaliar_estado_silencioso(tabuleiro)
    if resultado == "O": return 1  
    if resultado == "X": return -1 
    if resultado == "EMPATE": return 0
    
    if maximizando:
        melhor_valor = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "O" 
                    valor = algoritmo_minimax_alfa_beta(tabuleiro, False, alfa, beta)
                    tabuleiro[i][j] = None 
                    melhor_valor = max(melhor_valor, valor)
                    alfa = max(alfa, melhor_valor)
                    if beta <= alfa:
                        return melhor_valor 
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] is None:
                    tabuleiro[i][j] = "X" 
                    valor = algoritmo_minimax_alfa_beta(tabuleiro, True, alfa, beta)
                    tabuleiro[i][j] = None 
                    melhor_valor = min(melhor_valor, valor)
                    beta = min(beta, melhor_valor)
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
    movimentos_disponiveis = [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] is None]
    return random.choice(movimentos_disponiveis) if movimentos_disponiveis else None

def jogar_partida_automatizada(algoritmo):
    tabuleiro = [[None, None, None], [None, None, None], [None, None, None]]
    jogador_atual = "X"
    total_nos = 0
    while True:
        if jogador_atual == "X":
            movimento = obter_movimento_aleatorio(tabuleiro)
            if movimento: tabuleiro[movimento[0]][movimento[1]] = "X"
        else:
            if algoritmo == "MINIMAX":
                movimento, nos = obter_melhor_jogada_basico(tabuleiro)
            else:
                movimento, nos = obter_melhor_jogada_alfa_beta(tabuleiro)
            total_nos += nos
            if movimento: tabuleiro[movimento[0]][movimento[1]] = "O"
        
        resultado = avaliar_estado_silencioso(tabuleiro)
        if resultado is not None:
            return resultado, total_nos
        jogador_atual = "O" if jogador_atual == "X" else "X"

def executar_teste(algoritmo, quantidade_partidas=100):
    vitorias_ia = derrotas_ia = empates = total_nos = 0
    for _ in range(quantidade_partidas):
        resultado, nos = jogar_partida_automatizada(algoritmo)
        total_nos += nos
        if resultado == "O": vitorias_ia += 1
        elif resultado == "X": derrotas_ia += 1
        elif resultado == "EMPATE": empates += 1
    return {
        "partidas": quantidade_partidas,
        "vitorias_ia": vitorias_ia, "derrotas_ia": derrotas_ia, "empates": empates,
        "total_nos": total_nos, "media_nos": total_nos / quantidade_partidas
    }

def teste_automatizado():
    print("\n" + "=" * 60 + "\nTESTE AUTOMATIZADO - MINIMAX\n" + "=" * 60)
    res_mini = executar_teste("MINIMAX", 100)
    print(f"Partidas: {res_mini['partidas']}\nVitórias da IA: {res_mini['vitorias_ia']}\nDerrotas da IA: {res_mini['derrotas_ia']}\nEmpates: {res_mini['empates']}\nTotal de nós: {res_mini['total_nos']}\nMédia por partida: {res_mini['media_nos']:.2f}")

    print("\n" + "=" * 60 + "\nTESTE AUTOMATIZADO - ALPHA-BETA\n" + "=" * 60)
    res_ab = executar_teste("ALFA_BETA", 100)
    print(f"Partidas: {res_ab['partidas']}\nVitórias da IA: {res_ab['vitorias_ia']}\nDerrotas da IA: {res_ab['derrotas_ia']}\nEmpates: {res_ab['empates']}\nTotal de nós: {res_ab['total_nos']}\nMédia por partida: {res_ab['media_nos']:.2f}")

    print("\n" + "=" * 60 + "\nCOMPARAÇÃO\n" + "=" * 60)
    print(f"Minimax: {res_mini['total_nos']} nós\nAlpha-Beta: {res_ab['total_nos']} nós\nRedução com Alpha-Beta: {res_mini['total_nos'] - res_ab['total_nos']} nós")

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

# --- INÍCIO DO PYGAME E INTERFACE ---
pygame.init()
largura, altura = 900, 900
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Velha")

VELHA = pygame.image.load(caminho_asset('Board.png'))
IMG_X = pygame.image.load(caminho_asset('X.png'))
IMG_O = pygame.image.load(caminho_asset('O.png'))

cor_da_tela = (214, 201, 227)
campo = [[None, None, None], [None, None, None], [None, None, None]]
campo_grafico = [[[None, None], [None, None], [None, None]], 
                 [[None, None], [None, None], [None, None]], 
                 [[None, None], [None, None], [None, None]]]
mover = "X"

def desenhar_linha_vencedora(pos_inicial, pos_final):
    pygame.draw.line(tela, (220, 20, 60), pos_inicial, pos_final, 15)
    pygame.display.update()

def Vitoria(campo):
    for linha in range(3):
        if (campo[linha][0] == campo[linha][1] == campo[linha][2]) and (campo[linha][0] is not None):
            desenhar_linha_vencedora((50, 150 + linha * 300), (850, 150 + linha * 300))
            return campo[linha][0]
    for coluna in range(3):
        if (campo[0][coluna] == campo[1][coluna] == campo[2][coluna]) and (campo[0][coluna] is not None):
            desenhar_linha_vencedora((150 + coluna * 300, 50), (150 + coluna * 300, 850))
            return campo[0][coluna]
    if (campo[0][0] == campo[1][1] == campo[2][2]) and (campo[0][0] is not None):
        desenhar_linha_vencedora((50, 50), (850, 850))
        return campo[0][0]
    if (campo[0][2] == campo[1][1] == campo[2][0]) and (campo[0][2] is not None):
        desenhar_linha_vencedora((850, 50), (50, 850))
        return campo[0][2]
    
    for i in range(3):
        for j in range(3):
            if campo[i][j] is None:
                return None
    return "EMPATE"

def Campo_Renderizado(campo, img_x, img_o):
    for i in range(3):
        for j in range(3):
            if campo[i][j] == "X":
                campo_grafico[i][j][0] = img_x
                campo_grafico[i][j][1] = img_x.get_rect(center=(j * 300 + 150, i * 300 + 150))
            elif campo[i][j] == "O":
                campo_grafico[i][j][0] = img_o
                campo_grafico[i][j][1] = img_o.get_rect(center=(j * 300 + 150, i * 300 + 150))

def X_ou_O(campo, campo_grafico, mover):
    pos = pygame.mouse.get_pos()
    coluna, linha = pos[0] // 300, pos[1] // 300
    if coluna == 3: coluna = 2
    if linha == 3: linha = 2

    if campo[linha][coluna] is None:
        campo[linha][coluna] = mover
        mover = "O" if mover == "X" else "X"

    Campo_Renderizado(campo, IMG_X, IMG_O)
    for a in range(3):
        for b in range(3):
            if campo_grafico[a][b][0] is not None:
                tela.blit(campo_grafico[a][b][0], campo_grafico[a][b][1])
    return campo, mover

fonte_titulo = pygame.font.SysFont(None, 60)
fonte_botoes = pygame.font.SysFont(None, 40)

estado_atual = "MENU"
modo_de_jogo = None   
resultado_texto = ""  
simbolo_jogador = "X" 
teste_logs = None

def desenhar_botao(texto, x, y, largura, altura, cor_normal, cor_hover):
    mouse_pos = pygame.mouse.get_pos()
    retangulo = pygame.Rect(x, y, largura, altura)
    cor_atual = cor_hover if retangulo.collidepoint(mouse_pos) else cor_normal
    pygame.draw.rect(tela, cor_atual, retangulo, border_radius=10)
    
    texto_render = fonte_botoes.render(texto, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=retangulo.center)
    tela.blit(texto_render, texto_rect)
    return retangulo

def resetar_jogo():
    global campo, campo_grafico, mover
    campo = [[None, None, None], [None, None, None], [None, None, None]]
    campo_grafico = [[[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]]]
    mover = "X"
    tela.fill(cor_da_tela)
    tela.blit(VELHA, (64, 64))
    pygame.display.update()

# --- LOOP PRINCIPAL DO JOGO ---
while True:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    if estado_atual == "MENU":
        tela.fill((40, 44, 52))
        titulo = fonte_titulo.render("JOGO DA VELHA - MINIMAX", True, (255, 255, 255))
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 120))
        
        b1 = desenhar_botao("Jogar Manualmente", 250, 300, 400, 60, (70, 130, 180), (100, 149, 237))
        b2 = desenhar_botao("Contra Minimax Básico", 250, 400, 400, 60, (70, 130, 180), (100, 149, 237))
        b3 = desenhar_botao("Contra Minimax Alfa-Beta", 250, 500, 400, 60, (70, 130, 180), (100, 149, 237))
        b4 = desenhar_botao("Teste Automatizado", 250, 600, 400, 60, (220, 20, 60), (255, 99, 71))
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if b1.collidepoint(pos):
                    modo_de_jogo = "MANUAL"
                    estado_atual = "ESCOLHER_SIMBOLO"
                elif b2.collidepoint(pos):
                    modo_de_jogo = "MINIMAX"
                    estado_atual = "ESCOLHER_SIMBOLO"
                elif b3.collidepoint(pos):
                    modo_de_jogo = "ALFA_BETA"
                    estado_atual = "ESCOLHER_SIMBOLO"
                elif b4.collidepoint(pos):
                    estado_atual = "TESTE"
                    teste_logs = None

    elif estado_atual == "ESCOLHER_SIMBOLO":
        tela.fill((40, 44, 52))
        titulo_simbolo = fonte_titulo.render("ESCOLHA SEU SÍMBOLO", True, (255, 255, 255))
        tela.blit(titulo_simbolo, (largura//2 - titulo_simbolo.get_width()//2, 200))
        
        b_x = desenhar_botao("Jogar com X (Você começa)", 175, 350, 550, 60, (70, 130, 180), (100, 149, 237))
        b_o = desenhar_botao("Jogar com O (IA começa como X)", 175, 450, 550, 60, (70, 130, 180), (100, 149, 237))
        bt_voltar_escolha = desenhar_botao("Voltar", 350, 600, 200, 50, (178, 34, 34), (220, 20, 60))
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if b_x.collidepoint(pos):
                    simbolo_jogador = "X"
                    estado_atual = "JOGANDO"
                    resetar_jogo()
                elif b_o.collidepoint(pos):
                    simbolo_jogador = "O"
                    estado_atual = "JOGANDO"
                    resetar_jogo()
                elif bt_voltar_escolha.collidepoint(pos):
                    estado_atual = "MENU"
                    
    elif estado_atual == "JOGANDO":
        if mover == simbolo_jogador or modo_de_jogo == "MANUAL":
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    campo, mover = X_ou_O(campo, campo_grafico, mover)
                    vencedor_atual = Vitoria(campo)
                    if vencedor_atual is not None:
                        pygame.time.delay(400) 
                        if vencedor_atual == "EMPATE":
                            resultado_texto = "Empate!"
                        elif modo_de_jogo == "MANUAL":
                            resultado_texto = f"Jogador {vencedor_atual} ganhou!"
                        elif vencedor_atual == simbolo_jogador:
                            resultado_texto = "Você ganhou!"
                        else:
                            resultado_texto = "A IA ganhou!"
                        estado_atual = "FIM_DE_JOGO"
    
        if estado_atual == "JOGANDO" and mover != simbolo_jogador and modo_de_jogo != "MANUAL":
            simbolo_ia = "O" if simbolo_jogador == "X" else "X"
            usar_poda = (modo_de_jogo == "ALFA_BETA")
            (i, j), nos = obter_jogada_ia(campo, simbolo_ia, usar_poda)

            campo[i][j] = simbolo_ia
            mover = simbolo_jogador

            Campo_Renderizado(campo, IMG_X, IMG_O)
            for a in range(3):
                for b in range(3):
                    if campo_grafico[a][b][0] is not None:
                        tela.blit(campo_grafico[a][b][0], campo_grafico[a][b][1])

            pygame.display.update()
            vencedor_atual = Vitoria(campo)
            
            if vencedor_atual is not None:
                pygame.time.delay(400)
                if vencedor_atual == "EMPATE":
                    resultado_texto = "Empate!"
                elif vencedor_atual == simbolo_jogador:
                    resultado_texto = "Você ganhou!"
                else:
                    resultado_texto = "A IA ganhou!"
                estado_atual = "FIM_DE_JOGO"
       
    elif estado_atual == "FIM_DE_JOGO":
        pygame.draw.rect(tela, (50, 50, 50), (250, 300, 400, 300), border_radius=15)
        pygame.draw.rect(tela, (255, 255, 255), (250, 300, 400, 300), width=3, border_radius=15)
        
        texto_res = fonte_titulo.render(resultado_texto, True, (255, 215, 0))
        tela.blit(texto_res, (largura//2 - texto_res.get_width()//2, 330))
        
        bt_tentar = desenhar_botao("Tentar Novamente", 300, 420, 300, 50, (34, 139, 34), (50, 205, 50))
        bt_voltar = desenhar_botao("Voltar ao Menu", 300, 500, 300, 50, (178, 34, 34), (220, 20, 60))
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if bt_tentar.collidepoint(pos):
                    estado_atual = "JOGANDO"
                    resetar_jogo()
                elif bt_voltar.collidepoint(pos):
                    estado_atual = "MENU"

    elif estado_atual == "TESTE":
        tela.fill((30, 30, 30))
        titulo_logs = fonte_titulo.render("Teste Automatizado", True, (255, 255, 255))
        tela.blit(titulo_logs, (largura//2 - titulo_logs.get_width()//2, 30))

        if teste_logs is None:
            pygame.display.update()
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                teste_automatizado()
            linhas_brutas = buffer.getvalue().splitlines()
            teste_logs = [l for l in linhas_brutas if l.strip() and set(l.strip()) != {"="}]

        fonte_logs = pygame.font.SysFont(None, 28)
        y = 100
        for linha in teste_logs:
            tela.blit(fonte_logs.render(linha, True, (220, 220, 220)), (50, y))
            y += 30

        bt_rodar_de_novo = desenhar_botao("Rodar Teste Novamente", 275, 700, 350, 50, (34, 139, 34), (50, 205, 50))
        bt_voltar_teste = desenhar_botao("Voltar ao Menu", 300, 770, 300, 50, (178, 34, 34), (220, 20, 60))

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if bt_rodar_de_novo.collidepoint(pos):
                    teste_logs = None
                elif bt_voltar_teste.collidepoint(pos):
                    estado_atual = "MENU"
                    
    pygame.display.update()
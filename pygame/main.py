import pygame
import sys
import io
import contextlib
from TTT import obter_jogada_ia, teste_automatizado

import os

PASTA_DO_JOGO = os.path.dirname(os.path.abspath(__file__))

def caminho_asset(nome_arquivo):
    return os.path.join(PASTA_DO_JOGO, "assets", nome_arquivo)

#comando para iniciar o jogo
pygame.init()

largura, altura = 900, 900

#tamanho do nosso jogo
tela = pygame.display.set_mode((largura, altura))

#nome do jogo
pygame.display.set_caption("Jogo da Velha")

#as imagens 
VELHA = pygame.image.load(caminho_asset('Board.png'))
IMG_X = pygame.image.load(caminho_asset('X.png'))
IMG_O = pygame.image.load(caminho_asset('O.png'))

#cor, por formato RGB
cor_da_tela = (214, 201, 227)

#as grid do jogo da velha
campo = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
campo_grafico = [[[None, None], [None, None], [None, None]], 
                 [[None, None], [None, None], [None, None]], 
                 [[None, None], [None, None], [None, None]]]

mover = "X"

#está implemetando a cor no jogo e desenhando os formatos do jogo
tela.fill(cor_da_tela)
tela.blit(VELHA, (64, 64))

#atualizando o jogo para implementar as mudanças
pygame.display.update()

#função onde quando X ou O ganhar, desenha um risco vermelho sobre a jogada vitoriosa
def desenhar_linha_vencedora(pos_inicial, pos_final):
    pygame.draw.line(tela, (220, 20, 60), pos_inicial, pos_final, 15)
    pygame.display.update()


def Vitoria(campo):
    # Verifica se tem vitória de forma horizontal (Bug do índice [2] corrigido)
    for linha in range(0, 3):
        if (campo[linha][0] == campo[linha][1] == campo[linha][2]) and (campo[linha][0] is not None):
            y = 150 + linha * 300
            desenhar_linha_vencedora((50, y), (850, y))
            return campo[linha][0]

    # Verifica se tem vitoria vertical
    for coluna in range(0, 3):
        if (campo[0][coluna] == campo[1][coluna] == campo[2][coluna]) and (campo[0][coluna] is not None):
            x = 150 + coluna * 300
            desenhar_linha_vencedora((x, 50), (x, 850))
            return campo[0][coluna]

    # Verifica se tem vitoria na diagonal principal
    if (campo[0][0] == campo[1][1] == campo[2][2]) and (campo[0][0] is not None):
        desenhar_linha_vencedora((50, 50), (850, 850))
        return campo[0][0]

    # Verifica se tem vitória na diagonal secundária
    if (campo[0][2] == campo[1][1] == campo[2][0]) and (campo[0][2] is not None):
        desenhar_linha_vencedora((850, 50), (50, 850))
        return campo[0][2]

    # Verifica se não houve vitória, causando empate
    for i in range(len(campo)):
        for j in range(len(campo)):
            if campo[i][j] != 'X' and campo[i][j] != 'O':
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

    #forma de centralizar o quadrado
    x_centralizado = ((posicao_atual[0] - 65) / 835) * 2
    y_centralizado = (posicao_atual[1] / 835) * 2

    #verifica se o capo está vazio
    if campo[round(y_centralizado)][round(x_centralizado)] != 'O' and campo[round(y_centralizado)][round(x_centralizado)] != "X":
        campo[round(y_centralizado)][round(x_centralizado)] = mover

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
    campo = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    campo_grafico = [[[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]], 
                     [[None, None], [None, None], [None, None]]]
    mover = "X"
    tela.fill(cor_da_tela)
    tela.blit(VELHA, (64, 64))
    pygame.display.update()


while True:
    eventos = pygame.event.get()
    
    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Tela de Menu
    if estado_atual == "MENU":
        tela.fill((40, 44, 52))
        
        titulo = fonte_titulo.render("JOGO DA VELHA - MINIMAX", True, (255, 255, 255))
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 120))
        
        b1 = desenhar_botao("Jogar Manualmente", 250, 300, 400, 60, (70, 130, 180), (100, 149, 237))
        b2 = desenhar_botao("Contra Minimax Básico", 250, 400, 400, 60, (70, 130, 180), (100, 149, 237))
        b3 = desenhar_botao("Contra Minimax Alfa-Beta", 250, 500, 400, 60, (70, 130, 180), (100, 149, 237))
        b4 = desenhar_botao("Teste Automatizado", 250, 600, 400, 60, (220, 20, 60), (255, 99, 71))
        
#escolha da forma de jogar, manual, contra minimax básico, contra minimax alfa-beta ou teste automatizado
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

    # Tela de Escolher Símbolo
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
                    
    # Tela de jogando
    elif estado_atual == "JOGANDO":
        
        if mover == simbolo_jogador or modo_de_jogo == "MANUAL":
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    campo, mover = X_ou_O(campo, campo_grafico, mover)
                    
                    vencedor_atual = Vitoria(campo)
                    if vencedor_atual is not None:
                        pygame.time.delay(400) # Delay para visualizar o risco vermelho
                        
                        if vencedor_atual == "EMPATE":
                            resultado_texto = "Empate!"
                        elif modo_de_jogo == "MANUAL":
                            resultado_texto = f"Jogador {vencedor_atual} ganhou!"
                        elif vencedor_atual == simbolo_jogador:
                            resultado_texto = "Você ganhou!"
                        else:
                            resultado_texto = "A IA ganhou!"
                        estado_atual = "FIM_DE_JOGO"

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
       
    # Tela do fim de jogo
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

    # Tela de Teste
    elif estado_atual == "TESTE":
        tela.fill((30, 30, 30))
        titulo_logs = fonte_titulo.render("Teste Automatizado", True, (255, 255, 255))
        tela.blit(titulo_logs, (largura//2 - titulo_logs.get_width()//2, 30))

    if teste_logs is None:
        pygame.display.update()  # mostra o título antes de travar rodando as 200 partidas
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

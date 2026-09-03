import pygame
import sys

#comando para iniciar o jogo
pygame.init()

largura, altura = 900, 900

#tamanho do nosso jogo
tela = pygame.display.set_mode((largura, altura))

#nome do jogo
pygame.display.set_caption("Jogo da Velha")

#as imagens
VELHA = pygame.image.load('Tic-Tac-Toe-Py/pygame/assets/Board.png')
IMG_X = pygame.image.load('Tic-Tac-Toe-Py/pygame/assets/O.png')
IMG_O = pygame.image.load('Tic-Tac-Toe-Py/pygame/assets/X.png')

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

def Vitoria(campo):
    vencedor = None

    #verifica se tem vitória de forma horizontal
    for linha in range(0, 3):
        if((campo[linha][0] == campo[linha][1] == campo[linha][0]) and (campo[linha][0] is not None)):
            vencedor = campo[linha][0]

            #caso tiver um linha horizontal, vai colocar a imagem vencedora
            for i in range(0, 3):

                """Por algum motivo ocorre um bug, aonde a imagem vencedora esta inverso ao que ganhou
                ou seja, caso quem ganhou fosse o X, então a imagem vencedora mostra o O, então eu inverti
                o nome da imagem, tanto que for ver o Winning X, aparece na verdade o O"""
                campo_grafico[linha][i][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
                tela.blit(campo_grafico[linha][i][0], campo_grafico[linha][i][1])

            pygame.display.update()

            return vencedor

    #verifica se tem vitoria vertical
    for coluna in range(0, 3):
        if((campo[0][coluna] == campo[1][coluna] == campo[2][coluna]) and (campo[0][coluna] is not None)):
            vencedor = campo[0][coluna]

            for j in range(0, 3):
                campo_grafico[j][coluna][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
                tela.blit(campo_grafico[j][coluna][0], campo_grafico[j][coluna][1])

            pygame.display.update()

            return vencedor

    #verifica se tem vitoria na diagonal principal
    if (campo[0][0] == campo[1][1] == campo[2][2]) and (campo[0][0] is not None):
        vencedor =  campo[0][0]

        campo_grafico[0][0][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
        tela.blit(campo_grafico[0][0][0], campo_grafico[0][0][1])

        campo_grafico[1][1][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
        tela.blit(campo_grafico[1][1][0], campo_grafico[1][1][1])

        campo_grafico[2][2][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
        tela.blit(campo_grafico[2][2][0], campo_grafico[2][2][1])
        pygame.display.update()

        return vencedor

    #verifica se tem vitória na diagonal secundária
    if (campo[0][2] == campo[1][1] == campo[2][0]) and (campo[0][2] is not None):
        vencedor =  campo[0][2]

        campo_grafico[0][2][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
        tela.blit(campo_grafico[0][2][0], campo_grafico[0][2][1])

        campo_grafico[1][1][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
        tela.blit(campo_grafico[1][1][0], campo_grafico[1][1][1])

        campo_grafico[2][0][0] = pygame.image.load(f"Tic-Tac-Toe-Py/pygame/assets/Winning {vencedor}.png")
        tela.blit(campo_grafico[2][0][0], campo_grafico[2][0][1])

        pygame.display.update()

        return vencedor

    #verifica se não vitoria, causando em empate
    if vencedor is None:
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

jogo_finalizado = False

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #quando clicar no jogo aparece ou o X ou o O
        if evento.type == pygame.MOUSEBUTTONDOWN:
            campo, mover = X_ou_O(campo, campo_grafico, mover)

            #código para quando for reiniciar o jogo
            if jogo_finalizado:
                campo = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                campo_grafico = [[[None, None], [None, None], [None, None]], 
                                    [[None, None], [None, None], [None, None]], 
                                    [[None, None], [None, None], [None, None]]]

                mover = "X"

                tela.fill(cor_da_tela)
                tela.blit(VELHA, (64, 64))

                jogo_finalizado = False

                pygame.display.update()

            if Vitoria(campo) is not None:
                jogo_finalizado = True

            pygame.display.update()

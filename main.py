import pygame
from pygame.locals import *
import os
import random
from settings import *                                                          ################ MAYBE INUTIL?

# Inicialização do Pygame
pygame.init()

# clock = pygame.time.Clock()  # criar o relógio antes do loop



# Inicialização do Game
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(NOME_DO_JOGO)
# pygame.font.SysFont(FONT_1)                                                     ################ MAYBE INUTIL?






















# Classes dos jogadores
class Jogador:
    def __init__(self, x, y, cor):
        self.rect = pygame.Rect(x, y, TAMANHO_JOGADOR[0], TAMANHO_JOGADOR[1])
        self.cor = cor
        self.itens_coletados = 0  # Contador de itens coletados

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)

    def mover(self, teclas, cima, baixo, esquerda, direita):
        if teclas[cima]:
            self.rect.y -= VEL_JOGADOR
        if teclas[baixo]:
            self.rect.y += VEL_JOGADOR
        if teclas[esquerda]:
            self.rect.x -= VEL_JOGADOR
        if teclas[direita]:
            self.rect.x += VEL_JOGADOR



























# Classe do rio
class Rio:
    def __init__(self):
        self.x1 = 0
        self.x2 = LARGURA_TELA  # começa fora da tela à esquerda
        self.y = 0  # posição vertical do rio visível na parte inferior
        self.altura = ALTURA_TELA-(ALTURA_TELA/3) # altura do retângulo do rio
        self.cor = AZUL

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, (self.x1, self.y, LARGURA_TELA, self.altura))

# Criar rio
rio = Rio()









# Classe dos itens
# class Item:
#     def __init__(self, y):
#         self.rect = pygame.Rect(random.randint(-100, -50), ALTURA_TELA-500, 30, 30)
#         self.cor = AMARELO

#     def mover(self):
#         self.rect.x += VEL_ITEM

#     def desenhar(self):
#         pygame.draw.rect(TELA, self.cor, self.rect)




# def desenhar_objetos(self, ):

class Item:
    def __init__(self):
        y_positions = list(range(ALTURA_TELA - 300, ALTURA_TELA - 700, -50)) # Posições y dos objetos do rio
#        [ALTURA_TELA - 300, ALTURA_TELA - 350, ALTURA_TELA - 400, ALTURA_TELA - 450, ALTURA_TELA - 500, ALTURA_TELA - 550, ALTURA_TELA - 600, ALTURA_TELA - 650]
        self.rect = pygame.Rect(random.randint(-100, -50), random.choice(y_positions), TAMANHO_ITEM[0], TAMANHO_ITEM[1])
        self.cor = AMARELO

    def mover(self):
        self.rect.x += VEL_ITEM

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)

# Criar itens
itens = [Item() for _ in range(9)]













# Criar jogadores
jogador1 = Jogador(300, ALTURA_TELA-100, VERDE)  # Verde
jogador2 = Jogador(LARGURA_TELA-300, ALTURA_TELA-100, AZUL)  # Azul






















































































clock = pygame.time.Clock()  # criando o relógio antes do loop

# Loop principal
JOGO_RODANDO = True
while JOGO_RODANDO:
    clock.tick(FPS) # velocidade de atualização da tela ou FPS(Frames por segundo)
    TELA.fill(PRETO)    # cor do background sem imagem
# JOGO_RODANDO = True
# while JOGO_RODANDO:
#     pygame.time.Clock().tick(FPS)          # controla o FPS corretamente (ex: 60 FPS)
#     TELA.fill(PRETO)
#     Opção mudar a lógica Frames Por Segundo


    # Movimentação dos itens
    for item in itens:
        item.mover()

    teclas = pygame.key.get_pressed()
    jogador1.mover(teclas, K_w, K_s, K_a, K_d)
    jogador2.mover(teclas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

    # Verificar colisão (coleta de itens)
    for item in itens:
        if jogador1.rect.colliderect(item.rect):
            jogador1.itens_coletados += 1
            item.rect.x = LARGURA_TELA  # Reposiciona o item
        elif jogador2.rect.colliderect(item.rect):
            jogador2.itens_coletados += 1
            item.rect.x = LARGURA_TELA

    # Desenhar na tela
    rio.desenhar()
    for item in itens:
        item.desenhar()
    jogador1.desenhar()
    jogador2.desenhar()

    # Exibir pontuação
    fonte = pygame.font.SysFont('Arial', 24)
    texto1 = fonte.render(f'Jogador 1: {jogador1.itens_coletados}', True, VERMELHO)
    texto2 = fonte.render(f'Jogador 2: {jogador2.itens_coletados}', True, VERMELHO)
    largura_texto2 = texto2.get_width()
    TELA.blit(texto1, (10, 10))
    TELA.blit(texto2, (LARGURA_TELA-largura_texto2-10, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            JOGO_RODANDO = False

# Finaliza o Pygame
pygame.quit()

import pygame
from pygame.locals import *
import os
import sys
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
        if teclas[cima] and self.rect.top > 2*(ALTURA_TELA/3):
            self.rect.y -= VEL_JOGADOR
        if teclas[baixo] and self.rect.bottom < ALTURA_TELA-int(ALTURA_TELA/20):
            self.rect.y += VEL_JOGADOR
        if teclas[esquerda] and self.rect.left > 0:
            self.rect.x -= VEL_JOGADOR
        if teclas[direita] and self.rect.right < LARGURA_TELA:
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









class Item_agua:
    def __init__(self):
        y_positions = list(range(ALTURA_TELA - 300, ALTURA_TELA - 700, -50)) # Posições y dos objetos do rio
#        [ALTURA_TELA - 300, ALTURA_TELA - 350, ALTURA_TELA - 400, ALTURA_TELA - 450, ALTURA_TELA - 500, ALTURA_TELA - 550, ALTURA_TELA - 600, ALTURA_TELA - 650]
        self.rect = pygame.Rect(random.randint(-100, -50), random.choice(y_positions), TAMANHO_ITEM[0], TAMANHO_ITEM[1])
        self.cor = AMARELO

    def mover(self):
        self.rect.x += VEL_ITEM

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)

# Evento para criar itens
CRIAR_ITEM_EVENTO = pygame.USEREVENT + 2
pygame.time.set_timer(CRIAR_ITEM_EVENTO, 1000)  # 1000 ms = 1 segundo
itens_agua = []
CRIAR_ITEM_EVENTO_2 = pygame.USEREVENT + 1
pygame.time.set_timer(CRIAR_ITEM_EVENTO_2, 1000)  # 1000 ms = 1 segundo
itens_terra = []




class Item_terra:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(0, LARGURA_TELA - TAMANHO_ITEM[0]), 
            random.randint(int(2*(ALTURA_TELA/3)), ALTURA_TELA-int(ALTURA_TELA/20)-TAMANHO_ITEM[1]), 
            TAMANHO_ITEM[0], 
            TAMANHO_ITEM[1]) # parametros (X, Y, TAMANHO_ITEM, TAMANHO_ITEM)
        self.cor = VERMELHO

    def mover(self):
        pass

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)

























# Criar jogadores
jogador1 = Jogador(300, ALTURA_TELA-100, VERDE)  # Verde
jogador2 = Jogador(LARGURA_TELA-300, ALTURA_TELA-100, ROXO)  # Roxo





























































def tela_vitoria():
    vitoria_jogadores = True
    while vitoria_jogadores:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                vitoria_jogadores = False  # Sai da tela de vitória com qualquer tecla
                
        TELA.fill((PRETO))
        texto = fonte.render('Parabéns, vocês ajudaram na limpeza do rio!', True, BRANCO)
        TELA.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, ALTURA_TELA // 2 - 50))

        pygame.display.update()







clock = pygame.time.Clock()  # criando o relógio antes do loop

# Loop principal
JOGO_RODANDO = True
while JOGO_RODANDO:
    clock.tick(FPS) # velocidade de atualização da tela ou FPS(Frames por segundo)
    TELA.fill(PRETO)    # cor do background sem imagem



    teclas = pygame.key.get_pressed()
    jogador1.mover(teclas, K_w, K_s, K_a, K_d)
    jogador2.mover(teclas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

    # Verificar colisão (coleta de itens)
    for item in itens_agua:
        if jogador1.rect.colliderect(item.rect):
            jogador1.itens_coletados += 1
            item.rect.x = LARGURA_TELA  # Reposiciona o item
        elif jogador2.rect.colliderect(item.rect):
            jogador2.itens_coletados += 1
            item.rect.x = LARGURA_TELA
            
    for item in itens_terra:
        if jogador1.rect.colliderect(item.rect):
            jogador1.itens_coletados += 1
            item.rect.x = LARGURA_TELA  # Reposiciona o item
        elif jogador2.rect.colliderect(item.rect):
            jogador2.itens_coletados += 1
            item.rect.x = LARGURA_TELA

    # Desenhar na tela
    rio.desenhar()
    for item in itens_agua:
        item.desenhar()
        item.mover() # Movimentação dos itens
    
    for item in itens_terra:
        item.desenhar()
        item.mover()


    jogador1.desenhar()
    jogador2.desenhar()
    
    # Exibir pontuação
    fonte = pygame.font.SysFont('Arial', 24)
    texto1 = fonte.render(f'Jogador 1: {jogador1.itens_coletados}', True, VERMELHO)
    texto2 = fonte.render(f'Jogador 2: {jogador2.itens_coletados}', True, VERMELHO)
    largura_texto2 = texto2.get_width()
    TELA.blit(texto1, (10, 10))
    TELA.blit(texto2, (LARGURA_TELA-largura_texto2-10, 10))

    # Exibir vencedor
    if (jogador1.itens_coletados + jogador2.itens_coletados) >= OBJETIVO:
        tela_vitoria()
        rodando = False





    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            JOGO_RODANDO = False
        if event.type == CRIAR_ITEM_EVENTO:
            for _ in range(3):
                itens_agua.append(Item_agua())
                
        if event.type == CRIAR_ITEM_EVENTO_2:
            for _ in range(1):
                itens_terra.append(Item_terra())
            


# Finaliza o Pygame
pygame.quit()

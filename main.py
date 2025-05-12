import pygame
from pygame.locals import *
import os
import sys
import random
from settings import *                                                          ################ MAYBE INUTIL?

# Inicialização do Pygame
pygame.init()



# Inicialização do Game
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(NOME_DO_JOGO)


FONTE_TEXTO = pygame.font.SysFont(*FONTES["texto"])
FONTE_TEXTO_NEGRITO = pygame.font.SysFont(*FONTES["texto"], bold=True)
FONTE_TITULO = pygame.font.SysFont(*FONTES["titulo"])
FONTE_TITULO_NEGRITO = pygame.font.SysFont(*FONTES["titulo"], bold=True)


















# Classes dos jogadores
class Jogador:
    def __init__(self, x, y, cor):
        self.rect = pygame.Rect(x, y, TAMANHO_JOGADOR[0], TAMANHO_JOGADOR[1])
        self.cor = cor
        self.itens_coletados = 0  # Contador de itens coletados
        self.rede = None

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


    def coletar_item(self):
        # Coletar item diretamente abaixo do jogador 1
        for item in itens_agua:
            if self.rect.colliderect(item.rect):
                self.itens_coletados += 1
                itens_terra.remove(item)  # Remove o item da lista
                break

    def lançar_rede(self):
        # Verifica se o jogador 2 clicou e cria a rede
        self.pos_mouse = pygame.mouse.get_pos()
        self.rede_rect = pygame.Rect(300,200,30,30)
        self.rede = pygame.Rect(self.rect[0] - 15, self.rect.centery - 15, 30, 30)
        self.rede.center = self.pos_mouse
            

    def desenhar_rede(self):
        if self.rede:
            pygame.draw.circle(TELA, CORES["BRANCO"], self.rede.center, 30)
























# Classe do rio
class Rio:
    def __init__(self):
        self.x1 = 0
        self.x2 = LARGURA_TELA  # começa fora da tela à esquerda
        self.y = 0  # posição vertical do rio visível na parte inferior
        self.altura = ALTURA_TELA-(ALTURA_TELA/3) # altura do retângulo do rio
        self.cor = CORES["AZUL"]

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, (self.x1, self.y, LARGURA_TELA, self.altura))

# Criar rio
rio = Rio()








# Classes Item (Água e Terra)
class Item_agua:
    def __init__(self):
        y_positions = list(range(ALTURA_TELA - 300, ALTURA_TELA - 700, -50)) # Posições y dos objetos do rio
#        [ALTURA_TELA - 300, ALTURA_TELA - 350, ALTURA_TELA - 400, ALTURA_TELA - 450, ALTURA_TELA - 500, ALTURA_TELA - 550, ALTURA_TELA - 600, ALTURA_TELA - 650]
        self.rect = pygame.Rect(random.randint(-100, -50), random.choice(y_positions), TAMANHO_ITEM[0], TAMANHO_ITEM[1])
        self.cor = CORES["AMARELO"]

    def mover(self):
        self.rect.x += VEL_ITEM

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)

class Item_terra:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, LARGURA_TELA - TAMANHO_ITEM[0]), random.randint(2*(ALTURA_TELA//3), ALTURA_TELA-ALTURA_TELA//20-TAMANHO_ITEM[1]), TAMANHO_ITEM[0], TAMANHO_ITEM[1]) # parametros (X, Y, TAMANHO_ITEM, TAMANHO_ITEM)
        self.cor = CORES["VERMELHO"]

    def mover(self):
        pass

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)


# Evento para criar itens
CRIAR_ITEM_EVENTO = pygame.USEREVENT + 2
pygame.time.set_timer(CRIAR_ITEM_EVENTO, 1000)  # 1000 ms = 1 segundo
itens_agua = []
CRIAR_ITEM_EVENTO_2 = pygame.USEREVENT + 1
pygame.time.set_timer(CRIAR_ITEM_EVENTO_2, 3000)  # 1000 ms = 1 segundo
itens_terra = []





























# Criar jogadores
jogador1 = Jogador(300, ALTURA_TELA-100, CORES["VERDE"])  # Verde
jogador2 = Jogador(LARGURA_TELA-300, ALTURA_TELA-100, CORES["ROXO"])  # Roxo









































def desenhar_barra_progresso(TELA, x, y, largura, altura):
    # Fundo da barra
    pygame.draw.rect(TELA, CORES["CINZA_CLARO"], (x, y, largura, altura))

    # Calcular largura da barra preenchida
    preenchimento_barra = int((progresso / OBJETIVO) * largura)
    # Preenchimento proporcional / Barra preenchida
    pygame.draw.rect(TELA, CORES["VERDE"], (x, y, preenchimento_barra, altura))  # Barra verde de progressão

    # Borda da barra (contorno)
    pygame.draw.rect(TELA, CORES["PRETO"], (x, y, largura, altura), 2)  # Preto, contorno

    # Texto centralizado
    texto = f"{progresso}/{OBJETIVO}"
    superficie_texto = FONTE_TITULO.render(texto, True, CORES["PRETO"])
    largura_texto = superficie_texto.get_width()
    altura_texto = superficie_texto.get_height()
    pos_texto_x = x + (largura - largura_texto) // 2
    pos_texto_y = y + (altura - altura_texto) // 2
    TELA.blit(superficie_texto, (pos_texto_x, pos_texto_y))











def tela_vitoria():
    vitoria_jogadores = True
    while vitoria_jogadores:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                vitoria_jogadores = False  # Sai da tela de vitória com qualquer tecla
                
        TELA.fill((CORES["PRETO"]))
        TEXTO = FONTE_TITULO_NEGRITO.render('Parabéns, vocês ajudaram na limpeza do rio!', True, CORES["BRANCO"])
        TELA.blit(TEXTO, (LARGURA_TELA // 2 - TEXTO.get_width() // 2, ALTURA_TELA // 2 - 50))

        pygame.display.update()





def circle_colide(objeto:list,circulo:list,raio):
    # Definir a colisão com a esquerda e direita do circulo
    coli_x_esquerda = objeto[0] >= circulo[0] - raio
    coli_x_direita = objeto[0] <= circulo[0] + raio
    # Se o objeto está entre circulo -30 e circulo + 30
    coli_y_topo = objeto[1] >= circulo[1] - raio
    coli_y_baixo = objeto[1] <= circulo[1] + raio
    
    colide = [coli_x_esquerda,coli_x_direita,coli_y_topo,coli_y_baixo]
    return colide

clock = pygame.time.Clock()  # criando o relógio antes do loop

# Loop principal
JOGO_RODANDO = True
rede_circle = [999,999]
while JOGO_RODANDO:
    clock.tick(FPS) # velocidade de atualização da tela ou FPS(Frames por segundo)
    TELA.fill(CORES["PRETO"])    # cor do background sem imagem
    progresso = jogador1.itens_coletados + jogador2.itens_coletados # Progresso geral



    teclas = pygame.key.get_pressed()
    jogador1.mover(teclas, K_w, K_s, K_a, K_d)
    jogador2.mover(teclas, K_UP, K_DOWN, K_LEFT, K_RIGHT)



    for item in itens_terra:
        if jogador1.rect.colliderect(item.rect) and teclas[K_SPACE]:
            jogador1.itens_coletados += 1
            item.rect.x = LARGURA_TELA  # Reposiciona o item


    for item in itens_agua:
        pos = item.rect[0],item.rect[1]
        if jogador2.rect.colliderect(item.rect):
            jogador2.itens_coletados += 1
            item.rect.x = LARGURA_TELA
        if False not in circle_colide(pos,rede_circle,60):
            jogador2.itens_coletados += 1
            item.rect.x = LARGURA_TELA

    # Verificar colisão (coleta de itens)
    # for item in itens_agua:
    #     if jogador1.rect.colliderect(item.rect):
    #         jogador1.itens_coletados += 1
    #         item.rect.x = LARGURA_TELA  # Reposiciona o item
    #     elif jogador2.rect.colliderect(item.rect):
    #         jogador2.itens_coletados += 1
    #         item.rect.x = LARGURA_TELA
            
    # for item in itens_terra:
    #     if jogador1.rect.colliderect(item.rect):
    #         jogador1.itens_coletados += 1
    #         item.rect.x = LARGURA_TELA  # Reposiciona o item
    #     elif jogador2.rect.colliderect(item.rect):
    #         jogador2.itens_coletados += 1
    #         item.rect.x = LARGURA_TELA



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







    desenhar_barra_progresso(
        TELA,
        LARGURA_TELA//2-(LARGURA_BARRA//2),         # Posição x na tela
        10,                                                     # Posição y na tela
        LARGURA_BARRA, ALTURA_BARRA                             # Tamanho da barra
    )

    # Exibir pontuação
    TEXTO1 = FONTE_TEXTO_NEGRITO.render(f'Jogador 1: {jogador1.itens_coletados}', True, CORES["VERDE"])
    TEXTO2 = FONTE_TEXTO_NEGRITO.render(f'Jogador 2: {jogador2.itens_coletados}', True, CORES["VERDE"])
    TEXTO3 = FONTE_TITULO_NEGRITO.render(f'OBJETIVO', True, CORES["VERDE_CLARO"])
    largura_texto2 = TEXTO2.get_width()
    largura_texto3 = TEXTO3.get_width()
    TELA.blit(TEXTO1, (10, 10))
    TELA.blit(TEXTO2, (LARGURA_TELA-largura_texto2-10, 10))
    TELA.blit(TEXTO3, (LARGURA_TELA//2-(largura_texto3//2), ALTURA_BARRA+10))




    # Exibir vencedor
    if (progresso) >= OBJETIVO:
        tela_vitoria()
        JOGO_RODANDO = False






    for event in pygame.event.get():
        if event.type == QUIT:
            JOGO_RODANDO = False
        if event.type == CRIAR_ITEM_EVENTO:
            for _ in range(3):
                itens_agua.append(Item_agua())
        if event.type == CRIAR_ITEM_EVENTO_2:
            for _ in range(1):
                itens_terra.append(Item_terra())
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Ação com botão esquerdo do mouse
            # jogador2.lançar_rede()
            # print(f'{jogador2.rede_rect=}')
            # pygame.draw.rect(TELA,CORES["BRANCO"],jogador2.rede_rect)
            # pygame.blit()
            pos_mouse = pygame.mouse.get_pos()
            rede_circle = [pos_mouse[0], pos_mouse[1]]
            
        if event.type == KEYDOWN and event.key == K_SPACE: # Ação com botão Espaço
            jogador2.coletar_item()
    try:
        pygame.draw.circle(TELA, CORES["BRANCO"], (rede_circle[0], rede_circle[1]), 50)
    except:
        pass


# Atualiza a tela
    pygame.display.update()

# Finaliza o Pygame
pygame.quit()

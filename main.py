import pygame
from pygame.locals import *
import os
import sys
import random
from configs import *
from menu import Menu

# Inicialização do Pygame
pygame.init()

# Inicialização do Game
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(NOME_DO_JOGO)

# Inicializar o menu
menu = Menu(TELA)

FONTE_TEXTO = pygame.font.SysFont(*FONTES["texto"])
FONTE_TEXTO_NEGRITO = pygame.font.SysFont(*FONTES["texto"], bold=True)
FONTE_TITULO = pygame.font.SysFont(*FONTES["titulo"])
FONTE_TITULO_NEGRITO = pygame.font.SysFont(*FONTES["titulo"], bold=True)
FONTE_CONCLUSAO = pygame.font.SysFont(*FONTES["conclusao"])
FONTE_CONCLUSAO_NEGRITO = pygame.font.SysFont(*FONTES["conclusao"], bold=True)





























class Jogo:
    def __init__(self, tela): # Inicializa o menu do jogo.     ||       parâmetro tela -> Superfície do pygame onde o menu será desenhado
        self.tela = tela
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()

        # Carregar imagem de fundo
        try:
            self.background = pygame.image.load(os.path.join('assets', 'tela_jogo_capibariver.png'))
            self.background = pygame.transform.scale(self.background, (self.largura_tela, self.altura_tela))
        except:
            print("Imagem de fundo não encontrada. Usando cor sólida.")
            self.background = None
    
    def desenhar(self):                                     # Desenha o menu principal
        if self.background:
            self.tela.blit(self.background, (0, 0))         # Desenha o fundo
        else:
            pass













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
        for item in itens_terra:
            if self.rect.colliderect(item.rect):
                self.itens_coletados += 1
                itens_terra.remove(item)  # Remove o item da lista
                break
    
# todo ---------------------------------------------------------------------------------------------------
    def lançar_rede(self):
        # Verifica se o jogador 2 clicou e cria a rede
        self.pos_mouse = pygame.mouse.get_pos()
        self.rede_rect = pygame.Rect(300,200,30,30)
        self.rede = pygame.Rect(self.rect[0] - 15, self.rect.centery - 15, 30, 30)
        self.rede.center = self.pos_mouse
            
    def desenhar_rede(self):
        if self.rede:
            pygame.draw.circle(TELA, CORES["BRANCO"], self.rede.center, 30)


# todo ---------------------------------------------------------------------------------------------------






































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
                    # [ALTURA_TELA - 300, ALTURA_TELA - 350, ALTURA_TELA - 400, ALTURA_TELA - 450, ALTURA_TELA - 500, ALTURA_TELA - 550, ALTURA_TELA - 600, ALTURA_TELA - 650]
        self.rect = pygame.Rect(random.randint(-100, -50), random.choice(y_positions), TAMANHO_ITEM[0], TAMANHO_ITEM[1])
        self.cor = CORES["LARANJA"]

    def mover(self):
        self.rect.x += VEL_ITEM

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)

class Item_terra:
    def __init__(self):
        x1_margem = 5*(LARGURA_TELA//40) # antes era 0
        x2_margem = 37*(LARGURA_TELA//40) - TAMANHO_ITEM[0] # antes era LARGURA_TELA - TAMANHO_ITEM[0]
        y1_margem = 2*(ALTURA_TELA//3)
        y2_margem = ALTURA_TELA-ALTURA_TELA//20-TAMANHO_ITEM[1]
        self.rect = pygame.Rect(random.randint(x1_margem, x2_margem), random.randint(y1_margem, y2_margem), TAMANHO_ITEM[0], TAMANHO_ITEM[1]) # parametros (x(x1, x2), y(y1, y2), TAMANHO_ITEM, TAMANHO_ITEM)
        self.cor = CORES["VERMELHO"]

    def mover(self):
        pass

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.rect)


















class Conclusao:
    def __init__(self, tela): # Inicializa o background da tela de conclusão do jogo.     ||       parâmetro tela -> Superfície do pygame onde o menu será desenhado
        self.tela = tela
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()

        # Carregar imagem de fundo
        try:
            self.background = pygame.image.load(os.path.join('assets', 'tela_conclusao_capibariver.png'))
            self.background = pygame.transform.scale(self.background, (self.largura_tela, self.altura_tela))
        except:
            print("Imagem de fundo não encontrada. Usando cor sólida.")
            self.background = None
    
    def desenhar(self):                                     # Desenha o menu principal
        if self.background:
            self.tela.blit(self.background, (0, 0))         # Desenha o fundo
        else:
            pass













def iniciar_jogo():
    global jogador1, jogador2, itens_agua, itens_terra, CRIAR_ITEM_EVENTO, CRIAR_ITEM_EVENTO_2
    
    # Criar jogadores
    jogador1 = Jogador(300, ALTURA_TELA-100, CORES["AMARELO"])  # Amarelo
    jogador2 = Jogador(LARGURA_TELA-300, ALTURA_TELA-100, CORES["ROXO"])  # Roxo
    
    # Evento para criar itens
    CRIAR_ITEM_EVENTO = pygame.USEREVENT + 2
    pygame.time.set_timer(CRIAR_ITEM_EVENTO, 1000)  # 1000 ms = 1 segundo
    itens_agua = []
    
    CRIAR_ITEM_EVENTO_2 = pygame.USEREVENT + 1
    pygame.time.set_timer(CRIAR_ITEM_EVENTO_2, 3000)  # 3000 ms = 3 segundos
    itens_terra = []

















































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
# !!!!!!!!! ----------------------------------------------------- ALERTA ARRUMAR DEPOIS, NÃO ESTÁ RESPONSIVO ----------------------------------------------------------------
        Conclusao(TELA).desenhar()
        TEXTO1 = FONTE_CONCLUSAO_NEGRITO.render('Parabéns!', True, CORES["CIANO"], 1)
        TEXTO2 = FONTE_CONCLUSAO_NEGRITO.render('Vocês ajudaram na limpeza do rio.', True, CORES["VERDE"], 1)
        TEXTO3 = FONTE_CONCLUSAO_NEGRITO.render('Graças aos seus esforços, o rio foi salvo.', True, CORES["VERDE"], 1)
        TEXTO4 = FONTE_CONCLUSAO_NEGRITO.render('Continue com o bom trabalho!', True, CORES["VERDE"], 1)

        TELA.blit(TEXTO1, (LARGURA_TELA // 2 - TEXTO1.get_width() // 2, ALTURA_TELA // 5 - ALTURA_TELA // 10))
        TELA.blit(TEXTO2, (LARGURA_TELA // 2 - TEXTO2.get_width() // 2, ALTURA_TELA // 5 + ALTURA_TELA // 10 - 50))
        TELA.blit(TEXTO3, (LARGURA_TELA // 2 - TEXTO3.get_width() // 2, ALTURA_TELA // 5 + ALTURA_TELA // 10 + 50))
        TELA.blit(TEXTO4, (LARGURA_TELA // 2 - TEXTO4.get_width() // 2, ALTURA_TELA // 5 + ALTURA_TELA // 10 + 150))
# !!!!!!!!! ----------------------------------------------------- ALERTA ARRUMAR DEPOIS, NÃO ESTÁ RESPONSIVO ----------------------------------------------------------------

        # TELA.blit(TEXTO1, (LARGURA_TELA // 2 - TEXTO1.get_width() // 2, ALTURA_TELA // 2 - 50))

        pygame.display.update()

































def circle_colide(objeto:list, circulo:list, raio):
    # Definir a colisão com a esquerda e direita do circulo
    coli_x_esquerda = objeto[0] >= circulo[0] - raio
    coli_x_direita = objeto[0] <= circulo[0] + raio
    # Se o objeto está entre circulo -30 e circulo + 30
    coli_y_topo = objeto[1] >= circulo[1] - raio
    coli_y_baixo = objeto[1] <= circulo[1] + raio
    colide = [coli_x_esquerda, coli_x_direita, coli_y_topo, coli_y_baixo]
    return colide













# Variáveis globais
jogador1 = None
jogador2 = None
itens_agua = []
itens_terra = []
CRIAR_ITEM_EVENTO = None
CRIAR_ITEM_EVENTO_2 = None
progresso = 0
rede_circle = [999, 999]





























# Inicializar o jogo
iniciar_jogo()

clock = pygame.time.Clock()  # criando o relógio antes do loop


































# Loop principal
JOGO_RODANDO = True
while JOGO_RODANDO:
    clock.tick(FPS) # velocidade de atualização da tela ou FPS(Frames por segundo)
    
    # Processar eventos
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == QUIT:
            JOGO_RODANDO = False
            
        # Eventos específicos do jogo
        if menu.estado == "JOGO":
            if evento.type == CRIAR_ITEM_EVENTO:
                for _ in range(3):
                    itens_agua.append(Item_agua())
            if evento.type == CRIAR_ITEM_EVENTO_2:
                for _ in range(99):
                    itens_terra.append(Item_terra())
# todo ---------------------------------------------------------------------------------------------------
            # Colisão e coleta do jogador 2
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:  # Ação com botão esquerdo do mouse
                # jogador2.lançar_rede()
                # print(f'{jogador2.rede_rect=}')
                # pygame.draw.rect(TELA,CORES["BRANCO"],jogador2.rede_rect)
                # pygame.blit()
                pos_mouse = pygame.mouse.get_pos() 
                rede_circle = [pos_mouse[0], pos_mouse[1]]
                for item in itens_agua:
                    pos = item.rect[0], item.rect[1]
                    if jogador2.rect.colliderect(item.rect):
                        jogador2.itens_coletados += 1
                        item.rect.x = LARGURA_TELA
                    if False not in circle_colide(pos, rede_circle, 60):
                        jogador2.itens_coletados += 1
                        item.rect.x = LARGURA_TELA
# todo ---------------------------------------------------------------------------------------------------
            # Colisão e coleta do jogador 1
            for item in itens_terra:
                if jogador1.rect.colliderect(item.rect):
                    if evento.type ==  pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                        jogador1.coletar_item()
                        break



    
    # Processar eventos do menu
    menu.eventos(eventos)
    
    # Desenhar a tela atual baseada no estado
    if menu.estado == "MENU":
        menu.desenhar()
    elif menu.estado == "GUIA":
        menu.desenhar_guia()
    elif menu.estado == "CREDITOS":
        menu.desenhar_creditos()
    elif menu.estado == "OPCOES":
        menu.desenhar_opcoes()
    elif menu.estado == "JOGO":
        # Lógica do jogo
        TELA.fill(CORES["PRETO"])
        
        # Atualizar o progresso
        progresso = jogador1.itens_coletados + jogador2.itens_coletados
        
        # Movimentação dos jogadores
        teclas = pygame.key.get_pressed()





















        jogador1.mover(teclas, K_w, K_s, K_a, K_d)
        jogador2.mover(teclas, K_UP, K_DOWN, K_LEFT, K_RIGHT)


        # Desenhar elementos do jogo
        rio.desenhar()

        # desenhando o background do jogo
        Jogo(TELA).desenhar()
        
        for item in itens_agua:
            item.desenhar()
            item.mover() # Movimentação dos itens
        
        for item in itens_terra:
            item.desenhar()
            item.mover() # Movimentação dos itens
        
        # Desenhar jogadores
        jogador1.desenhar()
        jogador2.desenhar()



        
        # Desenhar rede
        try:
            pygame.draw.circle(TELA, CORES["BRANCO"], (rede_circle[0], rede_circle[1]), 50)
        except:
            pass
        
        # Barra de progresso
        desenhar_barra_progresso(
            TELA,
            LARGURA_TELA//2-(LARGURA_BARRA//2),                     # Posição x na tela
            10,                                                     # Posição y na tela
            LARGURA_BARRA, ALTURA_BARRA                             # Tamanho da barra (largura e altura)
    )
        
        # Exibir pontuação
        TEXTO1 = FONTE_TEXTO_NEGRITO.render(f'Jogador 1: {jogador1.itens_coletados}', True, CORES["AMARELO"])
        TEXTO2 = FONTE_TEXTO_NEGRITO.render(f'Jogador 2: {jogador2.itens_coletados}', True, CORES["ROXO"])
        TEXTO3 = FONTE_TITULO_NEGRITO.render(f'OBJETIVO', True, CORES["PRETO"])
        largura_texto2 = TEXTO2.get_width()
        largura_texto3 = TEXTO3.get_width()
        TELA.blit(TEXTO1, (10, 10))
        TELA.blit(TEXTO2, (LARGURA_TELA-largura_texto2-10, 10))
        TELA.blit(TEXTO3, (LARGURA_TELA//2-(largura_texto3//2), ALTURA_BARRA+10))
        
        # Verificador para validar se o objetivo foi alcançado
        if progresso >= OBJETIVO:
            tela_vitoria()
            menu.estado = "MENU"  # Volta para o menu após a vitória
            if menu.estado == "MENU" and iniciar_jogo() == True:
                menu.estado = "JOGO"
            # elif teclas[K_ESC] == (JOGO_RODANDO == False)
            # -------------------------------------------------------------------------------------------------------------------------
            # -------------------------------------------------------------------------------------------------------------------------
            # -------------------------------------------------------------------------------------------------------------------------
            # -------------------------------------------------------------------------------------------------------------------------
    
    # Atualizar a tela
    pygame.display.update()

# Finaliza o Pygame
pygame.quit()
sys.exit()
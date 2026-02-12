import pygame, os, sys, random
from pygame.locals import *
from configs import *
from menu import Menu
from entities.players import Jogador
from entities.items import *
from utils import *
from gameSystemFunctions import game 
from gameSystemFunctions.mapComponents import river
from gameSystemFunctions.gameEnding import conclusion

# ------------- Ignition Variables -----------------
pygame.init() # Inicialização do Pygame
pygame.mixer.init() # Inicialização da Música no Pygame
pygame.display.set_caption(NOME_DO_JOGO) # Inicialização da tela do Game
fullscreen = False # Deixa o jogo em modo janela por default
menu = Menu(TELA) # Inicialização do menu
jogo = game.Jogo(TELA) # Deixa toda a parte jogável do jogo pronta antes de apertar "jogar"
rio = river.Rio() # Cria rio
# --------------------------------------------------

def iniciar_jogo():
    global jogador1, jogador2, itens_agua, itens_terra, CRIAR_ITEM_EVENTO, CRIAR_ITEM_EVENTO_2


    # spritesheet path
    spritesheet_path1 = os.path.join('assets/sprites/players', 'Jogador1_spritesheet_movement.png')
    spritesheet_path2 = os.path.join('assets/sprites/players', 'Jogador2_spritesheet_movement.png')
    
    # Cria jogadores (COM animação)
    jogador1 = Jogador(300, ALTURA_TELA-100, CORES["AMARELO"], spritesheet_path1, 1)
    jogador2 = Jogador(LARGURA_TELA-300, ALTURA_TELA-100, CORES["ROXO"], spritesheet_path2, 2)

    # Evento para criar itens (intervalo entre a criação de itens)
    CRIAR_ITEM_EVENTO = pygame.USEREVENT + 2
    pygame.time.set_timer(CRIAR_ITEM_EVENTO, 1000)  # 1000 ms = 1 segundo
    itens_agua = []
    # Jogador.criar_item_evento(CRIAR_ITEM_EVENTO, 2, 1000, itens_agua)
    CRIAR_ITEM_EVENTO_2 = pygame.USEREVENT + 1
    pygame.time.set_timer(CRIAR_ITEM_EVENTO_2, 3000)  # 3000 ms = 3 segundos
    itens_terra = []
    # Jogador.criar_item_evento(CRIAR_ITEM_EVENTO_2, 1, 3000, itens_terra)

def circle_colide(objeto:list, circulo:list, raio):
    # Define a colisão com a esquerda e direita do circulo
    coli_x_esquerda = objeto[0] >= circulo[0] - raio
    coli_x_direita = objeto[0] <= circulo[0] + raio
    # Se o objeto está entre círculo -30 e círculo + 30
    coli_y_topo = objeto[1] >= circulo[1] - raio
    coli_y_baixo = objeto[1] <= circulo[1] + raio
    colide = [coli_x_esquerda, coli_x_direita, coli_y_topo, coli_y_baixo]
    return colide

# Inicializa o jogo
iniciar_jogo()

clock = pygame.time.Clock()  # Cria o relógio antes do loop

# Loop principal
JOGO_RODANDO = True

# Variáveis da rede.
rede_timer = -1
rede_chegou = False
rede_origem = [10000,10000]
pontos_jogada = 0
REDE = pygame.surface.Surface((100,100))
imagem_rede = pygame.image.load('assets/sprites/players/Jogador2_object_rede.png')
imagem_rede.set_colorkey((0,0,0))
REDE.blit(imagem_rede,(0,0))

while JOGO_RODANDO:
    clock.tick(FPS) # Velocidade de atualização da tela ou FPS (Frames Por Segundo)
    # Processa eventos
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == QUIT:
            JOGO_RODANDO = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            elif evento.key == pygame.K_ESCAPE:
                # Verifica se está em fullscreen checando as flags da tela
                current_flags = TELA.get_flags()
                if current_flags & pygame.FULLSCREEN:
                    pygame.display.toggle_fullscreen()
        # Eventos específicos do jogo
        if menu.estado == "JOGO":
            # Obter o tempo decorrido desde o último frame (em segundos)
            dt = clock.get_time() / 1000.0
            # Atualiza animações
            # Eventos (criação de items)
            if evento.type == CRIAR_ITEM_EVENTO:
                if progresso <= OBJETIVO / 4:
                    for _ in range(QUANT_LIXOS_AGUA): # Começa em 8 e vai diminuindo por mapa de 2 em 2, até 2
                        itens_agua.append(Item_agua())
                elif progresso <= OBJETIVO / 2:
                    for _ in range( (QUANT_LIXOS_AGUA * 3) // 4  ): 
                        itens_agua.append(Item_agua())
                elif progresso <= (3 * OBJETIVO) / 4:
                    for _ in range(QUANT_LIXOS_AGUA // 2): 
                        itens_agua.append(Item_agua())
                else:  
                   for _ in range(QUANT_LIXOS_AGUA // 4): 
                        itens_agua.append(Item_agua())

            if evento.type == CRIAR_ITEM_EVENTO_2:
                if progresso <= OBJETIVO / 4:
                    for _ in range(QUANT_LIXOS_TERRA): # Começa em 4 e vai diminuindo por mapa até 1
                        itens_terra.append(Item_terra())
                elif progresso <= OBJETIVO / 2:
                    for _ in range((QUANT_LIXOS_TERRA * 3) // 4): 
                        itens_terra.append(Item_terra())
                elif progresso <= (3 * OBJETIVO) / 4:
                    for _ in range(QUANT_LIXOS_TERRA // 2): 
                        itens_terra.append(Item_terra())
                else:  
                    for _ in range(QUANT_LIXOS_TERRA // 4): 
                        itens_terra.append(Item_terra())
            # Lógica de colisão da rede
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1 and rede_timer == -1:  # Faz uma série de verificações antes de lançar a rede
                pos_mouse = pygame.mouse.get_pos() 
                if pygame.rect.Rect(rede_disponivel).collidepoint(pos_mouse[0],pos_mouse[1]): # Verifica se o clique foi na área disponível para rede
                    rede_circle = [pos_mouse[0], pos_mouse[1]]
                    proporção = abs((abs(jogador_pos[1]) - abs(rede_circle[1]))) - 180 # Variável criada para mudar o tempo da rede dinamicamente, com base na distância
                    rede_timer = int(FPS*2.5+(proporção/6)) # Tempo do ciclo da rede e temporizador
                    tempo_total = rede_timer # Cópia do temporizador para referência de proporcionalidade na rede
                    rede_origem = [jogador2.rect.centerx,jogador2.rect.centery] # Posição de onde a rede vai
                    REDE.blit(imagem_rede,(0,0)) # Coloca a imagem da rede
            # Colisão e coleta do Jogador 1
            for item in itens_terra:
                if jogador1.rect.colliderect(item.rect):
                    if evento.type ==  pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                        jogador1.coletar_item(itens_terra)
                        jogador1.coleta = True
                        break

    #Animação dos personagens:
    if menu.estado == "JOGO":
        jogador1.update_animation()
        if rede_timer != -1:
            jogador2.update_animation(True)
        else:
            jogador2.update_animation()
    # Processa eventos do menu
    menu.eventos(eventos)
    
    # Desenha a tela atual baseada no estado
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
        
        # Atualiza o progresso
        progresso = jogador1.itens_coletados + jogador2.itens_coletados
        
        # Movimentação dos jogadores
        teclas = pygame.key.get_pressed()

        jogador1.mover(teclas, K_w, K_s, K_a, K_d)
        jogador2.mover(teclas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

        # Desenha elementos do jogo
        rio.desenhar()
        # Desenha o background do jogo
        jogo.desenhar_fundo_por_progresso(progresso, OBJETIVO)
    
        for item in itens_agua:
            item.desenhar()
            item.mover() # Movimentação dos itens no rio (água)
        for item in itens_terra:
            item.desenhar()
            item.mover() # Movimentação dos itens na margem (terra)

        # Área onde se pode jogar a rede, define e mostra
        rede_disponivel = [jogador2.rect.centerx-100,jogador2.rect[1]-500,200,350] # Área onde se pode jogar a rede (range da rede)
        range_rede = pygame.surface.Surface((200,350))
        range_rede.fill((COR_RANGE_REDE))
        range_rede.set_alpha(TRANSPARENCIA_RANGE_REDE)

        TELA.blit(range_rede,(jogador2.rect.centerx-100,jogador2.rect[1]-500)) # Mostra essa área na tela

        # Desenhar jogadores
        jogador1.desenhar(TELA)
        jogador2.desenhar(TELA)
        jogador_pos = [jogador2.rect.centerx,jogador2.rect.centery] # Pega a posição atual do jogador quando verifica a rede

        # Desenhar rede
        try:
            if rede_timer > tempo_total/2.3: # Primeiro ciclo da rede
                proporção = abs((abs(jogador_pos[1]) - abs(rede_circle[1]))/(abs(jogador_pos[0]) - abs(rede_circle[0])+0.1)) # Mesma proporção anterior
                rede_timer -= 1 # Diminui um do timer

                # Verificações de posições cartesianas
                if rede_origem[1] > rede_circle[1]:
                    rede_origem[1] -= rede_velocidade*2
                if rede_origem[0] < rede_circle[0]:
                    rede_origem[0] += rede_velocidade/(proporção+0.01)*2
                if rede_origem[0] > rede_circle[0]:
                    rede_origem[0] -= rede_velocidade/(proporção+0.01)*2

                # Verifica se a rede chegou no seu local para coletar o lixo
                if rede_origem[1] - rede_circle[1] < 5:
                    for item in itens_agua:
                        # pos = item.rect[0], item.rect[1]
                        if False not in circle_colide(pos, rede_pos, 40): # Se tiver colisão com algum dos itens
                            pontos_jogada += 1
                            item.rect.x = LARGURA_TELA
                            REDE.blit(item.imagem,(random.randint(0,30),random.randint(0,30))) # Coloca os itens na superfície da rede
                            # teste \/
                            # print(item.imagem)
                rede_pos = rede_origem

            elif rede_timer > 0:
                for item in itens_agua:
                        pos = item.rect[0], item.rect[1]
                        if False not in circle_colide(pos, rede_pos, 40):
                            pontos_jogada += 1
                            REDE.blit(item.imagem,(random.randint(0,40),random.randint(0,40)))
                            item.rect.x = LARGURA_TELA
                rede_timer -= 1

                proporção = abs((abs(jogador_pos[1]) - abs(rede_circle[1]))/(abs(jogador_pos[0]) - abs(rede_circle[0])+0.1))

                # Verificações de posições cartesianas
                if rede_circle[1] < jogador_pos[1]:
                    rede_circle[1] += rede_velocidade
                if rede_circle[1] > jogador_pos[1]:
                    rede_circle[1] -= rede_velocidade
                if rede_circle[0] < jogador_pos[0]:
                    rede_circle[0] += rede_velocidade//(proporção+0.01)
                if rede_circle[0] > jogador_pos[0]:
                    rede_circle[0] -= rede_velocidade//(proporção+0.01)
                # print(rede_circle)
                # print(rede_timer)
                # Atualiza a posição da rede
                rede_pos = rede_circle
            if rede_timer == 3: # Final do ciclo da rede
                if abs(rede_circle[1] - jogador_pos[1]) < 20 and abs(rede_circle[0] - jogador_pos[0]) < 20:
                    jogador2.itens_coletados += pontos_jogada
                    pontos_jogada = 0
                    rede_timer = -1
                else:
                    rede_circle = jogador_pos
                    rede_timer += 1  
        except NameError:
            pass
        try:
            REDE.set_colorkey(CORES["PRETO"])
            TELA.blit(REDE,(rede_pos[0]-50,rede_pos[1]-50))
            if rede_timer == -1:
                REDE.fill(CORES["PRETO"])

        except NameError:
            pass

        # Barra de progresso
        game.Jogo.desenhar_barra_progresso(
            jogo,
            (LARGURA_TELA//2-(LARGURA_BARRA//2)),                     # Posição x na tela
            10,                                                     # Posição y na tela
            LARGURA_BARRA, 
            ALTURA_BARRA,                             # Tamanho da barra (largura e altura)
            progresso
        )
        
        # Exibir pontuação
        TEXTO1 = FONTE_TEXTO_NEGRITO.render(f'Jogador 1:  {jogador1.itens_coletados}', True, CORES["AMARELO"])
        TEXTO2 = FONTE_TEXTO_NEGRITO.render(f'Jogador 2:  {jogador2.itens_coletados}', True, CORES["VERMELHO"])
        TEXTO3 = FONTE_TITULO_PEQUENO_NEGRITO.render(f'OBJETIVO', True, CORES["PRETO"])
        TEXTO_FPS = FONTE_TITULO_PEQUENO_NEGRITO.render(f'FPS: {int(clock.get_fps())}', True, CORES["ROXO"])
        largura_texto2 = TEXTO2.get_width()
        largura_texto3 = TEXTO3.get_width()
        altura_texto_fps = TEXTO_FPS.get_height()
        TELA.blit(TEXTO1, (10, 10))
        TELA.blit(TEXTO2, (LARGURA_TELA-largura_texto2-10, 10))
        TELA.blit(TEXTO3, (LARGURA_TELA//2-(largura_texto3//2), ALTURA_BARRA+10))
        TELA.blit(TEXTO_FPS, (10, ALTURA_TELA-altura_texto_fps - 10))
        
        # Verificador para validar se o objetivo foi alcançado
        if progresso >= OBJETIVO:
            conclusion.Conclusao.tela_vitoria()
            pygame.time.delay(5000)
            menu.estado = "MENU"  # Volta para o menu após a vitória
            if menu.estado == "MENU" and iniciar_jogo() == True:
                menu.estado = "JOGO"

    # Atualiza a tela
    pygame.display.update()

# Finaliza o Pygame
pygame.quit()
sys.exit()

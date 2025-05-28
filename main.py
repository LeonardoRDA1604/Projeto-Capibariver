import pygame, os, sys, random
from pygame.locals import *
from configs import *
from menu import Menu
from entities.players import Jogador
from entities.items import *
from utils import *

# Inicialização do Pygame
pygame.init()

# Inicialização da Música no Pygame
pygame.mixer.init()

# Inicialização da tela do Game
pygame.display.set_caption(NOME_DO_JOGO)

# Inicializar o menu
menu = Menu(TELA)

# try:
#     # Caminho para o som ambiente
#     caminho_som = os.path.join('assets/sounds', 'trilha_sonora_edit7.mp3')  # .ogg, .wav etc.

#     # Carrega e toca o som em loop infinito
#     pygame.mixer.music.load(caminho_som)
#     pygame.mixer.music.set_volume(0.1)  # volume entre 0.0(0%) e 1.0(100%)
#     pygame.mixer.music.play(-1)  # -1 = loop infinito
# except pygame.error as e:
#     print(f"Erro ao carregar trilha sonora: {e}")

# pygame.mixer.music.stop() # to stop

class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()

        # Nomes das pastas com frames animados de cada background do rio
        self.background_folders = [
            'background4_rio-imundo',        # rio imundo
            'background3_rio-muito-sujo',    # rio muito sujo
            'background2_rio-pouco-sujo',    # rio pouco sujo
            'background1_rio-limpo'          # rio limpo
        ]

        # Nomes das pastas com frames animados da margem do rio
        self.margem_folders = [
            'background5_margem-do-rio-fixa',
        ]

        # Carrega os frames animados dos backgrounds
        self.backgrounds = self.carregar_frames_animados(self.background_folders)

        # Carrega os frames animados das margens
        self.margens = self.carregar_frames_animados(self.margem_folders)

        # Controle de animação do rio (não afetado pelo scroll)
        self.rio_frame_index = 0
        self.rio_frame_delay = 1  # milissegundos entre frames #!padrão 150ms e o ideal é 1 / 10 / 100 ou multiplos de 2
        self.ultimo_update_rio = pygame.time.get_ticks()

        # Controle de animação da margem (independente do rio)
        self.margem_frame_index = 0
        self.margem_frame_delay = 1000  # milissegundos entre frames #!padrão 150ms
        self.ultimo_update_margem = pygame.time.get_ticks()

        # Controle de scroll (apenas para backgrounds, não afeta animação)
        self.scroll_x = 0
        self.scroll_speed = VEL_ITEM # velocidade do scroll (pixels por frame) #! +1 + VEL_ITEM  

    def carregar_frames_animados(self, lista_de_pastas):
        animacoes = []
        for folder in lista_de_pastas:
            frames = []
            folder_path = os.path.join('assets/sprites/backgrounds', folder)
            try:
                for file in sorted(os.listdir(folder_path)):
                    if file.endswith(".png") or file.endswith(".jpg"):
                        img_path = os.path.join(folder_path, file)
                        imagem = pygame.image.load(img_path).convert_alpha()
                        imagem = pygame.transform.scale(imagem, (self.largura_tela, self.altura_tela))
                        frames.append(imagem)
            except Exception as e:
                print(f"Erro ao carregar {folder}: {e}")
            animacoes.append(frames)
        return animacoes

    def atualizar_frame_rio(self):
        # Atualiza o frame da animação do rio (independente do scroll)
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update_rio > self.rio_frame_delay:
            max_frames_rio = max((len(f) for f in self.backgrounds if f), default=1)
            self.rio_frame_index = (self.rio_frame_index + 1) % max_frames_rio
            self.ultimo_update_rio = agora

    def atualizar_frame_margem(self):
        # Atualiza o frame da animação da margem (independente do rio)
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update_margem > self.margem_frame_delay:
            max_frames_margem = max((len(f) for f in self.margens if f), default=1)
            self.margem_frame_index = (self.margem_frame_index + 1) % max_frames_margem
            self.ultimo_update_margem = agora

    def atualizar_scroll(self):
        # Atualiza a posição do scroll (independente da animação)
        self.scroll_x += self.scroll_speed
        if self.scroll_x >= self.largura_tela:
            self.scroll_x = 0

    def get_max_frames(self): # Retorna o maior número de frames entre os fundos carregados. (backgrounds e margens)
        max_background = max((len(f) for f in self.backgrounds if f), default=1) # backgrounds
        max_margem = max((len(f) for f in self.margens if f), default=1) # margens
        return max(max_background, max_margem)

    def desenhar_fundo(self, nivel): # Desenha o frame atual do fundo de acordo com o nível.
        if 0 <= nivel < len(self.backgrounds) and self.backgrounds[nivel]:
            frames = self.backgrounds[nivel]
            frame_atual = frames[self.rio_frame_index % len(frames)]
            
            # Desenha o background com scroll (duas vezes para criar loop infinito)
            self.tela.blit(frame_atual, (self.scroll_x, 0))
            self.tela.blit(frame_atual, (self.scroll_x - self.largura_tela, 0))
        else:
            self.tela.fill((0, 0, 0))

        # Desenha margem por cima (fixa, usa sempre o índice 0 para aplicar em todos os backgrounds.)
        # A margem NÃO tem scroll, apenas animação
        if self.margens and self.margens[0]:
            frames_margem = self.margens[0]
            frame_margem = frames_margem[self.margem_frame_index % len(frames_margem)]
            self.tela.blit(frame_margem, (0, 0))

    def desenhar_fundo_por_progresso(self, progresso, objetivo):
        if progresso <= objetivo / 4:
            nivel = 0
        elif progresso <= objetivo / 2:
            nivel = 1
        elif progresso <= (3 * objetivo) / 4:
            nivel = 2
        else:
            nivel = 3

        # Atualiza animação e scroll independentemente
        self.atualizar_frame_rio()
        self.atualizar_frame_margem()
        self.atualizar_scroll()
        self.desenhar_fundo(nivel)

jogo = Jogo(TELA)

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


class Conclusao:
    def __init__(self, tela): # Inicializa o background da tela de conclusão do jogo.     ||       parâmetro tela -> Superfície do pygame onde o menu será desenhado
        self.tela = tela
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()

        # Carregar imagem de fundo
        try:
            self.background = pygame.image.load(os.path.join('assets/sprites/screens', 'tela_conclusao_com_texto_e_logo-fafire.png'))
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
    
    # # Criar jogadores (sem animação)
    # jogador1 = Jogador(300, ALTURA_TELA-100, CORES["AMARELO"])  # Amarelo
    # jogador2 = Jogador(LARGURA_TELA-300, ALTURA_TELA-100, CORES["ROXO"])  # Roxo
    
    #spritesheet path
    spritesheet_path1 = os.path.join('assets/sprites/players', 'Jogador1_spritesheet_movement.png')
    spritesheet_path2 = os.path.join('assets/sprites/players', 'Jogador2_spritesheet_movement.png')
    # Criar jogadores (com animação)
    jogador1 = Jogador(300, ALTURA_TELA-100, CORES["AMARELO"], spritesheet_path1, 1)
    jogador2 = Jogador(LARGURA_TELA-300, ALTURA_TELA-100, CORES["ROXO"], spritesheet_path2, 2)

    # Evento para criar itens (intervalo entre a criação de itens)
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
    superficie_texto = FONTE_TITULO_PEQUENO.render(texto, True, CORES["PRETO"])
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
        Conclusao(TELA).desenhar()
        pygame.display.update()

# todo ---------------------------------------------------------------------------------------------------
def circle_colide(objeto:list, circulo:list, raio):
    # Definir a colisão com a esquerda e direita do circulo
    coli_x_esquerda = objeto[0] >= circulo[0] - raio
    coli_x_direita = objeto[0] <= circulo[0] + raio
    # Se o objeto está entre circulo -30 e circulo + 30
    coli_y_topo = objeto[1] >= circulo[1] - raio
    coli_y_baixo = objeto[1] <= circulo[1] + raio
    colide = [coli_x_esquerda, coli_x_direita, coli_y_topo, coli_y_baixo]
    return colide
# todo --------------------------------------------------------------------------------------------------

# Inicializar o jogo
iniciar_jogo()

clock = pygame.time.Clock()  # criando o relógio antes do loop

# Loop principal
JOGO_RODANDO = True
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
# Variaveis da rede. #todo (passar pro config depois)
rede_timer = -1
rede_chegou = False
rede_origem = [10000,10000]
pontos_jogada = 0
REDE = pygame.surface.Surface((100,100))
imagem_rede = pygame.image.load('assets/sprites/players/Jogador2_object_rede.png')
imagem_rede.set_colorkey((0,0,0))
REDE.blit(imagem_rede,(0,0))
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
while JOGO_RODANDO:
    clock.tick(FPS) # velocidade de atualização da tela ou FPS(Frames por segundo)
    # print(clock.get_fps())
    # Processar eventos
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == QUIT:
            JOGO_RODANDO = False
        # Eventos específicos do jogo
        if menu.estado == "JOGO":
            # Obter o tempo decorrido desde o último frame (em segundos)
            dt = clock.get_time() / 1000.0
            # Atualizar animações
            jogador1.update_animation(dt)
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
            if rede_timer != -1:
                jogador2.update_animation(dt,True)
            else:
                jogador2.update_animation(dt)
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
            # Eventos (criação de items)
            if evento.type == CRIAR_ITEM_EVENTO:
                for _ in range(QUANT_LIXOS_AGUA): # começa em 8 e vai diminuindo por mapa de 2 em 2, até 2?
                    itens_agua.append(Item_agua())
            if evento.type == CRIAR_ITEM_EVENTO_2:
                for _ in range(QUANT_LIXOS_TERRA): # começa em 4 e vai diminuindo por mapa até 1
                    itens_terra.append(Item_terra())
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
            # Logica de colisão da rede
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1 and rede_timer == -1:  #Faz uma série de verificações antes de lançar a rede
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
                pos_mouse = pygame.mouse.get_pos() 
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
                if pygame.rect.Rect(rede_disponivel).collidepoint(pos_mouse[0],pos_mouse[1]): #Verifica se o clique foi na área disponível para rede
                    rede_circle = [pos_mouse[0], pos_mouse[1]]
                    proporção = abs((abs(jogador_pos[1]) - abs(rede_circle[1]))) - 180 #Varíavel criada para mudar o tempo da rede dinamicamente com base na distância
                    rede_timer = int(FPS*2.5+(proporção/6)) #Tempo do ciclo da rede e temporarizador
                    tempo_total = rede_timer #COpia do temporarizador para referência de proporcionalidade na rede
                    rede_origem = [jogador2.rect.centerx,jogador2.rect.centery] #Posição de onde a rede vai
                    REDE.blit(imagem_rede,(0,0)) #Coloca a imaagem da rede
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
            # Colisão e coleta do jogador 1
            for item in itens_terra:
                if jogador1.rect.colliderect(item.rect):
                    if evento.type ==  pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                        jogador1.coletar_item(itens_terra)
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
        jogo.desenhar_fundo_por_progresso(progresso, OBJETIVO)
    
        for item in itens_agua:
            item.desenhar()
            item.mover() # Movimentação dos itens
        for item in itens_terra:
            item.desenhar()
            item.mover() # Movimentação dos itens
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
        # Área onde se pode jogar a rede, define e mostra
        rede_disponivel = [jogador2.rect.centerx-100,jogador2.rect[1]-500,200,350] # area onde se pode jogar a rede (range da rede)
        range_rede = pygame.surface.Surface((200,350))
        range_rede.fill((COR_RANGE_REDE))
        range_rede.set_alpha(TRANSPARENCIA_RANGE_REDE)

        TELA.blit(range_rede,(jogador2.rect.centerx-100,jogador2.rect[1]-500)) # Mostra essa área na tela
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
        # Desenhar jogadores
        jogador1.desenhar(TELA)
        jogador2.desenhar(TELA)

#? ---------------------------------------------------------------------------------------------------------------------------------------- I
        jogador_pos = [jogador2.rect.centerx,jogador2.rect.centery] #Pega a posiçaõ atual do jogador quando verifica a rede

        # Desenhar rede
        try:
            if rede_timer > tempo_total/2.3: #Primeiro ciclo da rede
                proporção = abs((abs(jogador_pos[1]) - abs(rede_circle[1]))/(abs(jogador_pos[0]) - abs(rede_circle[0])+0.1)) #Mesma proporção anterior
                rede_timer -= 1 #Diminiu um do timer

                #Verficações de posições cartesianas
                if rede_origem[1] > rede_circle[1]:
                    rede_origem[1] -= rede_velocidade*2
                if rede_origem[0] < rede_circle[0]:
                    rede_origem[0] += rede_velocidade/(proporção+0.01)*2
                if rede_origem[0] > rede_circle[0]:
                    rede_origem[0] -= rede_velocidade/(proporção+0.01)*2

                #Verifica se a rede chegou no seu local para coletar o lixo
                if rede_origem[1] - rede_circle[1] < 5:
                    for item in itens_agua:
                        pos = item.rect[0], item.rect[1]
                        if False not in circle_colide(pos, rede_pos, 40): #Se tiver colisão com algum dos itens
                            pontos_jogada += 1
                            item.rect.x = LARGURA_TELA
                            REDE.blit(item.imagem,(random.randint(0,80),random.randint(0,80))) #Coloca os itens na superficie da rede
                            # teste \/
                            # print(item.imagem)
                rede_pos = rede_origem

            elif rede_timer > 0:
                for item in itens_agua:
                        pos = item.rect[0], item.rect[1]
                        if False not in circle_colide(pos, rede_pos, 40):
                            pontos_jogada += 1
                            REDE.blit(item.imagem,(random.randint(0,68),random.randint(0,68)))
                            item.rect.x = LARGURA_TELA
                rede_timer -= 1

                proporção = abs((abs(jogador_pos[1]) - abs(rede_circle[1]))/(abs(jogador_pos[0]) - abs(rede_circle[0])+0.1))

                #Verficações de posições cartesianas
                if rede_circle[1] < jogador_pos[1]:
                    rede_circle[1] += rede_velocidade
                if rede_circle[1] > jogador_pos[1]:
                    rede_circle[1] -= rede_velocidade
                if rede_circle[0] < jogador_pos[0]:
                    rede_circle[0] += rede_velocidade/(proporção+0.01)
                if rede_circle[0] > jogador_pos[0]:
                    rede_circle[0] -= rede_velocidade/(proporção+0.01)

                #Atualiza a posilção da rede
                rede_pos = rede_circle
            if rede_timer == 0: #Final do ciclo da rede
                if abs(rede_circle[1] - jogador_pos[1]) < 20 and abs(rede_circle[0] - jogador_pos[0]) < 20:
                    jogador2.itens_coletados += pontos_jogada
                    pontos_jogada = 0
                    rede_timer = -1
                else:
                    rede_timer += 10
        except NameError:
            pass
        try: #TODO (?)
            REDE.set_colorkey((0,0,0))
            TELA.blit(REDE,(rede_pos[0]-50,rede_pos[1]-50))
            if rede_timer == -1:
                REDE.fill((0,0,0))

        except NameError:
            pass
#? ---------------------------------------------------------------------------------------------------------------------------------------- F

        # Barra de progresso
        desenhar_barra_progresso(
            TELA,
            LARGURA_TELA//2-(LARGURA_BARRA//2),                     # Posição x na tela
            10,                                                     # Posição y na tela
            LARGURA_BARRA, ALTURA_BARRA                             # Tamanho da barra (largura e altura)
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
        
        # # Verificador para validar se o objetivo foi alcançado
        if progresso >= OBJETIVO:
            tela_vitoria()
            menu.estado = "MENU"  # Volta para o menu após a vitória
            if menu.estado == "MENU" and iniciar_jogo() == True:
                menu.estado = "JOGO"
            # elif teclas[K_ESC] == (JOGO_RODANDO == False)
            # -------------------------------------------------------------------------------------------------------------------------
            # -------------------------------------------------------------------------------------------------------------------------
    
    # Atualizar a tela
    pygame.display.update()

# Finaliza o Pygame
pygame.quit()
sys.exit()

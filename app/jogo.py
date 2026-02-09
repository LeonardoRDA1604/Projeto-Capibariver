from utils import *
import os

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
        self.rio_frame_delay = 1  # Milissegundos entre frames #!padrão 150ms e o ideal é 1 / 10 / 100 ou múltiplos de 2
        self.ultimo_update_rio = pygame.time.get_ticks()

        # Controle de animação da margem (independente do rio)
        self.margem_frame_index = 0
        self.margem_frame_delay = 1000 # Milissegundos entre frames #!padrão 150ms
        self.ultimo_update_margem = pygame.time.get_ticks()

        # Controle de scroll (apenas para backgrounds, não afeta animação)
        self.scroll_x = 0
        self.scroll_speed = VEL_ITEM # Velocidade do scroll (pixels por frame) #! +1 + VEL_ITEM  

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

    def get_max_frames(self): # Retorna o maior número de frames entre os fundos carregados (backgrounds e margens)
        max_background = max((len(f) for f in self.backgrounds if f), default=1) # Backgrounds
        max_margem = max((len(f) for f in self.margens if f), default=1) # Margens
        return max(max_background, max_margem)

    def desenhar_fundo(self, nivel): # Desenha o frame atual do fundo de acordo com o nível
        if 0 <= nivel < len(self.backgrounds) and self.backgrounds[nivel]:
            frames = self.backgrounds[nivel]
            frame_atual = frames[self.rio_frame_index % len(frames)]
            
            # Desenha o background com scroll (duas vezes para criar loop infinito)
            self.tela.blit(frame_atual, (self.scroll_x, 0))
            self.tela.blit(frame_atual, (self.scroll_x - self.largura_tela, 0))
        else:
            self.tela.fill(CORES["PRETO"])

        # Desenha margem por cima (fixa, usa sempre o índice 0 para aplicar em todos os backgrounds)
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

import pygame, os, sys
from assets.utils.configs import *

class Conclusao:
    def __init__(self, tela): # Inicializa o background da tela de conclusão do jogo.     ||       parâmetro tela -> Superfície do pygame onde o menu será desenhado
        self.tela = tela
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()

        # Carrega imagem de fundo
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
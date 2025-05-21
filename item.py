import pygame
import random
from configs import *

# Classes Item (Água e Terra)
class Item_agua:
    def __init__(self):
        y_positions = list(range(ALTURA_TELA - 350, ALTURA_TELA - 750, -50)) # Posições y dos objetos do rio
                    # [ALTURA_TELA - 350, ALTURA_TELA - 400, ALTURA_TELA - 450, ALTURA_TELA - 500, ALTURA_TELA - 550, ALTURA_TELA - 600, ALTURA_TELA - 650, ALTURA_TELA - 700, ALTURA_TELA - 750]
        # Lista de imagens disponíveis para os itens de água
        self.imagens = [
                    pygame.image.load('./assets/sprites/items/Objeto1_lata-de-cerveja.png'),
                    pygame.image.load('./assets/sprites/items/Objeto2_lata-coca-cola.png'),
                    pygame.image.load('./assets/sprites/items/Objeto3_lata-sardinha.png'),
                    pygame.image.load('./assets/sprites/items/Objeto4_lata-atum.png'),
                    pygame.image.load('./assets/sprites/items/Objeto6_all-star-preto.png'),
                    pygame.image.load('./assets/sprites/items/Objeto7_all-star-vermelho.png'),
                    pygame.image.load('./assets/sprites/items/Objeto8_embalagem-laranja.png'),
                    pygame.image.load('./assets/sprites/items/Objeto9_embalagem-azul.png'),
                    pygame.image.load('./assets/sprites/items/Objeto10_sacola.png'),
                    pygame.image.load('./assets/sprites/items/Objeto11_lixo-preto.png'),
                    pygame.image.load('./assets/sprites/items/Objeto12_lixo-azul.png'),
                    pygame.image.load('./assets/sprites/items/Objeto13_lixo-verde.png'),
                    pygame.image.load('./assets/sprites/items/Objeto14_água-sanitária.png'),
                    pygame.image.load('./assets/sprites/items/Objeto15_amaciante.png'),
                    pygame.image.load('./assets/sprites/items/Objeto16_garrafa-de-água.png'),
                    pygame.image.load('./assets/sprites/items/Objeto17_galão-de-água.png'),
                ]
        # Escolher uma imagem aleatória da lista
        self.imagem = random.choice(self.imagens)
        # Redimensionar a imagem para o tamanho do item (opcional)
        self.imagem = pygame.transform.scale(self.imagem, TAMANHO_ITEM)
        # self.rect = pygame.Rect(random.randint(-100, -50), random.choice(y_positions), TAMANHO_ITEM[0], TAMANHO_ITEM[1])
        # Criar o retângulo baseado na imagem
        self.rect = self.imagem.get_rect()
        self.rect.x = random.randint(-100, -50)
        self.rect.y = random.choice(y_positions)
        # Manter a cor se a imagem não carregar
        self.cor = CORES["LARANJA"]

    def mover(self):
        self.rect.x += VEL_ITEM

    # def desenhar(self):
    #     pygame.draw.rect(TELA, self.cor, self.rect)
    def desenhar(self):
        try:
            # Tentar desenhar a imagem
            TELA.blit(self.imagem, self.rect)
        except:
            # Fallback para o retângulo colorido se a imagem falhar
            pygame.draw.rect(TELA, self.cor, self.rect)

class Item_terra:
    def __init__(self):
        x1_margem = 5*(LARGURA_TELA//40) # antes era 0
        x2_margem = 37*(LARGURA_TELA//40) - TAMANHO_ITEM[0] # antes era LARGURA_TELA - TAMANHO_ITEM[0]
        y1_margem = 2*(ALTURA_TELA//3)
        y2_margem = ALTURA_TELA-ALTURA_TELA//20-TAMANHO_ITEM[1]
# Lista de imagens disponíveis para os itens da terra
        self.imagens = [
                    pygame.image.load('./assets/sprites/items/Objeto1_lata-de-cerveja.png'),
                    pygame.image.load('./assets/sprites/items/Objeto2_lata-coca-cola.png'),
                    pygame.image.load('./assets/sprites/items/Objeto3_lata-sardinha.png'),
                    pygame.image.load('./assets/sprites/items/Objeto4_lata-atum.png'),
                    pygame.image.load('./assets/sprites/items/Objeto5_pneu.png'),
                    pygame.image.load('./assets/sprites/items/Objeto6_all-star-preto.png'),
                    pygame.image.load('./assets/sprites/items/Objeto7_all-star-vermelho.png'),
                    pygame.image.load('./assets/sprites/items/Objeto8_embalagem-laranja.png'),
                    pygame.image.load('./assets/sprites/items/Objeto9_embalagem-azul.png'),
                    pygame.image.load('./assets/sprites/items/Objeto10_sacola.png'),
                    pygame.image.load('./assets/sprites/items/Objeto11_lixo-preto.png'),
                    pygame.image.load('./assets/sprites/items/Objeto12_lixo-azul.png'),
                    pygame.image.load('./assets/sprites/items/Objeto13_lixo-verde.png'),
                    pygame.image.load('./assets/sprites/items/Objeto14_água-sanitária.png'),
                    pygame.image.load('./assets/sprites/items/Objeto15_amaciante.png'),
                    pygame.image.load('./assets/sprites/items/Objeto16_garrafa-de-água.png'),
                    pygame.image.load('./assets/sprites/items/Objeto17_galão-de-água.png'),
                    pygame.image.load('./assets/sprites/items/Objeto18_coco.png'),
        ]
        # Escolher uma imagem aleatória da lista
        self.imagem = random.choice(self.imagens)
        self.imagem = pygame.transform.scale(self.imagem, TAMANHO_ITEM)
        # Criar o retângulo baseado na imagem
        self.rect = self.imagem.get_rect()
        self.rect.x = random.randint(x1_margem, x2_margem)
        self.rect.y = random.randint(y1_margem, y2_margem)
        # self.rect = pygame.Rect(random.randint(x1_margem, x2_margem), random.randint(y1_margem, y2_margem), TAMANHO_ITEM[0], TAMANHO_ITEM[1]) # parametros (x(x1, x2), y(y1, y2), TAMANHO_ITEM, TAMANHO_ITEM)
        # Manter a cor se a imagem não carregar
        self.cor = CORES["VERMELHO"]

    def mover(self):
        pass

    # def desenhar(self):
    #     pygame.draw.rect(TELA, self.cor, self.rect)
    def desenhar(self):
        try:
            # Tentar desenhar a imagem
            TELA.blit(self.imagem, self.rect)
        except:
            # Fallback para o retângulo colorido se a imagem falhar
            pygame.draw.rect(TELA, self.cor, self.rect)
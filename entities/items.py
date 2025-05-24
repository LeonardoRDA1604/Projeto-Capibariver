import pygame
import random
from configs import *

# Classes Item (Água e Terra)
class Item_agua:
    def __init__(self):
        y_positions = list(range(ALTURA_TELA - 350, ALTURA_TELA - 750, -50)) # Posições y dos objetos do rio
                    # [ALTURA_TELA - 350, ALTURA_TELA - 400, ALTURA_TELA - 450, ALTURA_TELA - 500, ALTURA_TELA - 550, ALTURA_TELA - 600, ALTURA_TELA - 650, ALTURA_TELA - 700, ALTURA_TELA - 750]
        # Lista de imagens disponíveis para os itens de água (coco e pneu não entram nessa lista pois não boiam)
        self.imagens = [
                    pygame.image.load('./assets/sprites/items/type1-lata-alimento_atum.png'), # Objeto 1
                    pygame.image.load('./assets/sprites/items/type1-lata-alimento_sardinha.png'), # Objeto 2
                    pygame.image.load('./assets/sprites/items/type2-lata-bebida_cerveja.png'), # Objeto 3
                    pygame.image.load('./assets/sprites/items/type2-lata-bebida_coca-cola.png'), # Objeto 4
                    pygame.image.load('./assets/sprites/items/type2-lata-bebida_fanta.png'), # Objeto 5
                    pygame.image.load('./assets/sprites/items/type3-tenis_all-star-preto.png'), # Objeto 6
                    pygame.image.load('./assets/sprites/items/type3-tenis_all-star-vermelho.png'), # Objeto 7
                    pygame.image.load('./assets/sprites/items/type4-embalagem_azul.png'), # Objeto 8
                    pygame.image.load('./assets/sprites/items/type4-embalagem_laranja.png'), # Objeto 9
                    pygame.image.load('./assets/sprites/items/type5-sacola_branca.png'), # Objeto 10
                    pygame.image.load('./assets/sprites/items/type5-sacola_verde-claro.png'), # Objeto 11
                    pygame.image.load('./assets/sprites/items/type6-lixo_azul.png'), # Objeto 12
                    pygame.image.load('./assets/sprites/items/type6-lixo_preto1.png'), # Objeto 13
                    pygame.image.load('./assets/sprites/items/type6-lixo_preto2.png'), # Objeto 14
                    pygame.image.load('./assets/sprites/items/type6-lixo_verde-claro.png'), # Objeto 15
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_agua.png'), # Objeto 16
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_guarana.png'), # Objeto 17
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_agua-sanitaria.png'), # Objeto 18
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_amaciante.png'), # Objeto 19
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_galao-de-agua.png'), # Objeto 20
                    pygame.image.load('./assets/sprites/items/type8-garrafa-vidro_verde.png'), # Objeto 21
                    pygame.image.load('./assets/sprites/items/type9-outros_caixa-de-leite.png'), # Objeto 24
                    pygame.image.load('./assets/sprites/items/type9-outros_oculos.png'), # Objeto 25
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
                    pygame.image.load('./assets/sprites/items/type1-lata-alimento_atum.png'), # Objeto 1
                    pygame.image.load('./assets/sprites/items/type1-lata-alimento_sardinha.png'), # Objeto 2
                    pygame.image.load('./assets/sprites/items/type2-lata-bebida_cerveja.png'), # Objeto 3
                    pygame.image.load('./assets/sprites/items/type2-lata-bebida_coca-cola.png'), # Objeto 4
                    pygame.image.load('./assets/sprites/items/type2-lata-bebida_fanta.png'), # Objeto 5
                    pygame.image.load('./assets/sprites/items/type3-tenis_all-star-preto.png'), # Objeto 6
                    pygame.image.load('./assets/sprites/items/type3-tenis_all-star-vermelho.png'), # Objeto 7
                    pygame.image.load('./assets/sprites/items/type4-embalagem_azul.png'), # Objeto 8
                    pygame.image.load('./assets/sprites/items/type4-embalagem_laranja.png'), # Objeto 9
                    pygame.image.load('./assets/sprites/items/type5-sacola_branca.png'), # Objeto 10
                    pygame.image.load('./assets/sprites/items/type5-sacola_verde-claro.png'), # Objeto 11
                    pygame.image.load('./assets/sprites/items/type6-lixo_azul.png'), # Objeto 12
                    pygame.image.load('./assets/sprites/items/type6-lixo_preto1.png'), # Objeto 13
                    pygame.image.load('./assets/sprites/items/type6-lixo_preto2.png'), # Objeto 14
                    pygame.image.load('./assets/sprites/items/type6-lixo_verde-claro.png'), # Objeto 15
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_agua.png'), # Objeto 16
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_guarana.png'), # Objeto 17
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_agua-sanitaria.png'), # Objeto 18
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_amaciante.png'), # Objeto 19
                    pygame.image.load('./assets/sprites/items/type7-garrafa-plastica_galao-de-agua.png'), # Objeto 20
                    pygame.image.load('./assets/sprites/items/type8-garrafa-vidro_verde.png'), # Objeto 21
                    pygame.image.load('./assets/sprites/items/type9-outros_coco-verde-com-canudo.png'), # Objeto 22
                    pygame.image.load('./assets/sprites/items/type9-outros_pneu.png'), # Objeto 23
                    pygame.image.load('./assets/sprites/items/type9-outros_caixa-de-leite.png'), # Objeto 24
                    pygame.image.load('./assets/sprites/items/type9-outros_oculos.png'), # Objeto 25
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
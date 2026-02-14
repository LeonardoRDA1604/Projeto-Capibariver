import pygame, random
from assets.utils.configs import *
from entities.players import *
class Net: 
    def __init__(self, itens_agua : list, jogador2 : Jogador):
        # Variáveis da rede.
        self.rede_timer = -1 
        self.rede_chegou = False
        self.rede_origem = [10000,10000]
        self.pontos_jogada = 0
        self.REDE = pygame.surface.Surface((100,100))
        self.imagem_rede = pygame.image.load('assets/sprites/players/Jogador2_object_rede.png')
        self.imagem_rede.set_colorkey((0,0,0))
        self.REDE.blit(self.imagem_rede,(0,0))

        self.proporcao = 0
        self.rede_disponivel = [jogador2.rect.centerx-100,jogador2.rect[1]-500,200,350]
        self.jogador2 = jogador2
        self.itens_agua = itens_agua
        self.tempo_total = 0
        self.jogador_pos = [jogador2.rect.centerx,jogador2.rect.centery] # Pega a posição atual do jogador quando verifica a rede
        self.rede_circle = list


    def launch_area(self):
        jogador2 = self.jogador2
        # Área onde se pode jogar a rede, define e mostra
        range_rede = pygame.surface.Surface((200,350))
        range_rede.fill((COR_RANGE_REDE))
        range_rede.set_alpha(TRANSPARENCIA_RANGE_REDE)
        TELA.blit(range_rede,(jogador2.rect.centerx-100,jogador2.rect[1]-500)) # Mostra essa área na tela
        
    def net_end_cicle(self, itens_agua : list, rede_pos):
        for item in itens_agua:
            pos = item.rect[0], item.rect[1]
            if False not in self._circle_colide(pos, rede_pos, 40): # Se tiver colisão com algum dos itens
                pontos_jogada += 1
                item.rect.x = LARGURA_TELA
                self.REDE.blit(item.imagem,(random.randint(0,40),random.randint(0,40))) # Coloca os itens na superfície da rede
        
        
    def verificador_posicao_cartesiana_primeiro_ciclo(self, rede_circle : list, rede_origem : list, proporcao):
        if rede_origem[1] > rede_circle[1]:
            rede_origem[1] -= rede_velocidade*2
        if rede_origem[0] < rede_circle[0]:
            rede_origem[0] += rede_velocidade/(proporcao+0.01)*2
        if rede_origem[0] > rede_circle[0]:
            rede_origem[0] -= rede_velocidade/(proporcao+0.01)*2
    
    def verificador_posicao_cartesiana_segundo_ciclo(self, proporcao, jogador_pos : list,  rede_circle : list):    
        if rede_circle[1] < jogador_pos[1]:
            rede_circle[1] += rede_velocidade
        if rede_circle[1] > jogador_pos[1]:
            rede_circle[1] -= rede_velocidade
        if rede_circle[0] < jogador_pos[0]:
            rede_circle[0] += rede_velocidade//(proporcao+0.01)
        if rede_circle[0] > jogador_pos[0]:
            rede_circle[0] -= rede_velocidade//(proporcao+0.01)
            
    def _circle_colide(self, objeto:list, circulo:list, raio):
        # Define a colisão com a esquerda e direita do circulo
        coli_x_esquerda = objeto[0] >= circulo[0] - raio
        coli_x_direita = objeto[0] <= circulo[0] + raio
        # Se o objeto está entre círculo -30 e círculo + 30
        coli_y_topo = objeto[1] >= circulo[1] - raio
        coli_y_baixo = objeto[1] <= circulo[1] + raio
        colide = [coli_x_esquerda, coli_x_direita, coli_y_topo, coli_y_baixo]
        return colide
import pygame
from assets.utils.configs import *
from entities.players import *
class Net: 
    def __init__(self):
        pass

    def launch_area(self, jogador2 : Jogador):
        # Área onde se pode jogar a rede, define e mostra
        range_rede = pygame.surface.Surface((200,350))
        range_rede.fill((COR_RANGE_REDE))
        range_rede.set_alpha(TRANSPARENCIA_RANGE_REDE)
        return TELA.blit(range_rede,(jogador2.rect.centerx-100,jogador2.rect[1]-500)) # Mostra essa área na tela
        
    def verificador_posicao_cartesiana_primeiro_ciclo(self, rede_circle : list, rede_origem : list, proporcao):
        if rede_origem[1] > rede_circle[1]:
            rede_origem[1] -= rede_velocidade*2
        if rede_origem[0] < rede_circle[0]:
            rede_origem[0] += rede_velocidade/(proporcao+0.01)*2
        if rede_origem[0] > rede_circle[0]:
            rede_origem[0] -= rede_velocidade/(proporcao+0.01)*2
        return rede_origem
    
    def verificador_posicao_cartesiana_segundo_ciclo(self, proporcao, jogador_pos : list,  rede_circle : list):    
        if rede_circle[1] < jogador_pos[1]:
            rede_circle[1] += rede_velocidade
        if rede_circle[1] > jogador_pos[1]:
            rede_circle[1] -= rede_velocidade
        if rede_circle[0] < jogador_pos[0]:
            rede_circle[0] += rede_velocidade//(proporcao+0.01)
        if rede_circle[0] > jogador_pos[0]:
            rede_circle[0] -= rede_velocidade//(proporcao+0.01)
        return rede_circle
            
    def circle_colide(self, objeto:list, circulo:list, raio):
        # Define a colisão com a esquerda e direita do circulo
        coli_x_esquerda = objeto[0] >= circulo[0] - raio
        coli_x_direita = objeto[0] <= circulo[0] + raio
        # Se o objeto está entre círculo -30 e círculo + 30
        coli_y_topo = objeto[1] >= circulo[1] - raio
        coli_y_baixo = objeto[1] <= circulo[1] + raio
        colide = [coli_x_esquerda, coli_x_direita, coli_y_topo, coli_y_baixo]
        return colide
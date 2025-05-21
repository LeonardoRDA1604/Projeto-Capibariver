import pygame
import os
from sprite_manager import SpriteSheet
from configs import *

# Classe dos jogadores
class Jogador:
    def __init__(self, x, y, cor, spritesheet_path=None, player_num=1):
        # Manter atributos originais para compatibilidade
        self.rect = pygame.Rect(x, y, TAMANHO_JOGADOR[0], TAMANHO_JOGADOR[1])  # Tamanho do sprite
        self.cor = cor
        self.itens_coletados = 0 # Contador de itens coletados
        self.rede = None
        self.player_num = player_num  # 1 para jogador 1, 2 para jogador 2
        
        # Atributos para animação
        self.direction = "down"  # Direção padrão (baixo, cima, esquerda, direita)
        self.animation_frame = 0
        self.animation_speed = 0.10  # Velocidade da animação (quanto menor, mais rápido)
        self.animation_timer = 0
        self.is_moving = False
        
        # Carregar o spritesheet
        if spritesheet_path and os.path.exists(spritesheet_path):
            self.spritesheet = SpriteSheet(spritesheet_path)
            # Recortar o spritesheet (16 sprites: 4 linhas, 4 colunas)
            # Cada sprite é dividido em 4 linhas (direções) e 4 colunas (frames de animação)
            self.sprites = self.spritesheet.get_sprites(
                width=64,   # Largura de cada sprite (ajuste conforme necessário)
                height=64,  # Altura de cada sprite (ajuste conforme necessário)
                rows=4,     # 4 linhas (down, left, right, up)
                cols=4      # 4 frames de animação para cada direção
            )
            
            # Redimensionar para o tamanho do jogador
            self.scale_sprites()
        else:
            self.sprites = None
            print(f"Spritesheet não encontrado: {spritesheet_path}")
    
    def scale_sprites(self): # Redimensiona todos os sprites para o tamanho correto do jogador
        if self.sprites:
            for i in range(len(self.sprites)):
                for j in range(len(self.sprites[i])):
                    self.sprites[i][j] = pygame.transform.scale(
                        self.sprites[i][j], 
                        (self.rect.width, self.rect.height)
                    )
    
    def update_animation(self, dt): # Atualiza o frame da animação com base no tempo decorrido.
        if not self.is_moving:
            # Se não estiver se movendo, usar o primeiro frame (posição padrão)
            self.animation_frame = 0
            return
            
        # Incrementar o timer
        self.animation_timer += dt
        
        # Se passou tempo suficiente, avançar para o próximo frame
        if self.animation_timer >= self.animation_speed:
            self.animation_frame = (self.animation_frame + 1) % 4  # Ciclo entre os 4 frames
            self.animation_timer = 0  # Resetar o timer
    
    def desenhar(self, tela): # Desenha o jogador com sprite ou retângulo colorido como fallback
        if self.sprites:
            # Selecionar a linha correta baseada na direção
            direction_index = self.get_direction_index()
            
            # Desenhar o sprite correto (linha = direção, coluna = frame)
            tela.blit(self.sprites[direction_index][self.animation_frame], self.rect)
        else:
            # Fallback para o retângulo colorido se não houver sprites
            pygame.draw.rect(tela, self.cor, self.rect)
    
    def get_direction_index(self): #Retorna o índice da linha correspondente à direção atual.
        if self.direction == "down":
            return 0
        elif self.direction == "up":
            return 1
        elif self.direction == "left":
            return 2
        elif self.direction == "right":
            return 3
        return 0  # Padrão: para baixo
    
    def mover(self, teclas, cima, baixo, esquerda, direita): # Move o jogador e atualiza a direção baseada nas teclas pressionadas.
        self.is_moving = False  # Assume que o jogador não está se movendo
        moveu_x = False
        moveu_y = False
        
        # Verifica movimentos e atualiza direção
        if teclas[cima] and self.rect.top > 2*(ALTURA_TELA/3):
            self.rect.y -= VEL_JOGADOR
            self.direction = "up"
            self.is_moving = True
            moveu_y = True
            
        if teclas[baixo] and self.rect.bottom < ALTURA_TELA-ALTURA_TELA//20: #!!!!!!!!!!!!!
            self.rect.y += VEL_JOGADOR
            self.direction = "down"
            self.is_moving = True
            moveu_y = True
            
        if teclas[esquerda] and self.rect.left > 5*(LARGURA_TELA//40): #!!!!!!!!!!!!!
            self.rect.x -= VEL_JOGADOR
            self.direction = "left"
            self.is_moving = True
            moveu_x = True
            
        if teclas[direita] and self.rect.right < 37*(LARGURA_TELA//40): #!!!!!!!!!!!!!
            self.rect.x += VEL_JOGADOR
            self.direction = "right"
            self.is_moving = True
            moveu_x = True
            
        # Evitar que a direção mude quando se pressiona teclas opostas simultaneamente
        if moveu_x and moveu_y:
            # Priorizar o último movimento
            if teclas[direita]:
                self.direction = "right"
            elif teclas[esquerda]:
                self.direction = "left"
            elif teclas[baixo]:
                self.direction = "down"
            elif teclas[cima]:
                self.direction = "up"
    
    # Métodos da classe original que devem ser preservados
    # def coletar_item(self): # Implementação do método original de coleta.
    #     # Coletar item diretamente abaixo do jogador 1
    #     for item in itens_terra:
    #         if self.rect.colliderect(item.rect):
    #             self.itens_coletados += 1
    #             itens_terra.remove(item)  # Remove o item da lista
    #             break
        
    def coletar_item(self, itens_lista): # Implementação do método original de coleta.
        # Coletar item diretamente abaixo do jogador 1
        for item in itens_lista:
            if self.rect.colliderect(item.rect):
                self.itens_coletados += 1
                itens_lista.remove(item)  # Remove o item da lista
                return True
        return False
        
    def lançar_rede(self): # Implementação do método de lançar a rede.
        self.pos_mouse = pygame.mouse.get_pos()
        self.rede_rect = pygame.Rect(300, 200, 30, 30)
        self.rede = pygame.Rect(self.rect[0] - 15, self.rect.centery - 15, 30, 30)
        self.rede.center = self.pos_mouse
            
    def desenhar_rede(self, tela): # Implementação do método de desenhar a rede.
        if self.rede:
            pygame.draw.circle(tela, (255, 255, 255), self.rede.center, 30)  # CORES["BRANCO"]


    
# # todo ---------------------------------------------------------------------------------------------------
#     def lançar_rede(self):
#         # Verifica se o jogador 2 clicou e cria a rede
#         self.pos_mouse = pygame.mouse.get_pos()
#         self.rede_rect = pygame.Rect(300,200,30,30)
#         self.rede = pygame.Rect(self.rect[0] - 15, self.rect.centery - 15, 30, 30)
#         self.rede.center = self.pos_mouse
            
#     def desenhar_rede(self):
#         if self.rede:
#             pygame.draw.circle(TELA, CORES["BRANCO"], self.rede.center, 30)
    
#     def limit_range(pos_rede , pos_player2):    
#         pos_player2 = jogador2.rect.topleft
#         pos_rede = pygame.rect(pos_player2[0], pos_player2[1] - (ALTURA_TELA//6), pos_player2[0]+ 100, pos_player2[1] - 100)
    
#     def hitbox_rede():
        
#         pos_player2 = jogador2.rect.topleft
#         pos_mouse = pygame.mouse.get_pos()
#         pygame.rect(pos_player2[0], pos_player2[1], pos_player2[0], pos_player2[1])
#         Dist_rede_player = abs((pos_mouse[1] - pos_player2[1])**1/2) + abs((pos_player2[0] - pos_mouse[0])**1/2 )
#         print(Dist_rede_player)
    


#     # def limit_range(self):
#     #     self.pos_player = self.rect
#     #     #delimitar a área de criação da rede de acordo com a posição do player
#     #     # pegar posição do jogador
#     #     # criar retângulo que pegue a largura do player e a altura de metade da tela , a partir da posição do player
#     #     self.pos_rede = pygame.rect(self.pos_player[0], self.pos_player[1], self.pos_player[0]+ 30, self.pos_player[1] - 100)
# # todo ---------------------------------------------------------------------------------------------------


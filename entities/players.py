import pygame, os
from sprite_manager import SpriteSheet
from configs import *

# Classe dos jogadores
class Jogador:
    def __init__(self, x, y, cor, spritesheet_path=None, player_num=1):
        # Manter atributos originais para compatibilidade
        self.rect = pygame.Rect(x, y, TAMANHO_JOGADOR[0], TAMANHO_JOGADOR[1])  # Tamanho do sprite
        self.cor = cor
        self.itens_coletados = 0 # Contador de itens coletados
        self.rede = pygame.Rect(300, 200, 30, 30)   
        self.player_num = player_num  # 1 para jogador 1, 2 para jogador 2
        
        # Atributos para animação
        self.direction = "down"  # Direção padrão (baixo, cima, esquerda, direita)
        self.animation_frame = 0
        self.animation_speed = 0.05  # Velocidade mais rápida (50ms por frame)
        self.animation_timer = 0
        self.is_moving = False
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
        # Index da rede
        self.redeindex = 0
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
        # Para evitar movimento diagonal
        self.last_direction_pressed = None
        
        # Carregar o spritesheet
        self.redesprites = pygame.image.load('assets/sprites/players/Jogador2_spritesheet_action_without_net.png')
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
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
            # Ler a spritesheet
            self.redespritesheet = SpriteSheet('assets/sprites/players/Jogador2_spritesheet_action_without_net.png')
            # Pra deixar os 3 sprites em uma unica lista
            # self.spritesrede = self.redespritesheet.get_sprites(64,128,2,2)
            # # teste \/
            # # print(self.spritesrede)
            # self.spritesrede[0].append(self.spritesrede[1][0])
            # self.spritesrede.pop()
            # self.spritesrede = self.spritesrede[0]


            self.spritesrede = self.redespritesheet.get_sprites(64, 64, 3, 2)  # 3 linhas, 2 colunas

            # Agora transformar a matriz em lista linear dos 5 sprites
            sprites_temp = []
            for linha in self.spritesrede:
                for sprite in linha:
                    sprites_temp.append(sprite)

            # Pegar apenas os 5 primeiros (caso tenha 6 posições mas só 5 sprites)
            self.spritesrede = sprites_temp[:5]


#? ---------------------------------------------------------------------------------------------------------------------------------------- F
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
    
    def update_animation(self, dt,rede=False): # Atualiza o frame da animação com base no tempo decorrido.
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
        self.rede = rede
        if rede == False:
            # self.redeindex == 0
            self.redeindex = 0
            # teste \/
            # print(f'{self.redeindex = }')
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
        if not self.is_moving:
            # Se não estiver se movendo, usar o primeiro frame (posição padrão)
            self.animation_frame = 0
            self.animation_timer = 0  # resetar timer quando parar
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
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
            # teste \/
            # print(f'{self.redeindex//10 = }')
            if self.rede:
                #TODO ajustar o reset da animação
                # tela.blit(self.spritesrede[self.redeindex//10],self.rect)
                # self.redeindex = (min(self.redeindex + 1,20))

                # tela.blit(self.spritesrede[self.redeindex//8],self.rect)  # //8 em vez de //10
                # self.redeindex = (self.redeindex + 1) % 40 # 39 em vez de 20 (5 sprites * 8 = 40 frames)
                frame_atual = min(self.redeindex//3, 4)  # Garante que não passe do sprite 4
                tela.blit(self.spritesrede[frame_atual], self.rect)
                if self.redeindex < 14:  # Só incrementa se não chegou no final
                    self.redeindex += 1

            else:
                tela.blit(self.sprites[direction_index][self.animation_frame], self.rect)
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
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
    
    def mover(self, teclas, cima, baixo, esquerda, direita): # Move o jogador e atualiza a direção
        # Resetar estado de movimento
        self.is_moving = False
        
        # Verificar quais teclas estão pressionadas
        movimentos_ativos = []
        
        if teclas[cima] and self.rect.top > 2*(ALTURA_TELA/3):
            movimentos_ativos.append("up")
        
        if teclas[baixo] and self.rect.bottom < ALTURA_TELA-ALTURA_TELA//20:
            movimentos_ativos.append("down")
        
        if teclas[esquerda] and self.rect.left > 5*(LARGURA_TELA//40):
            movimentos_ativos.append("left")
        
        if teclas[direita] and self.rect.right < 37*(LARGURA_TELA//40):
            movimentos_ativos.append("right")
        
        # Se não há movimento, sair
        if not movimentos_ativos:
            self.last_direction_pressed = None
            return
        
        # Se há apenas um movimento, aplicar diretamente
        if len(movimentos_ativos) == 1:
            direction = movimentos_ativos[0]
            self.last_direction_pressed = direction
        else:
            # Evitar movimento diagonal - usar última direção ou primeira disponível
            direction = None
            
            # Verificar se a última direção pressionada ainda está ativa
            if self.last_direction_pressed in movimentos_ativos:
                direction = self.last_direction_pressed
            else:
                # Usar a primeira direção da lista (ordem de prioridade)
                direction = movimentos_ativos[0]
                self.last_direction_pressed = direction
        
        # Aplicar o movimento na direção escolhida
        self.is_moving = True
        self.direction = direction
        
        if direction == "up":
            self.rect.y -= VEL_JOGADOR
        elif direction == "down":
            self.rect.y += VEL_JOGADOR
        elif direction == "left":
            self.rect.x -= VEL_JOGADOR
        elif direction == "right":
            self.rect.x += VEL_JOGADOR
    
    # Métodos da classe original que devem ser preservados
    def coletar_item(self, itens_lista): # Implementação do método original de coleta.
        # Coletar item diretamente abaixo do jogador 1
        for item in itens_lista:
            if self.rect.colliderect(item.rect):
                self.itens_coletados += 1
                itens_lista.remove(item)  # Remove o item da lista
                return True
        return False
    
# #todo ---------------------------------------------------------------------------------------------------------------------
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! mudar
    def lançar_rede(self): # Implementação do método de lançar a rede.
        self.pos_mouse = pygame.mouse.get_pos()
        self.rede_rect = pygame.Rect(300, 200, 30, 30)
        self.rede = pygame.Rect(self.rect[0] - 15, self.rect.centery - 15, 30, 30)
        self.rede.center = self.pos_mouse
            
    def desenhar_rede(self, tela): # Implementação do método de desenhar a rede.
        if self.rede:
            pygame.draw.circle(tela, (CORES["BRANCO"]), self.rede.center, 30)
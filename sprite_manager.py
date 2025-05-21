import pygame

class SpriteSheet:
    def __init__(self, filename): # Carrega o arquivo de spritesheet.
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar o spritesheet: {e}")
            self.sheet = None
    
    def get_image(self, x, y, width, height): # Extrai uma imagem do spritesheet.
        if self.sheet is None:
            # Criar uma superfície vazia como fallback
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.fill((255, 0, 255, 0))  # Transparente
            return image
            
        # Cria uma nova superfície vazia com transparência
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Copia a sprite da imagem original para a nova superfície
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image
    
    def get_sprites(self, width, height, rows, cols): # Recorta todo o spritesheet em várias imagens individuais e Retorna uma matriz bidimensional de imagens.
        sprite_list = []
        for row in range(rows):
            row_sprites = []
            for col in range(cols):
                x = col * width
                y = row * height
                sprite = self.get_image(x, y, width, height)
                row_sprites.append(sprite)
            sprite_list.append(row_sprites)
        return sprite_list
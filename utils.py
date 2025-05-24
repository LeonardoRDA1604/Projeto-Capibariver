import pygame
from configs import *

pygame.init()

# Fontes
FONTE_TEXTO = pygame.font.SysFont(*FONTES["texto"])
FONTE_TEXTO_NEGRITO = pygame.font.SysFont(*FONTES["texto"], bold=True)
FONTE_TITULO_PEQUENO = pygame.font.SysFont(*FONTES["titulo_pequeno"])
FONTE_TITULO_PEQUENO_NEGRITO = pygame.font.SysFont(*FONTES["titulo_pequeno"], bold=True)
FONTE_TITULO_GRANDE_NEGRITO = pygame.font.SysFont(*FONTES["titulo_grande"], bold=True)
FONTE_CONCLUSAO = pygame.font.SysFont(*FONTES["conclusao"])
FONTE_CONCLUSAO_NEGRITO = pygame.font.SysFont(*FONTES["conclusao"], bold=True)
FONTE_BOTAO_MENU = pygame.font.SysFont(*FONTES["botao_menu"], bold=True)
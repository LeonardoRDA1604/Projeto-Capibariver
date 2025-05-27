import pygame
from pygame.locals import *

# === Configurações da tela ===
LARGURA_TELA, ALTURA_TELA = 1280, 720
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
NOME_DO_JOGO = "Capibariver v9.4.4"
FPS = 50 #! os frames do personagem tão organizados para 6 fps

# Fontes
FONTES = {
    "titulo_grande": ('Arial', 56),
    "botao_menu": ('Arial', 32),
    "titulo_pequeno": ('Arial', 30),
    "texto": ('Arial', 24),
    "texto_pequeno": ('Arial', 18),
    "conclusao": ('Arial', 50),
}

# === Cores ===
CORES = {
    "PRETO": (0, 0, 0),
    "PRETO_SOMBRA": (30, 30, 30),
    "CINZA": (150, 150, 150),
    "CINZA_CLARO": (200, 200, 200),
    "BRANCO": (255, 255, 255),
    "VERMELHO": (255, 0, 0),
    "VERMELHO_CLARO": (200, 0, 0),
    "VERDE_LIMÃO": (0, 255, 0),
    "VERDE": (0, 200, 0),
    "VERDE_CLARO": (0, 150, 0),
    "VERDE_MENU": (100, 255, 100),
    "VERDE_MENU_2": (85, 217, 85),
    "AZUL_ESCURO": (17, 13, 120),
    "AZUL": (0, 0, 255),
    "AZUL_CLARO": (0, 0, 200),
    "CIANO": (0, 255, 255),
    "AMARELO": (255, 255, 0),
    "ROXO": (67, 18, 135),
    "ROXO_GUIA": (126, 10, 242),
    "ROXO_GUIA_2": (122, 44, 255),
    "LARANJA": (255, 165, 0),
    "LARANJA_TITULO_MENU": (240, 124, 29),
}

# === Velocidade do jogador e dos itens ===
VEL_JOGADOR = 5
VEL_ITEM = 2

# === Tamanho do jogador e do itens ===
TAMANHO_JOGADOR = 64, 64
TAMANHO_ITEM = 40, 40

# TAMANHOS = { 
#     "jogador": (30, 30),
#     "item": (590, 500)
# }

# === Objetivo do jogo ===                 # 200 objetivo ideal
OBJETIVO = 5

# === Quantidade de lixos ===
QUANT_LIXOS_AGUA = 8
QUANT_LIXOS_TERRA = 4

# === Barra de progressão de objetivo do jogo ===
LARGURA_BARRA = 300
ALTURA_BARRA = 30

# === Áudio ===
SOM_ATIVADO = True
VOLUME_GERAL = 0.5

# Variáveis globais
jogador1 = None
jogador2 = None
itens_agua = []
itens_terra = []
CRIAR_ITEM_EVENTO = None
CRIAR_ITEM_EVENTO_2 = None
progresso = 0
rede_circle = [999, 999]
#? ---------------------------------------------------------------------------------------------------------------------------------------- I
rede_velocidade = 6
#? ---------------------------------------------------------------------------------------------------------------------------------------- F
TRANSPARENCIA_RANGE_REDE = 40
COR_RANGE_REDE = CORES["PRETO"]

OPACIDADE_FUNDO_MENU = 180
import pygame

# === Configurações da tela ===
LARGURA_TELA, ALTURA_TELA = 1280, 720
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
NOME_DO_JOGO = "Capibariver v9.4.4"
FPS = 30 #! os frames do personagem tão organizados para 6 fps


FONTES = {
    "titulo": ('Arial', 30),
    "texto": ('Arial', 24),
    "conclusao": ('Arial', 50),
}

# === Cores ===
CORES = {
    "PRETO": (0, 0, 0),
    "BRANCO": (255, 255, 255),
    "VERMELHO": (255, 0, 0),
    "VERDE_LIMÃO": (0, 255, 0),
    "VERDE": (0, 200, 0),
    "VERDE_CLARO": (0, 150, 0),
    "AZUL": (0, 0, 255),
    "AMARELO": (255, 255, 0),
    "ROXO": (67, 18, 135),
    "CINZA_CLARO": (200, 200, 200),
    "CIANO": (0, 255, 255),
    "LARANJA": (255, 165, 0),
    "AZUL_ESCURO": (17, 13, 120),
    "VERDE MENU": (100, 255, 100),

#    "VERMELHO": (200, 0, 0),
#    "AZUL": (0, 0, 200),
#    "CINZA": (150, 150, 150),
#    "CINZA_CLARO": (200, 200, 200)
}

# === Velocidade do jogador e dos itens ===
VEL_JOGADOR = 5
VEL_ITEM = 3

# === Tamanho do jogador e do itens ===
TAMANHO_JOGADOR = 64, 64
TAMANHO_ITEM = 40, 40

# TAMANHOS = { 
#     "jogador": (30, 30),
#     "item": (590, 500)
# }


# === Objetivo do jogo ===                 # 200 objetivo ideal
OBJETIVO = 200



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
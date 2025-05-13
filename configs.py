import pygame

# === Configurações da tela ===
LARGURA_TELA, ALTURA_TELA = 1280, 720
NOME_DO_JOGO = "Capibariver v9.4.4"
FPS = 30


FONTES = {
    "titulo": ('Arial', 30),
    "texto": ('Arial', 24)
}

# === Cores ===
CORES = {
    "PRETO": (0, 0, 0),
    "BRANCO": (255, 255, 255),
    "VERMELHO": (255, 0, 0),
    "VERDE_LIMÃO": (0, 255, 0),
    "VERDE": (0, 200, 0),
    "VERDE_CLARO": (0, 200, 0),
    "AZUL": (0, 0, 255),
    "AMARELO": (255, 255, 0),
    "ROXO": (67, 18, 135),
    "CINZA_CLARO": (200, 200, 200),
}

# === Velocidade do jogador e dos itens ===
VEL_JOGADOR = 10
VEL_ITEM = 3

# === Tamanho do jogador e do itens ===
TAMANHO_JOGADOR = 30, 30
TAMANHO_ITEM = 20, 20

TAMANHOS = {
    "jogador": (30, 30),
    "item": (20, 20)
}


# === Objetivo do jogo ===
OBJETIVO = 200


# === Barra de progressão de objetivo do jogo ===
LARGURA_BARRA = 300
ALTURA_BARRA = 30







# === Áudio ===
SOM_ATIVADO = True
VOLUME_GERAL = 0.5


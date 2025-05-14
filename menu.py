import pygame
from pygame.locals import *
import sys
import os
from configs import *

class Menu:
    def __init__(self, tela): # Inicializa o menu do jogo.     ||       parâmetro tela -> Superfície do pygame onde o menu será desenhado
        self.tela = tela
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()
        
        # Estados possíveis
        self.estados = ["MENU", "JOGO", "GUIA", "CREDITOS", "OPCOES"]
        self.estado = "MENU"  # Estado inicial
        
        # Fontes
        self.fonte_titulo = pygame.font.SysFont('Arial', 48, bold=True)
        self.fonte_botao = pygame.font.SysFont('Arial', 30)
        
        # Configurações de áudio
        self.som_ativado = True
        self.efeitos_ativados = True
        
        # Carregar imagem de fundo
        try:
            self.background = pygame.image.load(os.path.join('assets', 'tela_menu_capibariver.png'))
            self.background = pygame.transform.scale(self.background, (self.largura_tela, self.altura_tela))
        except:
            print("Imagem de fundo não encontrada. Usando cor sólida.")
            self.background = None
        
        # Botões
        self.botoes = []
        self.criar_botoes()

    def criar_botoes(self): #Cria os botões do menu principal
        opcoes = ["INICIAR", "GUIA", "CRÉDITOS", "OPÇÕES", "SAIR"]
        for i, opcao in enumerate(opcoes):
            largura_botao = 200
            altura_botao = 50
            x = self.largura_tela // 2 - largura_botao // 2
            y = self.altura_tela // 2 - (len(opcoes) * altura_botao) // 2 + i * (altura_botao + 20)
            
            self.botoes.append({
                "texto": opcao,
                "rect": pygame.Rect(x, y, largura_botao, altura_botao),
                "cor": CORES["VERDE"],
                "cor_hover": CORES["VERDE_CLARO"],
                "acao": self.get_acao(opcao)
            })
    
    def get_acao(self, opcao): # Retorna a ação associada a cada botão
        if opcao == "INICIAR":
            return lambda: self.mudar_estado("JOGO")
        elif opcao == "GUIA":
            return lambda: self.mudar_estado("GUIA")
        elif opcao == "CRÉDITOS":
            return lambda: self.mudar_estado("CREDITOS")
        elif opcao == "OPÇÕES":
            return lambda: self.mudar_estado("OPCOES")
        elif opcao == "SAIR":
            return lambda: sys.exit()
        else:
            return lambda: None
    
    def mudar_estado(self, novo_estado):                    # Muda o estado do menu
        if novo_estado in self.estados:
            self.estado = novo_estado
    
    def desenhar(self):                                     # Desenha o menu principal
        if self.background:
            self.tela.blit(self.background, (0, 0))         # Desenha o fundo
        else:
            self.tela.fill(CORES["AZUL"])
# ----------------------------------------------------------------------------------------------------------
        # Desenha o título
        # titulo = self.fonte_titulo.render("Capibariver", True, CORES["BRANCO"])                # Desenha o título
        # self.tela.blit(titulo, (self.largura_tela // 2 - titulo.get_width() // 2, 100))
# ----------------------------------------------------------------------------------------------------------
        
        # Desenha os botões
        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            cor = botao["cor_hover"] if botao["rect"].collidepoint(pos_mouse) else botao["cor"]
            
            # Retângulo do botão
            pygame.draw.rect(self.tela, cor, botao["rect"])
            pygame.draw.rect(self.tela, CORES["PRETO"], botao["rect"], 2)  # Borda
            
            # Texto do botão
            texto = self.fonte_botao.render(botao["texto"], True, CORES["PRETO"])
            self.tela.blit(texto, (
                botao["rect"].centerx - texto.get_width() // 2,
                botao["rect"].centery - texto.get_height() // 2
            ))
    
    def desenhar_opcoes(self): # Desenha o menu de opções
        if self.background:
            self.tela.blit(self.background, (0, 0)) # Desenha o fundo
        else:
            self.tela.fill(CORES["AZUL"])
        
        # Desenha o título
        titulo = self.fonte_titulo.render("OPÇÕES", True, CORES["BRANCO"])
        self.tela.blit(titulo, (self.largura_tela // 2 - titulo.get_width() // 2, 100))
        
        # Opção de Som
        som_texto = self.fonte_botao.render("Som (tecla 1): " + ("LIGADO" if self.som_ativado else "DESLIGADO"), 
                                            True, CORES["BRANCO"])
        self.tela.blit(som_texto, (self.largura_tela // 2 - som_texto.get_width() // 2, 250))
        
        # Opção de Efeitos
        efeitos_texto = self.fonte_botao.render("Efeitos (tecla 2): " + ("LIGADO" if self.efeitos_ativados else "DESLIGADO"), 
                                               True, CORES["BRANCO"])
        self.tela.blit(efeitos_texto, (self.largura_tela // 2 - efeitos_texto.get_width() // 2, 300))
        
        # Botão voltar
        voltar_rect = pygame.Rect(self.largura_tela // 2 - 100, 400, 200, 50)
        pygame.draw.rect(self.tela, CORES["VERDE"], voltar_rect)
        pygame.draw.rect(self.tela, CORES["PRETO"], voltar_rect, 2)
        
        voltar_texto = self.fonte_botao.render("VOLTAR", True, CORES["PRETO"])
        self.tela.blit(voltar_texto, (
            voltar_rect.centerx - voltar_texto.get_width() // 2,
            voltar_rect.centery - voltar_texto.get_height() // 2
        ))
        
        return voltar_rect  # Retorna o rect do botão voltar para checagem de clique
    
    def desenhar_guia(self): # Desenha a tela de guia        
        if self.background:
            self.tela.blit(self.background, (0, 0)) # Desenha o fundo
        else:
            self.tela.fill(CORES["AZUL"])
        
        # Desenha o título
        titulo = self.fonte_titulo.render("GUIA DO JOGO", True, CORES["BRANCO"])
        self.tela.blit(titulo, (self.largura_tela // 2 - titulo.get_width() // 2, 100))
        # ----------------------------------------------------------------------------------------------------------
        # Instruções
        instrucoes = [
            f"Jogador 1 (Verde): Use as teclas 'W', 'A', 'S' e 'D' para mover o personagem e ESPAÇO para coletar os resíduos da margem",
            "Jogador 2 (Roxo): Use setas direcionais do teclado para mover o personagem e clique com o botão direito do mouse para lançar rede e coletar os resíduos do rio",
            "Colete itens para limpar o rio e atingir o objetivo!",
            "Trabalhem juntos para conseguir o melhor resultado!"
        ]
        # ----------------------------------------------------------------------------------------------------------
        for i, texto in enumerate(instrucoes):
            linha = self.fonte_botao.render(texto, True, CORES["BRANCO"])
            self.tela.blit(linha, (self.largura_tela // 2 - linha.get_width() // 2, 200 + i * 40))
        
        # Botão voltar
        voltar_rect = pygame.Rect(self.largura_tela // 2 - 100, 400, 200, 50)
        pygame.draw.rect(self.tela, CORES["VERDE"], voltar_rect)
        pygame.draw.rect(self.tela, CORES["PRETO"], voltar_rect, 2)
        
        voltar_texto = self.fonte_botao.render("VOLTAR", True, CORES["PRETO"])
        self.tela.blit(voltar_texto, (
            voltar_rect.centerx - voltar_texto.get_width() // 2,
            voltar_rect.centery - voltar_texto.get_height() // 2
        ))
        
        return voltar_rect  # Retorna o rect do botão voltar para checagem de clique
    
    def desenhar_creditos(self):
        """Desenha a tela de créditos"""
        # Desenha o fundo
        if self.background:
            self.tela.blit(self.background, (0, 0))
        else:
            self.tela.fill(CORES["AZUL"])
        
        # Desenha o título
        titulo = self.fonte_titulo.render("CRÉDITOS", True, CORES["PRETO"])
        self.tela.blit(titulo, (self.largura_tela // 2 - titulo.get_width() // 2, 100))
        
        # Créditos
        creditos = [
            "Desenvolvido por: Leonardo Rafael, Gabriel Lucas, Heitor da Silva e Brenno Rodrigues",
            "Arte por: Guilherme Enrique, Yasmim Victória",
            "Documentado por: Wesley Luiz e Brenda Rafaelly",
            "Versão: 9.4.4",
            "Agradecimentos especiais: Coord. Patrícia Mergulhão, Prof. Humberto Caetano, Camila Moura e Davi Wanderley",
            "Música: Rebbeka Cynthia",
        ]
        
        for i, texto in enumerate(creditos):
            linha = self.fonte_botao.render(texto, True, CORES["PRETO"])
            self.tela.blit(linha, (self.largura_tela // 2 - linha.get_width() // 2, 200 + i * 40))
        
        # Botão voltar
        voltar_rect = pygame.Rect(self.largura_tela // 2 - 100, 400, 200, 50)
        pygame.draw.rect(self.tela, CORES["VERDE"], voltar_rect)
        pygame.draw.rect(self.tela, CORES["PRETO"], voltar_rect, 2)
        
        voltar_texto = self.fonte_botao.render("VOLTAR", True, CORES["PRETO"])
        self.tela.blit(voltar_texto, (
            voltar_rect.centerx - voltar_texto.get_width() // 2,
            voltar_rect.centery - voltar_texto.get_height() // 2
        ))
        
        return voltar_rect  # Retorna o rect do botão voltar para checagem de clique
    
    def eventos(self, eventos):
        """Processa os eventos do pygame"""
        for evento in eventos:
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
                
            # Verificar cliques nos botões
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:  # Clique esquerdo
                pos_mouse = pygame.mouse.get_pos()
                
                if self.estado == "MENU":
                    for botao in self.botoes:
                        if botao["rect"].collidepoint(pos_mouse):
                            botao["acao"]()
                
                elif self.estado == "OPCOES":
                    voltar_rect = self.desenhar_opcoes()
                    if voltar_rect.collidepoint(pos_mouse):
                        self.estado = "MENU"
                
                elif self.estado == "GUIA":
                    voltar_rect = self.desenhar_guia()
                    if voltar_rect.collidepoint(pos_mouse):
                        self.estado = "MENU"
                
                elif self.estado == "CREDITOS":
                    voltar_rect = self.desenhar_creditos()
                    if voltar_rect.collidepoint(pos_mouse):
                        self.estado = "MENU"
            
            # Teclas para as opções
            if evento.type == KEYDOWN and self.estado == "OPCOES":
                if evento.key == K_1:  # Tecla 1 para alternar som
                    self.som_ativado = not self.som_ativado
                elif evento.key == K_2:  # Tecla 2 para alternar efeitos
                    self.efeitos_ativados = not self.efeitos_ativados
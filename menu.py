import pygame, sys, os
from pygame.locals import *
from configs import *
from utils import *

class Menu:
    def __init__(self, tela): # Inicializa o menu do jogo.     ||       parâmetro tela -> Superfície do pygame onde o menu será desenhado
        self.tela = TELA
        self.largura_tela = tela.get_width()
        self.altura_tela = tela.get_height()
        
        # Estados possíveis
        self.estados = ["MENU", "JOGO", "GUIA", "CREDITOS", "OPCOES"]
        self.estado = "MENU"  # Estado inicial

        
        # Configurações de áudio
        self.som_ativado = True
        self.volume = 00  # Volume de 0 a 100 (começando em 10%)
        self.efeitos_ativados = True
        self.musica_carregada = False
        
        # Carregar imagem de fundo
        try:
            self.background = pygame.image.load(os.path.join('assets/sprites/screens', 'tela_menu_capibariver.png'))
            self.background = pygame.transform.scale(self.background, (self.largura_tela, self.altura_tela))
        except:
            # print("Imagem de fundo não encontrada. Usando cor sólida.")
            self.background = None

        # Inicializar sistema de som
        self.inicializar_som()

        # Botões
        self.botoes = []
        self.criar_botoes()


    # Carregar som do jogo
    def inicializar_som(self): # Inicializa o sistema de som e carrega a música
        try:
            # Caminho para o som ambiente
            caminho_som = os.path.join('assets/sounds', 'trilha_sonora_edit7.mp3')  # .ogg, .wav etc.
            # Verifica se o arquivo existe
            if os.path.exists(caminho_som):
                pygame.mixer.music.load(caminho_som)
                self.musica_carregada = True
                # print(f"Música carregada: {caminho_som}")
                # Inicia a música se o som estiver ativado
                if self.som_ativado:
                    pygame.mixer.music.set_volume(self.volume / 100.0)  # volume entre 0.0(0%) e 1.0(100%) ||| divide e transforma 10 em 0.1 por exemplo
                    pygame.mixer.music.play(-1)  # -1 = loop infinito
                    # print("Música iniciada")
            else:
                print(f"Arquivo de música não encontrado: {caminho_som}")
                self.musica_carregada = False
        except pygame.error as e:
            # print(f"Erro ao carregar trilha sonora: {e}")
            self.musica_carregada = False


    def controlar_som(self): # controla o estado da música baseado na config de som
        if not self.musica_carregada:
            # print("Música não carregada, não é possível controlar")
            return
        try:
            if self.som_ativado: # Se o som está ativado mas a música não está tocando, inicia
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.set_volume(self.volume / 100.0)  # volume entre 0.0(0%) e 1.0(100%) ||| divide e transforma 10 em 0.1 por exemplo
                    # Carrega e toca o som em loop infinito
                    pygame.mixer.music.play(-1)  # -1 = loop infinito
                    # print("Música iniciada via controle")
                else:
                    # Se já está tocando, apenas ajusta o volume
                    pygame.mixer.music.set_volume(self.volume / 100.0)
                    # print("Volume ajustado")
            else:
                # Se o som está desativado, para a música
                pygame.mixer.music.stop()
                # print("Música parada")
        except pygame.error as e:
            print(f"Erro ao carregar trilha sonora: {e}")


    def alternar_som(self): # alterna o estado do som e controla a música
        self.som_ativado = not self.som_ativado
        # print(f"Som {'ativado' if self.som_ativado else 'desativado'}")
        self.controlar_som()


    def aumentar_volume(self): # Aumenta o volume em 1%
        if self.volume < 100:
            self.volume += 10
            # print(f"Volume aumentado para: {self.volume}%")
            if self.som_ativado and self.musica_carregada:
                pygame.mixer.music.set_volume(self.volume / 100.0)


    def diminuir_volume(self): # Diminui o volume em 1%
        if self.volume > 0:
            self.volume -= 10
            # print(f"Volume diminuído para: {self.volume}%")
            if self.som_ativado and self.musica_carregada:
                pygame.mixer.music.set_volume(self.volume / 100.0)


    def texto_com_sombra(self, texto, fonte, cor, cor_sombra=(CORES["PRETO_SOMBRA"]), deslocamento=2):
        # Renderiza a sombra
        superficie_sombra = fonte.render(texto, True, cor_sombra)
        # Renderiza o texto principal
        superficie_texto = fonte.render(texto, True, cor)
        # Cria uma superfície que comporta texto e sombra
        superficie_final = pygame.Surface((superficie_texto.get_width() + deslocamento, 
                                          superficie_texto.get_height() + deslocamento), 
                                          pygame.SRCALPHA)
        # Posiciona sombra e texto
        superficie_final.blit(superficie_sombra, (deslocamento, deslocamento))
        superficie_final.blit(superficie_texto, (0, 0))
        return superficie_final


    def renderizar_texto(self, texto, fonte, cor, y, alinhamento="CENTRO", usar_sombra=True): #  Renderiza texto com alinhamento e sombra opcional.
        if usar_sombra:
            superficie_texto = self.texto_com_sombra(texto, fonte, cor)
        else:
            superficie_texto = fonte.render(texto, True, cor)

        if alinhamento == "CENTRO_GUIA":
            x = self.largura_tela // 2 - superficie_texto.get_width() // 2
        elif alinhamento == "ESQUERDA_GUIA":
            x = self.largura_tela // 2 - 270  # ajuste para alinhamento à esquerda
        elif alinhamento == "DIREITA_GUIA":
            x = self.largura_tela // 2 + 400 - superficie_texto.get_width()
        elif alinhamento == "CENTRO_CREDITOS":
            x = self.largura_tela // 2 - superficie_texto.get_width() // 2
        elif alinhamento == "ESQUERDA_CREDITOS":
            x = self.largura_tela // 2 - 370  # ajuste para alinhamento à esquerda
        elif alinhamento == "DIREITA_CREDITOS":
            x = self.largura_tela // 2 + 400 - superficie_texto.get_width()
        elif alinhamento == "CENTRO_OPCOES":
            x = self.largura_tela // 2 - superficie_texto.get_width() // 2
        elif alinhamento == "ESQUERDA_OPCOES":
            x = self.largura_tela // 2 - 200  # ajuste para alinhamento à esquerda
        elif alinhamento == "DIREITA_OPCOES":
            x = self.largura_tela // 2 + 400 - superficie_texto.get_width()
        else:
            x = 0  # fallback

        self.tela.blit(superficie_texto, (x, y))


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

        # Desenha os botões
        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            cor = botao["cor_hover"] if botao["rect"].collidepoint(pos_mouse) else botao["cor"]
            
            # Retângulo do botão
            pygame.draw.rect(self.tela, cor, botao["rect"])
            pygame.draw.rect(self.tela, CORES["PRETO"], botao["rect"], 2)  # Borda
            
            # Texto do botão
            texto = FONTE_BOTAO_MENU.render(botao["texto"], True, CORES["PRETO"])
            self.tela.blit(texto, (
                botao["rect"].centerx - texto.get_width() // 2,
                botao["rect"].centery - texto.get_height() // 2
            ))


    def desenhar_guia(self): # Desenha a tela de guia        
        if self.background:
            self.tela.blit(self.background, (0, 0)) # Desenha o fundo
            # Painel de fundo (retangulo preto com opacidade)
            painel = pygame.Surface((600, 380), pygame.SRCALPHA) #todo ------------------------------------------------------------- (opacidade do fundo)
            painel.fill((*CORES["PRETO"], OPACIDADE_FUNDO_MENU))  # Preto com opacidade
            self.tela.blit(painel, (self.largura_tela // 2 - 300, 215))
        else:
            self.tela.fill(CORES["AZUL"])

        # Desenha o título
        self.renderizar_texto("GUIA DO JOGO", FONTE_TITULO_PEQUENO_NEGRITO, CORES["LARANJA_TITULO_MENU"], 220, "CENTRO_GUIA")

        # Instruções
        instrucoes = [
            ("Jogador 1 (Personagem Feminino):", "CENTRO_GUIA", CORES["AMARELO"]),
            ("- Use as teclas 'W', 'A', 'S' e 'D' para mover o personagem.", "ESQUERDA_GUIA", CORES["BRANCO"]),
            ("- Use a tecla ESPAÇO para coletar os resíduos da margem.", "ESQUERDA_GUIA", CORES["BRANCO"]),
            ("Jogador 2 (Personagem Masculino):", "CENTRO_GUIA", CORES["VERMELHO"]),
            ("- Use as setas direcionais do teclado para mover o personagem.", "ESQUERDA_GUIA", CORES["BRANCO"]),
            ("- Clique com o botão direito do mouse dentro da área de alcance,", "ESQUERDA_GUIA", CORES["BRANCO"]),
            ("  para lançar rede e coletar os resíduos do rio.", "ESQUERDA_GUIA", CORES["BRANCO"]),
            ("Colete itens para limpar o rio e atingir o objetivo!", "CENTRO_GUIA", CORES["ROXO_GUIA_2"]),
            ("Trabalhem juntos para conseguir o melhor resultado!", "CENTRO_GUIA", CORES["VERDE_MENU"]),
        ]

        y_base = 270
        espaco_linha = 35

        for i, (texto, alinhamento, cor) in enumerate(instrucoes):
            # Usar o método renderizar_texto da própria classe
            self.renderizar_texto(texto, FONTE_TEXTO_PEQUENO_NEGRITO, cor, y_base + i * espaco_linha, alinhamento)

        # Botão voltar
        voltar_rect = pygame.Rect(self.largura_tela // 2 - 100, 610, 200, 50)
        pygame.draw.rect(self.tela, CORES["VERDE"], voltar_rect)
        pygame.draw.rect(self.tela, CORES["PRETO"], voltar_rect, 2)
        
        voltar_texto = FONTE_BOTAO_MENU.render("VOLTAR", True, CORES["PRETO"])
        self.tela.blit(voltar_texto, (
            voltar_rect.centerx - voltar_texto.get_width() // 2,
            voltar_rect.centery - voltar_texto.get_height() // 2
        ))
        
        return voltar_rect  # Retorna o rect do botão voltar para checagem de clique


    def desenhar_creditos(self): # Desenha a tela de créditos
        # Desenha o fundo
        if self.background:
            self.tela.blit(self.background, (0, 0))
            # Painel de fundo (retangulo preto com opacidade)
            painel = pygame.Surface((800, 360), pygame.SRCALPHA)
            painel.fill((*CORES["PRETO"], OPACIDADE_FUNDO_MENU))  
            self.tela.blit(painel, (self.largura_tela // 2 - 400, 215)) #todo ------------------------------------------------------------- (opacidade do fundo)
        else:
            self.tela.fill(CORES["AZUL"])
        
        # Desenha o título
        self.renderizar_texto("CRÉDITOS", FONTE_TITULO_PEQUENO_NEGRITO, CORES["LARANJA_TITULO_MENU"], 220, "CENTRO_GUIA")
        
        # Créditos
        creditos = [
            ("Desenvolvido por: ", "ESQUERDA_CREDITOS", CORES["VERDE_MENU"]),
            ("Leonardo Rafael, Gabriel Lucas, Heitor da Silva e Brenno Rodrigues", "ESQUERDA_CREDITOS", CORES["BRANCO"]),
            ("Arte por: ", "ESQUERDA_CREDITOS", CORES["VERDE_MENU"]),
            ("Guilherme Enrique e Yasmim Victória", "ESQUERDA_CREDITOS", CORES["BRANCO"]),
            ("Documentado por:", "ESQUERDA_CREDITOS", CORES["VERDE_MENU"]),
            ("Wesley Luiz e Brenda Rafaelly", "ESQUERDA_CREDITOS", CORES["BRANCO"]),
            ("Música por:", "ESQUERDA_CREDITOS", CORES["VERDE_MENU"]),
            ("Rebbeka Cynthia", "ESQUERDA_CREDITOS", CORES["BRANCO"]),
            ("Agradecimentos especiais:", "ESQUERDA_CREDITOS", CORES["VERDE_MENU"]),
            ("Coord. Patrícia Mergulhão, Prof. Humberto Caetano, Camila Moura e Davi Wanderley", "ESQUERDA_CREDITOS", CORES["BRANCO"]),
        ]

        # Definir posição inicial e espaçamento
        y_base = 260  # Posição Y inicial para os créditos
        espaco_linha = 30  # Espaço entre cada linha de crédito
        for i, (texto, alinhamento, cor) in enumerate(creditos):
            # Usar o método renderizar_texto da própria classe
            self.renderizar_texto(texto, FONTE_TEXTO_PEQUENO_NEGRITO, cor, y_base + i * espaco_linha, alinhamento)

        # Botão voltar
        voltar_rect = pygame.Rect(self.largura_tela // 2 - 100, 590, 200, 50)
        pygame.draw.rect(self.tela, CORES["VERDE"], voltar_rect)
        pygame.draw.rect(self.tela, CORES["PRETO"], voltar_rect, 2)
        
        voltar_texto = FONTE_BOTAO_MENU.render("VOLTAR", True, CORES["PRETO"])
        self.tela.blit(voltar_texto, (
            voltar_rect.centerx - voltar_texto.get_width() // 2,
            voltar_rect.centery - voltar_texto.get_height() // 2
        ))
        
        return voltar_rect  # Retorna o rect do botão voltar para checagem de clique

        
    def desenhar_opcoes(self): # Desenha o menu de opções
        # Desenha o fundo
        if self.background:
            self.tela.blit(self.background, (0, 0))
            # Painel de fundo (retangulo preto com opacidade)
            painel = pygame.Surface((450, 280), pygame.SRCALPHA)
            painel.fill((*CORES["PRETO"], OPACIDADE_FUNDO_MENU))  
            self.tela.blit(painel, (self.largura_tela // 2 - 225, 215))
        else:
            self.tela.fill(CORES["AZUL"])
        
        # Desenha o título
        self.renderizar_texto("OPÇÕES", FONTE_TITULO_PEQUENO_NEGRITO, CORES["LARANJA_TITULO_MENU"], 220, "CENTRO_GUIA")
        
        # Definir posição inicial e espaçamento
        y_base = 260  # Posição Y inicial para as opções
        espaco_linha = 35  # Espaço entre cada linha de opção
        linha_atual = 0
        
        # 1. Música (Tecla 1 para Ligar/Desligar)
        self.renderizar_texto("Tecla 1 para Ligar/Desligar a música do jogo", FONTE_TEXTO_PEQUENO_NEGRITO, CORES["VERDE_MENU"], 
                            y_base + linha_atual * espaco_linha, "ESQUERDA_OPCOES")
        linha_atual += 1

        # 2. MÚSICA: LIGADO/DESLIGADO na mesma linha
        y_som = y_base + linha_atual * espaco_linha
        som_texto = FONTE_TEXTO_PEQUENO_NEGRITO.render("MÚSICA: ", True, CORES["BRANCO"])
        status_texto = FONTE_TEXTO_PEQUENO_NEGRITO.render("LIGADA" if self.som_ativado else "DESLIGADA", True, 
                                            CORES["VERDE"] if self.som_ativado else CORES["VERMELHO_CLARO"])
        
        # Calcular posições para centralizar ambos os textos juntos
        largura_total = som_texto.get_width() + status_texto.get_width()
        x_inicio = 440
        # x_inicio = self.largura_tela // 2 - largura_total // 2
        
        self.tela.blit(som_texto, (x_inicio, y_som))
        self.tela.blit(status_texto, (x_inicio + som_texto.get_width(), y_som))
        linha_atual += 1

        # 3. Blank space, para separar
        self.renderizar_texto("", FONTE_TEXTO_PEQUENO_NEGRITO, CORES["BRANCO"], 
                            y_base + linha_atual * espaco_linha, "ESQUERDA_OPCOES")
        linha_atual += 1

        # 4. Volume (Tecla 2 para Diminuir o som do jogo)
        self.renderizar_texto("Tecla 2 para diminuir o som do jogo", FONTE_TEXTO_PEQUENO_NEGRITO, CORES["VERDE_MENU"], 
                            y_base + linha_atual * espaco_linha, "ESQUERDA_OPCOES")
        linha_atual += 1
        
        # 5. Volume (Tecla 3 para Aumentar o som do jogo)
        self.renderizar_texto("ou a Tecla 3 para aumentar", FONTE_TEXTO_PEQUENO_NEGRITO, CORES["VERDE_MENU"], 
                            y_base + linha_atual * espaco_linha, "ESQUERDA_OPCOES")
        linha_atual += 1

        # 6. VOLUME: x% na mesma linha
        y_volume = y_base + linha_atual * espaco_linha
        volume_texto = FONTE_TEXTO_PEQUENO_NEGRITO.render("VOLUME: ", True, CORES["BRANCO"])
        valor_texto = FONTE_TEXTO_PEQUENO_NEGRITO.render(f"{self.volume}%", True, CORES["ROXO_GUIA"])
        
        # Calcular posições para centralizar ambos os textos juntos
        largura_total = volume_texto.get_width() + valor_texto.get_width()
        x_inicio = 440
        # x_inicio = self.largura_tela // 2 - largura_total // 2
        
        self.tela.blit(volume_texto, (x_inicio, y_volume))
        self.tela.blit(valor_texto, (x_inicio + volume_texto.get_width(), y_volume))

        # Botão voltar
        voltar_rect = pygame.Rect(self.largura_tela // 2 - 100, 535, 200, 50)
        pygame.draw.rect(self.tela, CORES["VERDE"], voltar_rect)
        pygame.draw.rect(self.tela, CORES["PRETO"], voltar_rect, 2)
        
        voltar_texto = FONTE_BOTAO_MENU.render("VOLTAR", True, CORES["PRETO"])
        self.tela.blit(voltar_texto, (
            voltar_rect.centerx - voltar_texto.get_width() // 2,
            voltar_rect.centery - voltar_texto.get_height() // 2
        ))
        
        return voltar_rect  # Retorna o rect do botão voltar para checagem de clique


    def eventos(self, eventos): # Processa os eventos do pygame
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
                    self.alternar_som()
                elif evento.key == K_2:  # Tecla 2 para diminuir volume
                    self.diminuir_volume()
                elif evento.key == K_3:  # Tecla 3 para aumentar volume
                    self.aumentar_volume()
                elif evento.key == K_4:  # Tecla 4 para alternar efeitos
                    self.efeitos_ativados = not self.efeitos_ativados
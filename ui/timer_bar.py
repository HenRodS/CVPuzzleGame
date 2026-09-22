import pygame

class TimerBar:
    def __init__(self, largura_tela=1280, x=None, y=18, largura=500, altura=26, duracao_padrao=30):
        self.largura_tela = largura_tela
        self.largura = largura
        self.altura = altura
        self.x = (largura_tela - largura) // 2 if x is None else x
        self.y = y
        self.duracao_padrao = duracao_padrao
        self.duracao_ms = int(duracao_padrao * 1000)
        self.start_ticks = 0
        self.tempo_restante_ms = self.duracao_ms
        self.pausado = False
        self.esgotado = False
        self.fonte = pygame.font.SysFont("Arial", 18, bold=True)

    def iniciar(self, duracao_segundos=None):
        """Inicia ou reinicia a contagem do tempo."""
        if duracao_segundos is not None:
            self.duracao_ms = int(duracao_segundos * 1000)
        else:
            self.duracao_ms = int(self.duracao_padrao * 1000)
            
        self.start_ticks = pygame.time.get_ticks()
        self.tempo_restante_ms = self.duracao_ms
        self.pausado = False
        self.esgotado = False

    def pausar(self):
        """Pausa o temporizador (usado na vitória)."""
        self.pausado = True

    def atualizar(self):
        """Atualiza a contagem de tempo."""
        if self.pausado or self.esgotado:
            return

        passado = pygame.time.get_ticks() - self.start_ticks
        self.tempo_restante_ms = max(0, self.duracao_ms - passado)

        if self.tempo_restante_ms <= 0:
            self.esgotado = True

    def esta_esgotado(self):
        """Retorna se o tempo acabou."""
        return self.esgotado

    def tempo_restante_segundos(self):
        """Retorna o tempo restante em segundos (arredondado para cima)."""
        return max(0, (self.tempo_restante_ms + 999) // 1000)

    def desenhar(self, tela):
        """Desenha a barra de tempo na tela."""
        progresso = max(0.0, min(1.0, self.tempo_restante_ms / self.duracao_ms)) if self.duracao_ms > 0 else 0.0

        # Sombra externa
        pygame.draw.rect(tela, (15, 15, 15), (self.x + 3, self.y + 3, self.largura, self.altura), border_radius=10)
        # Fundo da barra
        pygame.draw.rect(tela, (40, 40, 40), (self.x, self.y, self.largura, self.altura), border_radius=10)

        # Cor dinâmica de acordo com o tempo restante
        if progresso > 0.5:
            cor_barra = (46, 204, 113)  # Verde
        elif progresso > 0.2:
            cor_barra = (241, 196, 15)  # Amarelo / Laranja
        else:
            cor_barra = (231, 76, 60)   # Vermelho

        # Preenchimento da barra (vai diminuindo)
        largura_preenchimento = int((self.largura - 6) * progresso)
        if largura_preenchimento > 0:
            rect_preenchimento = pygame.Rect(self.x + 3, self.y + 3, largura_preenchimento, self.altura - 6)
            pygame.draw.rect(tela, cor_barra, rect_preenchimento, border_radius=8)

        # Borda
        pygame.draw.rect(tela, (220, 220, 220), (self.x, self.y, self.largura, self.altura), width=2, border_radius=10)

        # Texto com minutos e segundos
        total_seg = self.tempo_restante_segundos()
        minutos = total_seg // 60
        segundos = total_seg % 60
        texto_tempo = f"TEMPO: {minutos:02d}:{segundos:02d}"

        # Renderização do texto com leve sombra para contraste
        txt_sombra = self.fonte.render(texto_tempo, True, (0, 0, 0))
        txt_surf = self.fonte.render(texto_tempo, True, (255, 255, 255))

        rect_centro = (self.x + self.largura // 2, self.y + self.altura // 2)
        tela.blit(txt_sombra, txt_sombra.get_rect(center=(rect_centro[0] + 1, rect_centro[1] + 1)))
        tela.blit(txt_surf, txt_surf.get_rect(center=rect_centro))

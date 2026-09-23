import pygame

class TimerUI:
    """Responsável por renderizar graficamente os dados do TimerSystem."""
    def __init__(self, timer_system, largura_tela=1280, x=None, y=18, largura=500, altura=26):
        self.timer = timer_system  # Referência à lógica
        self.largura_tela = largura_tela
        self.largura = largura
        self.altura = altura
        self.x = (largura_tela - largura) // 2 if x is None else x
        self.y = y
        self.fonte = pygame.font.SysFont("Arial", 18, bold=True)

    def desenhar(self, tela):
        """Lê os dados do timer e desenha a barra na tela."""
        progresso = self.timer.get_progresso()

        # Sombra externa
        pygame.draw.rect(tela, (15, 15, 15), (self.x + 3, self.y + 3, self.largura, self.altura), border_radius=10)
        # Fundo da barra
        pygame.draw.rect(tela, (40, 40, 40), (self.x, self.y, self.largura, self.altura), border_radius=10)

        # Cor dinâmica de acordo com o progresso restante
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
        total_seg = self.timer.tempo_restante_segundos()
        minutos = total_seg // 60
        segundos = total_seg % 60
        texto_tempo = f"TEMPO: {minutos:02d}:{segundos:02d}"

        # Renderização do texto com leve sombra para contraste
        txt_sombra = self.fonte.render(texto_tempo, True, (0, 0, 0))
        txt_surf = self.fonte.render(texto_tempo, True, (255, 255, 255))

        rect_centro = (self.x + self.largura // 2, self.y + self.altura // 2)
        tela.blit(txt_sombra, txt_sombra.get_rect(center=(rect_centro[0] + 1, rect_centro[1] + 1)))
        tela.blit(txt_surf, txt_surf.get_rect(center=rect_centro))

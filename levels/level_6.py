import pygame
import math
from systems.level_generator import generate_fixed_level

class Level6:
    tempo = 60

    def __init__(self, largura=1280, altura=720):
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont("Arial", 16, bold=True)

        # Configurações da barreira central móvel
        self.espessura = 44
        self.altura_barreira = 360
        self.centro_x = (largura - self.espessura) // 2

        # Limites verticais de movimentação (do topo até encostar no chão)
        self.min_y = 0
        self.max_y = altura - self.altura_barreira  # 360px de percurso

        # Barreira retangular única central
        self.barreira = pygame.Rect(self.centro_x, self.min_y, self.espessura, self.altura_barreira)
        self.obstaculos = [self.barreira]

    def load(self):
        print("ping 6")
        return generate_fixed_level(qtd_pecas=2, w=150, h=150)

    def setup_obstacles(self, obstacle_system):
        """Registra a área de perigo móvel no sistema de obstáculos."""
        obstacle_system.definir_areas(self.obstaculos)

    def obter_obstaculos(self):
        """Retorna a lista de obstáculos deste level."""
        return self.obstaculos

    def atualizar(self):
        """Atualiza a posição da barreira com movimento vertical contínuo e suave."""
        ticks = pygame.time.get_ticks()
        # Oscilação senoidal suave: desacelera nos extremos (topo e base) dando tempo para passar
        fator = (math.sin(ticks * 0.0018) + 1.0) / 2.0
        self.barreira.y = int(self.min_y + fator * (self.max_y - self.min_y))

    def _desenhar_area_perigo(self, tela, rect):
        """Renderiza a barreira com efeitos visuais de pulsação e aviso."""
        ticks = pygame.time.get_ticks()
        pulso = int(25 * math.sin(ticks * 0.005))

        # 1. Corpo principal com cor dinâmica pulsante
        r = min(255, max(0, 200 + pulso))
        cor_corpo = (r, 35, 45)
        pygame.draw.rect(tela, cor_corpo, rect, border_radius=10)

        # 2. Faixas diagonais estilo perigo/hazard
        largura_listra = 8
        espaco = 28
        clip_anterior = tela.get_clip()
        tela.set_clip(rect)
        for offset_y in range(-rect.width * 2, rect.height + rect.width * 2, espaco):
            p1 = (rect.left - 10, rect.top + offset_y)
            p2 = (rect.right + 10, rect.top + offset_y + rect.width + 20)
            pygame.draw.line(tela, (110, 15, 20), p1, p2, width=largura_listra)
        tela.set_clip(clip_anterior)

        # 3. Borda externa brilhante
        pygame.draw.rect(tela, (255, 90, 90), rect, width=3, border_radius=10)

    def desenhar_obstaculos(self, tela):
        """Atualiza a posição e renderiza a barreira móvel na tela."""
        self.atualizar()
        for area in self.obstaculos:
            self._desenhar_area_perigo(tela, area)

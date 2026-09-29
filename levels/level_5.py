import pygame
import math
from systems.level_generator import generate_fixed_level

class Level5:
    tempo = 75

    def __init__(self, largura=1280, altura=720):
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont("Arial", 16, bold=True)

        espessura = 36

        # --- 1º SET: Abertura no topo (pequena barreira no topo e uma maior embaixo) ---
        x_set1 = 410
        alt_topo_1 = 70
        abertura_1 = 240
        y_baixo_1 = alt_topo_1 + abertura_1  # 310

        self.set1_topo = pygame.Rect(x_set1, 0, espessura, alt_topo_1)
        self.set1_baixo = pygame.Rect(x_set1, y_baixo_1, espessura, altura - y_baixo_1)

        # --- 2º SET: Abertura embaixo ---
        x_set2 = 635
        alt_topo_2 = 470  # deixa abertura de 250px na base (470 a 720)

        self.set2_topo = pygame.Rect(x_set2, 0, espessura, alt_topo_2)

        # --- 3º SET: Abertura no meio ---
        x_set3 = 860
        abertura_3 = 250
        y_abertura_3_inicio = (altura - abertura_3) // 2   # 235
        y_abertura_3_fim = y_abertura_3_inicio + abertura_3 # 485

        self.set3_topo = pygame.Rect(x_set3, 0, espessura, y_abertura_3_inicio)
        self.set3_baixo = pygame.Rect(x_set3, y_abertura_3_fim, espessura, altura - y_abertura_3_fim)

        self.obstaculos = [
            self.set1_topo, self.set1_baixo,
            self.set2_topo,
            self.set3_topo, self.set3_baixo
        ]

    def load(self):
        print("ping 5")
        return generate_fixed_level(qtd_pecas=2, w=130, h=130)

    def setup_obstacles(self, obstacle_system):
        """Registra as áreas de perigo no sistema de obstáculos."""
        obstacle_system.definir_areas(self.obstaculos)

    def obter_obstaculos(self):
        """Retorna a lista de áreas de perigo deste level."""
        return self.obstaculos

    def _desenhar_area_perigo(self, tela, rect, texto="PERIGO"):
        """Renderiza a área de perigo com efeitos visuais de pulsação e aviso."""
        ticks = pygame.time.get_ticks()
        pulso = int(25 * math.sin(ticks * 0.005))

        # 2. Corpo principal com cor dinâmica pulsante
        r = min(255, max(0, 200 + pulso))
        cor_corpo = (r, 35, 45)
        pygame.draw.rect(tela, cor_corpo, rect, border_radius=10)

        # 3. Faixas diagonais estilo perigo/hazard
        largura_listra = 8
        espaco = 28
        clip_anterior = tela.get_clip()
        tela.set_clip(rect)
        for offset_y in range(-rect.width * 2, rect.height + rect.width * 2, espaco):
            p1 = (rect.left - 10, rect.top + offset_y)
            p2 = (rect.right + 10, rect.top + offset_y + rect.width + 20)
            pygame.draw.line(tela, (110, 15, 20), p1, p2, width=largura_listra)
        tela.set_clip(clip_anterior)

        # 4. Borda externa brilhante
        pygame.draw.rect(tela, (255, 90, 90), rect, width=3, border_radius=10)

    def desenhar_obstaculos(self, tela):
        """Renderiza os 3 sets de obstáculos da Fase 5 na tela."""
        for area in self.obstaculos:
            self._desenhar_area_perigo(tela, area, texto="PERIGO")

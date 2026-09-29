import pygame
import math
from systems.level_generator import generate_fixed_level

class Level4:
    tempo = 60

    def __init__(self, largura=1280, altura=720):
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont("Arial", 16, bold=True)

        # Gera os obstáculos no topo e na parte de baixo da tela (barreiras verticais),
        # deixando uma abertura no meio para o jogador guiar as peças entre os lados.
        espessura = 44
        centro_x = (largura - espessura) // 2

        # Corredor central com 260px de altura (peças têm 160px)
        corredor_altura = 260
        y_abertura_inicio = (altura - corredor_altura) // 2   # 230
        y_abertura_fim = y_abertura_inicio + corredor_altura # 490

        # 1. Obstáculo no topo da tela (y: 0 até 230)
        self.area_topo = pygame.Rect(centro_x, 0, espessura, y_abertura_inicio)

        # 2. Obstáculo na parte de baixo da tela (y: 490 até 720)
        self.area_baixo = pygame.Rect(centro_x, y_abertura_fim, espessura, altura - y_abertura_fim)

        self.obstaculos = [self.area_topo, self.area_baixo]

    def load(self):
        print("ping 4")
        return generate_fixed_level(qtd_pecas=2)

    def setup_obstacles(self, obstacle_system):
        """Registra as áreas de perigo no sistema de obstáculos."""
        obstacle_system.definir_areas(self.obstaculos)

    def obter_obstaculos(self):
        """Retorna a lista de retângulos dos obstáculos deste level."""
        return self.obstaculos

    def _desenhar_area_perigo(self, tela, rect, texto="PERIGO"):
        """Renderiza a área de perigo com efeitos visuais de pulsação e aviso."""
        ticks = pygame.time.get_ticks()
        pulso = int(25 * math.sin(ticks * 0.005))

        # 1. Aura / Brilho ao redor da área
        aura_rect = rect.inflate(14, 14)
        superficie_aura = pygame.Surface((aura_rect.width, aura_rect.height), pygame.SRCALPHA)
        alpha_aura = min(255, max(30, 75 + pulso * 2))
        pygame.draw.rect(superficie_aura, (240, 40, 40, alpha_aura), superficie_aura.get_rect(), border_radius=14)
        tela.blit(superficie_aura, aura_rect.topleft)

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

        # 5. Texto de aviso no centro da barreira
        if rect.height > 100:
            txt_sombra = self.fonte.render(texto, True, (0, 0, 0))
            txt_surf = self.fonte.render(texto, True, (255, 255, 255))
            txt_sombra_rot = pygame.transform.rotate(txt_sombra, 90)
            txt_surf_rot = pygame.transform.rotate(txt_surf, 90)

            c_x, c_y = rect.center
            tela.blit(txt_sombra_rot, txt_sombra_rot.get_rect(center=(c_x + 1, c_y + 1)))
            tela.blit(txt_surf_rot, txt_surf_rot.get_rect(center=(c_x, c_y)))

    def desenhar_obstaculos(self, tela):
        """Renderiza os obstáculos da Fase 4 na tela (topo e base)."""
        for area in self.obstaculos:
            self._desenhar_area_perigo(tela, area, texto="PERIGO")

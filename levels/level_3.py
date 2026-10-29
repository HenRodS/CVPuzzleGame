import pygame
import math
from systems.level_generator import generate_fixed_level

class Level3:
    tempo = 60
    usa_maos = False  # Flag: Fase nao utiliza diferenciacao de Mao Esquerda e Direita

    def __init__(self, largura=1280, altura=720):
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont("Arial", 16, bold=True)

        # Gera a área de obstáculo no meio da tela (barreira central vertical)
        # Deixa passagens livres no topo e na parte inferior
        espessura = 44
        abertura_superior = 230
        abertura_inferior = 230
        centro_x = (largura - espessura) // 2
        topo_y = abertura_superior
        altura_barreira = max(50, altura - abertura_superior - abertura_inferior)

        self.area_obstaculo = pygame.Rect(centro_x, topo_y, espessura, altura_barreira)
        self.obstaculos = [self.area_obstaculo]

    def load(self):
        print("ping 3")
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
        """Renderiza os obstáculos da Fase 3 na tela."""
        for area in self.obstaculos:
            self._desenhar_area_perigo(tela, area, texto="PERIGO")

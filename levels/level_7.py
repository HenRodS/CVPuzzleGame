import pygame
import math
from systems.level_generator import generate_fixed_level

class Level7:
    tempo = 60

    def __init__(self, largura=1280, altura=720):
        self.largura = largura
        self.altura = altura
        self.fonte_aviso = pygame.font.SysFont("Arial", 18, bold=True)

        # Barreira central no meio da tela (deixa passagens livres no topo e na base)
        espessura = 44
        centro_x = (largura - espessura) // 2
        y_inicio = 230
        altura_barreira = 260

        self.obstaculo_centro = pygame.Rect(centro_x, y_inicio, espessura, altura_barreira)
        self.obstaculos = [self.obstaculo_centro]

    def load(self):
        print("ping 7")
        pieces = generate_fixed_level(qtd_pecas=2, w=150, h=150)
        if len(pieces) >= 2:
            # 1. Peça superior com BORDA VERMELHA (apenas MÃO ESQUERDA)
            pieces[0].required_hand = "Left"
            pieces[0].border_color = (240, 45, 45)

            # 2. Peça inferior com BORDA AZUL (apenas MÃO DIREITA)
            pieces[1].required_hand = "Right"
            pieces[1].border_color = (35, 135, 255)

        return pieces

    def setup_obstacles(self, obstacle_system):
        """Registra as áreas de perigo no sistema de obstáculos."""
        obstacle_system.definir_areas(self.obstaculos)

    def obter_obstaculos(self):
        """Retorna a lista de obstáculos deste level."""
        return self.obstaculos

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

    def _desenhar_painel_instrucao(self, tela):
        """Exibe um banner superior instruindo o jogador sobre as mãos requeridas."""
        # Fundo do banner no topo central
        banner_w, banner_h = 560, 36
        banner_x = (self.largura - banner_w) // 2
        banner_y = 10

        s = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        tela.blit(s, (banner_x, banner_y))
        pygame.draw.rect(tela, (100, 100, 100), (banner_x, banner_y, banner_w, banner_h), width=1, border_radius=8)

        # Texto Vermelho: Mão Esquerda
        txt_esq = self.fonte_aviso.render("MÃO ESQUERDA: PEÇA VERMELHA", True, (255, 70, 70))
        tela.blit(txt_esq, (banner_x + 16, banner_y + 8))

        # Divisor
        txt_div = self.fonte_aviso.render("|", True, (180, 180, 180))
        tela.blit(txt_div, (banner_x + 295, banner_y + 8))

        # Texto Azul: Mão Direita
        txt_dir = self.fonte_aviso.render("MÃO DIREITA: PEÇA AZUL", True, (70, 160, 255))
        tela.blit(txt_dir, (banner_x + 315, banner_y + 8))

    def desenhar_obstaculos(self, tela):
        """Renderiza os obstáculos e a barra de instrução da Fase 7."""
        for area in self.obstaculos:
            self._desenhar_area_perigo(tela, area)

        self._desenhar_painel_instrucao(tela)

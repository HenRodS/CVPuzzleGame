import pygame
import math
import os
from objects.puzzle_piece import PuzzlePiece

class Level8:
    tempo = 75
    usa_maos = True  # Flag: Fase utiliza diferenciacao de Mao Esquerda e Direita

    def __init__(self, largura=1280, altura=720):
        self.largura = largura
        self.altura = altura
        self.fonte_status = pygame.font.SysFont("Arial", 16, bold=True)
        self.fonte_item = pygame.font.SysFont("Arial", 13, bold=True)
        self.tempo_inicio = None

        self.obstacle_system = None
        self.barreira_ativa = True
        self.pecas = []
        self.peca_vermelha = None
        self.peca_azul = None
        self.peca_neutra = None

        # Definição das 4 paredes da barreira cercada em volta do encaixe neutro
        # Encaixe neutro fica em: x = 565, y = 85 (tamanho alvo: 150x150, ocupando x: 565..715, y: 85..235)
        # Cage exterior: x: 515..765, y: 56..269
        self.parede_topo = pygame.Rect(515, 56, 250, 24)
        self.parede_baixo = pygame.Rect(515, 245, 250, 24)
        self.parede_esq = pygame.Rect(515, 56, 28, 213)
        self.parede_dir = pygame.Rect(737, 56, 28, 213)

        self.obstaculos = [
            self.parede_topo,
            self.parede_baixo,
            self.parede_esq,
            self.parede_dir
        ]

    def load(self):
        print("ping 8")
        self.tempo_inicio = pygame.time.get_ticks()
        base_path = "assets"
        pasta_origem = os.path.join(base_path, "imagesPNG")
        pasta_alvo = os.path.join(base_path, "imagesTarget")

        if not os.path.exists(pasta_origem):
            print(f"Erro: Pasta {pasta_origem} não encontrada!")
            return []

        files = sorted([f for f in os.listdir(pasta_origem) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        if not files:
            print("Erro: Nenhuma imagem encontrada para a Fase 8!")
            return []

        w, h = 140, 140

        # Escolhe 3 arquivos para as peças
        f_vermelha = files[0]
        f_azul = files[1 % len(files)]
        f_neutra = files[2 % len(files)]

        # 1. Peça Vermelha (Mão Esquerda)
        # Lado esquerdo: peça vermelha (origem [120, 150])
        # Lado direito: encaixe vermelho (alvo [1020, 430])
        self.peca_vermelha = PuzzlePiece(
            os.path.join(pasta_origem, f_vermelha),
            os.path.join(pasta_alvo, f_vermelha),
            posOrigin=[120, 150],
            posTarget=[1020, 430],
            width=w, height=h,
            required_hand="Left",
            border_color=(240, 45, 45)
        )
        self.peca_vermelha.badge_text = "MÃO ESQUERDA"
        self.peca_vermelha.target_badge_text = "ENCAIXE VERMELHO"

        # 2. Peça Azul (Mão Direita)
        # Lado direito: peça azul (origem [1020, 150])
        # Lado esquerdo: encaixe azul (alvo [120, 430])
        self.peca_azul = PuzzlePiece(
            os.path.join(pasta_origem, f_azul),
            os.path.join(pasta_alvo, f_azul),
            posOrigin=[1020, 150],
            posTarget=[120, 430],
            width=w, height=h,
            required_hand="Right",
            border_color=(35, 135, 255)
        )
        self.peca_azul.badge_text = "MÃO DIREITA"
        self.peca_azul.target_badge_text = "ENCAIXE AZUL"

        # 3. Peça Neutra (Ambas as Mãos - Mão Esquerda ou Direita)
        # Centro inferior: peça neutra (origem [565, 490])
        # Centro superior: encaixe neutro (alvo [565, 85], cercado por barreiras)
        self.peca_neutra = PuzzlePiece(
            os.path.join(pasta_origem, f_neutra),
            os.path.join(pasta_alvo, f_neutra),
            posOrigin=[565, 490],
            posTarget=[565, 85],
            width=w, height=h,
            required_hand=None,
            border_color=(245, 200, 35)
        )
        self.peca_neutra.badge_text = "AMBAS AS MÃOS"
        self.peca_neutra.target_badge_text = None

        self.pecas = [self.peca_vermelha, self.peca_azul, self.peca_neutra]
        return self.pecas

    def setup_obstacles(self, obstacle_system):
        """Registra as 4 barreiras em volta do encaixe neutro no sistema de obstáculos."""
        self.obstacle_system = obstacle_system
        self.barreira_ativa = True
        self.obstacle_system.definir_areas(self.obstaculos)

    def obter_obstaculos(self):
        """Retorna os obstáculos caso a barreira esteja ativa."""
        return self.obstaculos if self.barreira_ativa else []

    def _desenhar_area_perigo(self, tela, rect):
        """Renderiza a barreira com efeitos visuais de pulsação e aviso."""
        ticks = pygame.time.get_ticks()
        pulso = int(25 * math.sin(ticks * 0.005))

        # 1. Corpo principal com cor dinâmica pulsante
        r = min(255, max(0, 200 + pulso))
        cor_corpo = (r, 35, 45)
        pygame.draw.rect(tela, cor_corpo, rect, border_radius=8)

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
        pygame.draw.rect(tela, (255, 90, 90), rect, width=3, border_radius=8)

    def _desenhar_painel_instrucao(self, tela):
        """Exibe o status das peças e aviso sobre as barreiras (some após 10s)."""
        if self.tempo_inicio is None:
            self.tempo_inicio = pygame.time.get_ticks()

        # Some após 10 segundos
        tempo_passado = (pygame.time.get_ticks() - self.tempo_inicio) / 1000.0
        if tempo_passado >= 10.0:
            return

        # Fundo do banner na parte de baixo no centro da tela, próximo da borda
        banner_w, banner_h = 680, 48
        banner_x = (self.largura - banner_w) // 2
        banner_y = self.altura - banner_h - 15

        s = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 195))
        tela.blit(s, (banner_x, banner_y))

        if self.barreira_ativa:
            # Borda de aviso
            cor_borda = (230, 80, 80)
            pygame.draw.rect(tela, cor_borda, (banner_x, banner_y, banner_w, banner_h), width=2, border_radius=8)

            txt_titulo = self.fonte_status.render("BARREIRA ATIVA: ENCAIXE AS PEÇAS VERMELHA E AZUL", True, (255, 210, 80))
            tela.blit(txt_titulo, (banner_x + (banner_w - txt_titulo.get_width()) // 2, banner_y + 4))

            # Status Peça Vermelha
            v_ok = self.peca_vermelha.isMatched if self.peca_vermelha else False
            cor_v = (70, 240, 100) if v_ok else (255, 90, 90)
            txt_v = "[OK] VERMELHA" if v_ok else "[X] VERMELHA (MÃO ESQ)"
            surf_v = self.fonte_item.render(txt_v, True, cor_v)
            tela.blit(surf_v, (banner_x + 80, banner_y + 26))

            # Divisor
            txt_div = self.fonte_item.render("|", True, (150, 150, 150))
            tela.blit(txt_div, (banner_x + 335, banner_y + 26))

            # Status Peça Azul
            a_ok = self.peca_azul.isMatched if self.peca_azul else False
            cor_a = (70, 240, 100) if a_ok else (70, 160, 255)
            txt_a = "[OK] AZUL" if a_ok else "[X] AZUL (MÃO DIR)"
            surf_a = self.fonte_item.render(txt_a, True, cor_a)
            tela.blit(surf_a, (banner_x + 390, banner_y + 26))
        else:
            # Barreira aberta / desbloqueada
            cor_borda = (50, 220, 120)
            pygame.draw.rect(tela, cor_borda, (banner_x, banner_y, banner_w, banner_h), width=2, border_radius=8)

            txt_liberada = self.fonte_status.render("BARREIRA DESATIVADA! ENCAIXE A PEÇA NEUTRA", True, (80, 255, 140))
            tela.blit(txt_liberada, (banner_x + (banner_w - txt_liberada.get_width()) // 2, banner_y + 6))

            txt_sub = self.fonte_item.render("A peça neutra pode ser movida com qualquer mão (Esq ou Dir)", True, (230, 230, 230))
            tela.blit(txt_sub, (banner_x + (banner_w - txt_sub.get_width()) // 2, banner_y + 26))

    def desenhar_obstaculos(self, tela):
        """Atualiza estado das barreiras e desenha na tela."""
        # 1. Se ambas as peças (vermelha e azul) encaixaram, desativa as barreiras
        if self.barreira_ativa:
            ambas_encaixadas = (
                self.peca_vermelha is not None and self.peca_vermelha.isMatched and
                self.peca_azul is not None and self.peca_azul.isMatched
            )
            if ambas_encaixadas:
                self.barreira_ativa = False
                if self.obstacle_system is not None:
                    self.obstacle_system.limpar()

        # 2. Renderiza barreiras se estiverem ativas
        if self.barreira_ativa:
            for area in self.obstaculos:
                self._desenhar_area_perigo(tela, area)
        elif self.peca_neutra and not self.peca_neutra.isMatched:
            # Efeito de destaque no alvo liberado
            ticks = pygame.time.get_ticks()
            pulso_alvo = int(4 * math.sin(ticks * 0.008))
            halo_rect = pygame.Rect(565 - 6 - pulso_alvo, 85 - 6 - pulso_alvo, 150 + 12 + pulso_alvo * 2, 150 + 12 + pulso_alvo * 2)
            s_halo = pygame.Surface((halo_rect.width, halo_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s_halo, (50, 255, 120, 50), s_halo.get_rect(), border_radius=14)
            tela.blit(s_halo, halo_rect.topleft)
            pygame.draw.rect(tela, (80, 255, 140), halo_rect, width=2, border_radius=14)

        # 3. Painel de status e instrução
        self._desenhar_painel_instrucao(tela)
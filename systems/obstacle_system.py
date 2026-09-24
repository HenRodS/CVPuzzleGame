import pygame
import math

class Obstacle:
    """Representa um obstáculo/barreira que causa derrota ao colidir com uma peça."""
    def __init__(self, rect, cor=(200, 35, 45), cor_borda=(255, 90, 90), texto="PERIGO"):
        self.rect = pygame.Rect(rect)
        self.cor = cor
        self.cor_borda = cor_borda
        self.texto = texto
        self.fonte = pygame.font.SysFont("Arial", 16, bold=True)

    def colidiu(self, rect_peca, tolerancia=14):
        """
        Verifica se houve colisão com a peça.
        Usa tolerância interna para evitar falsos positivos nas bordas transparentes do PNG.
        """
        rect_ajustado = rect_peca.inflate(-tolerancia * 2, -tolerancia * 2)
        return self.rect.colliderect(rect_ajustado)

    def desenhar(self, tela):
        """Renderiza a barreira com efeitos visuais de pulsação e aviso."""
        ticks = pygame.time.get_ticks()
        pulso = int(25 * math.sin(ticks * 0.005))
        
        # 1. Brilho / Aura ao redor da barreira
        aura_rect = self.rect.inflate(14, 14)
        superficie_aura = pygame.Surface((aura_rect.width, aura_rect.height), pygame.SRCALPHA)
        alpha_aura = min(255, max(30, 75 + pulso * 2))
        pygame.draw.rect(superficie_aura, (240, 40, 40, alpha_aura), superficie_aura.get_rect(), border_radius=14)
        tela.blit(superficie_aura, aura_rect.topleft)

        # 2. Corpo principal com cor dinâmica pulsante
        r = min(255, max(0, self.cor[0] + pulso))
        cor_corpo = (r, self.cor[1], self.cor[2])
        pygame.draw.rect(tela, cor_corpo, self.rect, border_radius=10)

        # 3. Faixas diagonais estilo perigo/hazard
        largura_listra = 8
        espaco = 28
        # Define clip para não vazar do retângulo
        clip_anterior = tela.get_clip()
        tela.set_clip(self.rect)
        for offset_y in range(-self.rect.width * 2, self.rect.height + self.rect.width * 2, espaco):
            p1 = (self.rect.left - 10, self.rect.top + offset_y)
            p2 = (self.rect.right + 10, self.rect.top + offset_y + self.rect.width + 20)
            pygame.draw.line(tela, (110, 15, 20), p1, p2, width=largura_listra)
        tela.set_clip(clip_anterior)

        # 4. Borda externa brilhante
        pygame.draw.rect(tela, self.cor_borda, self.rect, width=3, border_radius=10)

        # 5. Texto de aviso no centro da barreira
        if self.rect.height > 100:
            txt_sombra = self.fonte.render(self.texto, True, (0, 0, 0))
            txt_surf = self.fonte.render(self.texto, True, (255, 255, 255))
            txt_sombra_rot = pygame.transform.rotate(txt_sombra, 90)
            txt_surf_rot = pygame.transform.rotate(txt_surf, 90)
            
            c_x, c_y = self.rect.center
            tela.blit(txt_sombra_rot, txt_sombra_rot.get_rect(center=(c_x + 1, c_y + 1)))
            tela.blit(txt_surf_rot, txt_surf_rot.get_rect(center=(c_x, c_y)))


class ObstacleSystem:
    """Sistema isolado e modular para controle, geração e colisão de obstáculos em qualquer fase."""
    def __init__(self):
        self.obstaculos = []
        self.ativo = False

    def iniciar(self, obstaculos=None):
        """Ativa o sistema e opcionalmente define a lista de obstáculos."""
        if obstaculos is not None:
            self.obstaculos = list(obstaculos)
        self.ativo = True

    def adicionar_obstaculo(self, obstaculo):
        """Adiciona um obstáculo customizado."""
        self.obstaculos.append(obstaculo)
        self.ativo = True

    def adicionar_barreira(self, x, y, largura, altura, texto="PERIGO"):
        """Cria e adiciona uma barreira retangular."""
        obs = Obstacle((x, y, largura, altura), texto=texto)
        self.adicionar_obstaculo(obs)
        return obs

    def configurar_barreira_vertical_fase3(self, largura_tela=1280, altura_tela=720, espessura=44, abertura_superior=230, abertura_inferior=230):
        """
        Configura a barreira vertical no meio da tela para a Fase 3.
        Deixa corredores de passagem nos cantos superior e inferior.
        """
        self.limpar()
        centro_x = (largura_tela - espessura) // 2
        topo_y = abertura_superior
        altura_barreira = max(50, altura_tela - abertura_superior - abertura_inferior)

        self.adicionar_barreira(centro_x, topo_y, espessura, altura_barreira, texto="PERIGO")
        self.ativo = True

    def limpar(self):
        """Remove todos os obstáculos e desativa o sistema."""
        self.obstaculos.clear()
        self.ativo = False

    def parar(self):
        """Alias para limpar/desativar o sistema."""
        self.limpar()

    def esta_ativo(self):
        """Retorna se há obstáculos ativos."""
        return self.ativo and len(self.obstaculos) > 0

    def verificar_colisao(self, lista_pecas):
        """
        Verifica se alguma peça não encaixada colidiu com qualquer barreira.
        Retorna True se houve colisão (resultando em derrota).
        """
        if not self.ativo or not self.obstaculos:
            return False

        for peca in lista_pecas:
            # Peças já encaixadas no alvo não sofrem colisão
            if not getattr(peca, 'isMatched', False):
                for obs in self.obstaculos:
                    if obs.colidiu(peca.rect):
                        return True
        return False

    def desenhar(self, tela):
        """Desenha todos os obstáculos cadastrados."""
        if not self.ativo:
            return

        for obs in self.obstaculos:
            obs.desenhar(tela)

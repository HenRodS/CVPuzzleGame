import pygame

class Button:
    def __init__(self, texto, pos, size, cor_base=(50, 50, 50), cor_hover=(0, 200, 0)):
        self.texto = texto
        self.rect = pygame.Rect(pos, size)
        self.cor_base = cor_base
        self.cor_hover = cor_hover
        self.fonte = pygame.font.SysFont("Arial", 32, bold = True)

    def desenhar(self, tela, cursor):
        # verifica a colisao
        colisao = self.rect.collidepoint(cursor)
        cor = self.cor_hover if colisao else self.cor_base

        # desenho do botão
        pygame.draw.rect(tela, (20, 20, 20), (self.rect.x + 5, self.rect.y + 5, self.rect.w, self.rect.h), border_radius=12)
        pygame.draw.rect(tela, cor, self.rect, border_radius=12)
        pygame.draw.rect(tela, (255, 255, 255), self.rect, 3, border_radius=12)

        # renderiza o texto centralizado
        txt_surf = self.fonte.render(self.texto, True, (255,255,255))
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        tela.blit(txt_surf, txt_rect)

        return colisao
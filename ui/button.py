import pygame

class Button:
    def __init__(self, texto, pos, size, cor_base=(50, 50, 50), cor_hover=(0, 200, 0), cor_click=(0, 240, 100)):
        self.texto = texto
        self.rect = pygame.Rect(pos, size)
        self.cor_base = cor_base
        self.cor_hover = cor_hover
        self.cor_click = cor_click
        self.fonte = pygame.font.SysFont("Arial", 32, bold=True)

    def desenhar(self, tela, cursor, click=False):
        # Verifica se o cursor está sobre o botão
        colisao = self.rect.collidepoint(cursor)

        # O clique só é registrado se o gesto de clique ocorrer ENCIMA deste botão
        clicou_no_botao = colisao and click

        # Feedback visual: normal, hover ou clique ativo
        if clicou_no_botao:
            cor = self.cor_click
            offset = 2
        elif colisao:
            cor = self.cor_hover
            offset = 0
        else:
            cor = self.cor_base
            offset = 0

        # Sombra do botão
        pygame.draw.rect(tela, (20, 20, 20), (self.rect.x + 5, self.rect.y + 5, self.rect.w, self.rect.h), border_radius=12)

        # Corpo do botão com leve deslocamento no clique para efeito tátil
        rect_desenho = pygame.Rect(self.rect.x + offset, self.rect.y + offset, self.rect.w, self.rect.h)
        pygame.draw.rect(tela, cor, rect_desenho, border_radius=12)
        pygame.draw.rect(tela, (255, 255, 255), rect_desenho, 3, border_radius=12)

        # Renderiza o texto centralizado
        txt_surf = self.fonte.render(self.texto, True, (255, 255, 255))
        txt_rect = txt_surf.get_rect(center=rect_desenho.center)
        tela.blit(txt_surf, txt_rect)

        return clicou_no_botao

import pygame
from ui.button import Button

btn_fases = Button("FASES", (515, 250), (250, 70))
btn_sair = Button("SAIR", (515, 450), (250, 70))

def tela_menu_pygame(tela, largura_tela, cursor, click):
    # titulo
    fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
    titulo = fonte_titulo.render("MENU PRINCIPAL", True, (255,255,0))
    tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 100))

    if btn_fases.desenhar(tela, cursor) and click:
        return "fases"
    
    if btn_sair.desenhar(tela, cursor) and click:
        return "sair"
    
    return "menu"
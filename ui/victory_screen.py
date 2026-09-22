import pygame
from ui.button import Button

def tela_vitoria_pygame(tela, largura_tela, cursor, click):
    # tela com transparencia
    s = pygame.Surface((1280,720))
    s.set_alpha(180) # Nivel de transparencia
    s.fill((0,0,0))
    tela.blit(s, (0,0))

    # Texto de vitoria
    fonte_vitoria = pygame.font.SysFont("Arial", 50, bold=True)
    msg = fonte_vitoria.render("PARABÉNS, VOCÊ VENCEU!", True, (0,255,0))
    tela.blit(msg, (largura_tela // 2 - msg.get_width() // 2, 300))

    btn_cont = Button("CONTINUAR", (500, 450), (280, 80), cor_base=(0,150,0))
    if btn_cont.desenhar(tela, cursor) and click:
        return True # Indica que clicou para continuar
    
    return False
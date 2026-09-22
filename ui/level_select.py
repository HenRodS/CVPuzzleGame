import pygame
from ui.button import Button

# Instancia os botoes de fase (melhorar isso)
btn_fase1 = Button("FASE 1", (200, 250), (200, 60))
btn_fase2 = Button("FASE 2", (450, 250), (200, 60))
btn_fase3 = Button("FASE 3", (700, 250), (200, 60))
btn_voltar = Button("VOLTAR", (540, 600), (200, 60), cor_base=(100, 100, 100))

def tela_fases_pygame(tela, largura_tela, cursor, click):
    # titulo centralizado
    # Explicação: Faz a superficie do titulo (titulo_surf) e "coloca" ela encima da moldura correta (titulo_rect)
    fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
    titulo_surf = fonte_titulo.render("MENU PRINCIPAL", True, (255,255,0))

    titulo_rect = titulo_surf.get_rect(center=(largura_tela // 2, 100))
    tela.blit(titulo_surf, titulo_rect) # blit é a funcao que "carimba" uma superficie numa posicao especifica
    

    # Renderiza os botoes
    if btn_fase1.desenhar(tela, cursor) and click:
        return "jogando", 1 # indica o numero de peças
    
    if btn_fase2.desenhar(tela, cursor) and click:
        return "jogando", 2
    
    if btn_fase3.desenhar(tela, cursor) and click:
        return "jogando", 3

    if btn_voltar.desenhar(tela, cursor) and click:
        return "menu", None
    
    return "fases", None
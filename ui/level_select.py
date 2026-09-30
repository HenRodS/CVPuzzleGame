import pygame
from ui.button import Button

# Instancia os botões das fases e botão voltar
btn_fase1 = Button("FASE 1", (235, 230), (180, 55))
btn_fase2 = Button("FASE 2", (445, 230), (180, 55))
btn_fase3 = Button("FASE 3", (655, 230), (180, 55))
btn_fase4 = Button("FASE 4", (865, 230), (180, 55))
btn_fase5 = Button("FASE 5", (340, 310), (180, 55))
btn_fase6 = Button("FASE 6", (550, 310), (180, 55))
btn_fase7 = Button("FASE 7", (760, 310), (180, 55))
btn_voltar = Button("VOLTAR", (540, 480), (200, 55), cor_base=(100, 100, 100))

def tela_fases_pygame(tela, largura_tela, cursor, click):
    fonte_titulo = pygame.font.SysFont("Arial", 56, bold=True)
    titulo_surf = fonte_titulo.render("SELEÇÃO DE FASES", True, (255, 255, 0))
    titulo_rect = titulo_surf.get_rect(center=(largura_tela // 2, 90))
    tela.blit(titulo_surf, titulo_rect)

    fonte_sub = pygame.font.SysFont("Arial", 22)
    sub_surf = fonte_sub.render("Escolha uma fase para iniciar o desafio", True, (220, 220, 220))
    sub_rect = sub_surf.get_rect(center=(largura_tela // 2, 150))
    tela.blit(sub_surf, sub_rect)

    # Renderiza os botões
    if btn_fase1.desenhar(tela, cursor) and click:
        return "jogando", 1

    if btn_fase2.desenhar(tela, cursor) and click:
        return "jogando", 2

    if btn_fase3.desenhar(tela, cursor) and click:
        return "jogando", 3

    if btn_fase4.desenhar(tela, cursor) and click:
        return "jogando", 4

    if btn_fase5.desenhar(tela, cursor) and click:
        return "jogando", 5

    if btn_fase6.desenhar(tela, cursor) and click:
        return "jogando", 6

    if btn_fase7.desenhar(tela, cursor) and click:
        return "jogando", 7

    if btn_voltar.desenhar(tela, cursor) and click:
        return "menu", None

    return "fases", None
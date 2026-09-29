import pygame
from ui.button import Button

# Instancia os botões das fases e botão voltar
btn_fase1 = Button("FASE 1", (170, 270), (160, 60))
btn_fase2 = Button("FASE 2", (365, 270), (160, 60))
btn_fase3 = Button("FASE 3", (560, 270), (160, 60))
btn_fase4 = Button("FASE 4", (755, 270), (160, 60))
btn_fase5 = Button("FASE 5", (950, 270), (160, 60))
btn_voltar = Button("VOLTAR", (540, 520), (200, 60), cor_base=(100, 100, 100))

def tela_fases_pygame(tela, largura_tela, cursor, click):
    fonte_titulo = pygame.font.SysFont("Arial", 56, bold=True)
    titulo_surf = fonte_titulo.render("SELEÇÃO DE FASES", True, (255, 255, 0))
    titulo_rect = titulo_surf.get_rect(center=(largura_tela // 2, 100))
    tela.blit(titulo_surf, titulo_rect)

    fonte_sub = pygame.font.SysFont("Arial", 22)
    sub_surf = fonte_sub.render("Escolha uma fase para iniciar o desafio", True, (220, 220, 220))
    sub_rect = sub_surf.get_rect(center=(largura_tela // 2, 160))
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

    if btn_voltar.desenhar(tela, cursor) and click:
        return "menu", None

    return "fases", None
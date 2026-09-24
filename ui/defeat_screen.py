import pygame
from ui.button import Button

btn_tentar = Button("TENTAR NOVAMENTE", (340, 440), (280, 70), cor_base=(180, 40, 40), cor_hover=(220, 60, 60))
btn_fases = Button("FASES", (660, 440), (280, 70), cor_base=(70, 70, 70), cor_hover=(110, 110, 110))

def tela_derrota_pygame(tela, largura_tela, cursor, click, motivo="tempo"):
    """
    Renderiza a tela de derrota quando o tempo se esgota ou ocorre colisão com obstáculo.
    Retorna:
        - "reiniciar" se clicou em 'Tentar Novamente'
        - "fases" se clicou em 'Fases'
        - None se nenhuma ação foi confirmada
    """
    # Fundo escuro semi-transparente
    s = pygame.Surface((largura_tela, 720))
    s.set_alpha(190)
    s.fill((0, 0, 0))
    tela.blit(s, (0, 0))

    # Título e subtítulo dinâmicos conforme o motivo da derrota
    fonte_titulo = pygame.font.SysFont("Arial", 50, bold=True)
    fonte_sub = pygame.font.SysFont("Arial", 24)

    if motivo == "obstaculo":
        msg_titulo = fonte_titulo.render("COLISÃO COM BARREIRA!", True, (255, 60, 60))
        msg_sub = fonte_sub.render("Uma peça colidiu com o obstáculo! Guie as peças pelos cantos.", True, (220, 220, 220))
    else:
        msg_titulo = fonte_titulo.render("TEMPO ESGOTADO!", True, (255, 60, 60))
        msg_sub = fonte_sub.render("A fase falhou! Você não conseguiu encaixar as peças a tempo.", True, (220, 220, 220))

    tela.blit(msg_titulo, (largura_tela // 2 - msg_titulo.get_width() // 2, 240))
    tela.blit(msg_sub, (largura_tela // 2 - msg_sub.get_width() // 2, 320))

    # Botões interativos
    if btn_tentar.desenhar(tela, cursor) and click:
        return "reiniciar"

    if btn_fases.desenhar(tela, cursor) and click:
        return "fases"

    return None

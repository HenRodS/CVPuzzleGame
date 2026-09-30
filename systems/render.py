import pygame

def draw_game(tela, pieces):
    # 1. Desenha os alvos (Targets)
    for piece in pieces:
        tela.blit(piece.spriteTarget, piece.posTarget)
        border_color = getattr(piece, 'border_color', None)
        if border_color:
            target_rect = pygame.Rect(piece.posTarget[0], piece.posTarget[1], piece.size[0] + 10, piece.size[1] + 10)
            pygame.draw.rect(tela, border_color, target_rect, width=3, border_radius=12)

    # 2. Desenha as peças com borda colorida e badge de mão se aplicável
    for piece in pieces:
        tela.blit(piece.sprite, piece.rect.topleft)
        border_color = getattr(piece, 'border_color', None)
        if border_color:
            # Borda ao redor da peça
            pygame.draw.rect(tela, border_color, piece.rect, width=4, border_radius=10)

            # Badge indicando a mão requerida acima da peça (enquanto não estiver encaixada)
            req_hand = getattr(piece, 'required_hand', None)
            if req_hand and not piece.isMatched:
                texto_mao = "MÃO ESQUERDA" if req_hand.lower() == "left" else "MÃO DIREITA"
                fonte = pygame.font.SysFont("Arial", 12, bold=True)
                surf_txt = fonte.render(texto_mao, True, (255, 255, 255))
                w_badge = surf_txt.get_width() + 12
                h_badge = 20
                badge_rect = pygame.Rect(piece.rect.centerx - w_badge // 2, piece.rect.top - 24, w_badge, h_badge)
                pygame.draw.rect(tela, border_color, badge_rect, border_radius=6)
                tela.blit(surf_txt, (badge_rect.x + 6, badge_rect.y + 2))
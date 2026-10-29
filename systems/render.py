import pygame

def draw_game(tela, pieces):
    # 1. Desenha os alvos (Targets)
    for piece in pieces:
        tela.blit(piece.spriteTarget, piece.posTarget)
        border_color = getattr(piece, 'border_color', None)
        target_color = getattr(piece, 'target_border_color', border_color)
        if target_color:
            target_rect = pygame.Rect(piece.posTarget[0], piece.posTarget[1], piece.size[0] + 10, piece.size[1] + 10)
            pygame.draw.rect(tela, target_color, target_rect, width=3, border_radius=12)

            # Badge do alvo se configurado
            target_badge = getattr(piece, 'target_badge_text', None)
            if target_badge and not piece.isMatched:
                fonte_alvo = pygame.font.SysFont("Arial", 11, bold=True)
                surf_alvo = fonte_alvo.render(target_badge, True, (255, 255, 255))
                w_alvo = surf_alvo.get_width() + 10
                h_alvo = 18
                badge_alvo_rect = pygame.Rect(target_rect.centerx - w_alvo // 2, target_rect.top - 20, w_alvo, h_alvo)
                pygame.draw.rect(tela, target_color, badge_alvo_rect, border_radius=5)
                tela.blit(surf_alvo, (badge_alvo_rect.x + 5, badge_alvo_rect.y + 1))

    # 2. Desenha as peças com borda colorida e badge de mão se aplicável
    for piece in pieces:
        tela.blit(piece.sprite, piece.rect.topleft)
        border_color = getattr(piece, 'border_color', None)
        if border_color:
            # Borda ao redor da peça
            pygame.draw.rect(tela, border_color, piece.rect, width=4, border_radius=10)
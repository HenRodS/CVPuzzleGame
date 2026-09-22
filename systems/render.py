def draw_game(tela, pieces):

    for piece in pieces:
        tela.blit(piece.spriteTarget, piece.posTarget)

    for piece in pieces:
        tela.blit(piece.sprite, piece.rect.topleft)
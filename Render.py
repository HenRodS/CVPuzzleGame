import pygame


def renderizar_jogo(tela, listPiece):
    contador = 0
    
    # CAMADA 1: Todos os alvos ao fundo
    for obj in listPiece:
        tela.blit(obj.spriteTarget, obj.posTarget)
        pygame.draw.rect(tela, obj.color, (obj.posTarget[0], obj.posTarget[1], obj.size[0], obj.size[1]), 2)

    # CAMADA 2: Todas as peças à frente
    for obj in listPiece:
        tela.blit(obj.sprite, obj.rect.topleft)
        # Se encaixou, borda verde. Se não, cor aleatória.
        cor = (0, 255, 0) if obj.isMatched else obj.color
        pygame.draw.rect(tela, cor, obj.rect, 2)
        
        if obj.isMatched:
            contador += 1
            
    return contador
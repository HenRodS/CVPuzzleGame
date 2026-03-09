import pygame


def renderizar_jogo(tela, listImg):
    contador = 0
    
    # CAMADA 1: Todos os alvos ao fundo
    for obj in listImg:
        tela.blit(obj.imgTarget, obj.posTarget)
        pygame.draw.rect(tela, obj.color, (obj.posTarget[0], obj.posTarget[1], obj.size[0], obj.size[1]), 2)

    # CAMADA 2: Todas as peças à frente
    for obj in listImg:
        tela.blit(obj.img, obj.rect.topleft)
        # Se encaixou, borda verde. Se não, cor aleatória.
        cor = (0, 255, 0) if obj.isMatched else obj.color
        pygame.draw.rect(tela, cor, obj.rect, 2)
        
        if obj.isMatched:
            contador += 1
            
    return contador
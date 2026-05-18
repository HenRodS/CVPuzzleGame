import pygame
import random

class PuzzlePiece():
    def __init__(self, path, pathTarget, posOrigin, posTarget, width=200, height=200):
        self.path = path
        self.pathTarget = pathTarget
        self.isMatched = False  # Indica se já encaixou

        # Carrega a imagem
        self.sprite = pygame.image.load(self.path).convert_alpha()
        self.spriteTarget = pygame.image.load(self.pathTarget).convert_alpha()

        # 2. Redimensiona
        self.sprite = pygame.transform.smoothscale(self.sprite, (width, height))
        self.spriteTarget = pygame.transform.smoothscale(self.spriteTarget, (width + 10, height + 10))
    
        self.size = (width, height)
        self.posOrigin = list(posOrigin) # Converte para lista para poder alterar x e y
        self.posTarget = list(posTarget)

        # cria um Rect para facilitar a detecção de clicks e o movimento
        self.rect = self.sprite.get_rect(topleft=self.posOrigin)

        # Gera uma cor aleatoria
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self, cursor):
        if self.isMatched: return  # Se já encaixou, não move mais

        # Verifica se o cursor colidiu com a imagem
        if self.rect.collidepoint(cursor):
            self.rect.center = cursor
            self.posOrigin = list(self.rect.topleft)

            # logica de encaixe (snap)
            tx, ty = self.posTarget
            distancia_x = abs(self.rect.x - tx)
            distancia_y = abs(self.rect.y - ty)

            if distancia_x < 50 and distancia_y < 50:
                # Ajusta perfeitamente ao alvo
                self.rect.x = tx + 5
                self.rect.y = ty + 5
                self.posOrigin = list(self.rect.topleft)
                self.isMatched = True
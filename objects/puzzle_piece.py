import pygame
import random

class PuzzlePiece():
    def __init__(self, path, pathTarget, posOrigin, posTarget, width=200, height=200, required_hand=None, border_color=None):
        self.path = path
        self.pathTarget = pathTarget
        self.isMatched = False  # Indica se já encaixou
        self.dragged_by = None   # Mão que está arrastando atualmente ("Left", "Right" ou None)
        self.required_hand = required_hand  # "Left", "Right" ou None (qualquer mão)

        # Se não fornecida explicitamente, define a cor da borda com base na mão requerida
        if border_color is None and required_hand is not None:
            if required_hand.lower() == "left":
                self.border_color = (240, 45, 45)    # Vermelho para mão esquerda
            elif required_hand.lower() == "right":
                self.border_color = (35, 135, 255)   # Azul para mão direita
            else:
                self.border_color = None
        else:
            self.border_color = border_color

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

    def can_be_moved_by(self, hand_type):
        """Verifica se esta peça pode ser manipulada pela mão especificada ('Left' ou 'Right')."""
        if self.isMatched:
            return False
        if self.required_hand is None:
            return True
        return self.required_hand.lower() == str(hand_type).lower()

    def update(self, cursor):
        if self.isMatched: return  # Se já encaixou, não move mais

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
            self.dragged_by = None
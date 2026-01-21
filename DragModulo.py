import cv2
import cvzone
import random

class DragImg():
    def __init__(self, path, pathTarget, posOrigin, posTarget, imgType, width=200, height=200):
        self.path = path
        self.pathTarget = pathTarget
        self.posOrigin = posOrigin  # Onde a imagem está agora
        self.posTarget = posTarget  # Onde ela deve ser encaixada
        self.imgType = imgType
        self.isMatched = False  # Indica se já encaixou

        # Carrega a imagem
        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
            self.imgTarget = cv2.imread(self.pathTarget, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)
            self.imgTarget = cv2.imread(self.pathTarget)

        # 2. Redimensiona para o tamanho padrão em pixels
        novo_tamanho = (width, height)  # (Largura, Altura)
        novo_tamanho_target = (width + 10, height + 10)
        self.img = cv2.resize(self.img, novo_tamanho, interpolation=cv2.INTER_AREA)
        self.imgTarget = cv2.resize(self.imgTarget, novo_tamanho_target, interpolation=cv2.INTER_AREA)

        # Gera uma cor aleatoria
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.size = self.img.shape[:2] # Tamanho da imagem
        self.sizeTarget = self.imgTarget.shape[:2]  # Tamanho da imagem_alvo (pode ser diferente)

    def update(self, cursor):
        if self.isMatched: return  # Se já encaixou, não move mais

        ox, oy = self.posOrigin
        h, w = self.size

        # Verifica se o dedo está sobre a imagem
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = [cursor[0] - w // 2, cursor[1] - h // 2]

            # Lógica de Encaixe (Snap)
            tx, ty = self.posTarget
            # Se a distância for menor que 50 pixels, encaixa no alvo
            if abs(self.posOrigin[0] - tx) < 50 and abs(self.posOrigin[1] - ty) < 50:
                self.posOrigin = [tx + 5, ty + 5]
                self.isMatched = True
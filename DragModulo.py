import cv2
import cvzone
import random

class DragImg():
    def __init__(self, path, posOrigin, posTarget, imgType, scale=1.0):
        self.path = path
        self.posOrigin = posOrigin  # Onde a imagem está agora
        self.posTarget = posTarget  # Onde ela deve ser encaixada
        self.imgType = imgType
        self.isMatched = False  # Indica se já encaixou

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        if scale != 1.0:
            h, w = self.img.shape[:2]
            newSize = (int(w * scale), int(h * scale))
            self.img = cv2.resize(self.img, newSize, interpolation=cv2.INTER_AREA)

        # Gera uma cor aleatoria
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.size = self.img.shape[:2]

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
                self.posOrigin = [tx, ty]
                self.isMatched = True
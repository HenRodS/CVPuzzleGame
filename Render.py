import cv2
import cvzone


def renderizar_jogo(img, listImg):
    """
    Desenha os alvos e as imagens na tela.
    Retorna o número de peças que já foram encaixadas.
    """
    contador = 0
    for imgObject in listImg:
        h, w = imgObject.size
        h_t, w_t = imgObject.sizeTarget  # Tamanho da imagem_alvo
        ox, oy = imgObject.posOrigin
        tx, ty = imgObject.posTarget

        # 1. Desenha a imagem_alvo (Target)
        if imgObject.imgType == 'png':
            img = cvzone.overlayPNG(img, imgObject.imgTarget, [tx, ty])
        else:
            img[ty:ty + h_t, tx:tx + w_t] = imgObject.imgTarget
            # Opcional: Borda ao redor do alvo para identificação
        cv2.rectangle(img, (tx, ty), (tx + w_t, ty + h_t), imgObject.color, 2)

        # 2. Desenha a Peça (Image)
        if imgObject.imgType == 'png':
            img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            # Borda para identificação
            cv2.rectangle(img, (ox, oy), (ox + w, oy + h), imgObject.color, 2)
        else:
            img[oy:oy + h, ox:ox + w] = imgObject.img

        # 3. Verifica encaixe
        if imgObject.isMatched:
            contador += 1

    return img, contador
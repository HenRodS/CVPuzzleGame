import cv2
from cvzone.HandTrackingModule import HandDetector

def processar_hand_input(detector: HandDetector, img, listImg: list, selectedImg, vitoria:bool):
    """
        Processa a imagem da câmera, detecta mãos, calcula cursor e clique,
        e faz a lógica de arraste dos objetos.

        Parâmetros:
            detector: Instância do HandDetector
            img: Frame atual da câmera (será modificado)
            listImg: Lista de objetos DragImg
            selectedImg: Objeto atualmente selecionado (ou None)
            vitoria: Se True, desativa a lógica de arraste

        Retorna:
            tuple: (img atualizada, cursor [x,y], clicou: bool, selectedImg atualizado)
        """
    hands, img = detector.findHands(img, flipType=False)

    cursor = [0, 0]
    clicou = False

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8][0:2]
        length, _, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)

        if length < 60:
            clicou = True

            # Lógica de arraste (só funciona se NÃO estiver na tela de vitória)
            if not vitoria:
                if selectedImg is None:
                    for imgObj in listImg:
                        ox, oy = imgObj.posOrigin
                        h, w = imgObj.size
                        if (ox < cursor[0] < ox + w) and (oy < cursor[1] < oy + h):
                            if not imgObj.isMatched:
                                selectedImg = imgObj
                                break
                if selectedImg:
                    selectedImg.update(cursor)
        else:
            selectedImg = None

    return img, cursor, clicou, selectedImg
import cv2
import cvzone
import random
import os
from cvzone.HandTrackingModule import HandDetector
from DragModulo import DragImg

# --- Configurações Iniciais ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)
MODO = 2
vitoria = False  # Controla se a tela de parabéns deve aparecer


# --- Função de Interface de Vitória ---
def tela_vitoria(img, cursor, click):
    """
    Desenha a tela de parabéns e o botão de continuar.
    Retorna True se o botão for clicado.
    """
    # 1. Overlay semi-transparente para escurecer o fundo (opcional)
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (1280, 720), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

    # 2. Texto de Parabéns (TROCAR PARA UMA IMAGEM)
    cvzone.putTextRect(img, "PARABENS! VOCE VENCEU", (350, 300), scale=4, thickness=4, colorR=(0, 200, 0))

    # 3. Configuração do Botão "Continuar"
    btn_x, btn_y, btn_w, btn_h = 500, 400, 280, 80
    cor_btn = (0, 255, 0)

    # Verifica se o cursor está sobre o botão
    if btn_x < cursor[0] < btn_x + btn_w and btn_y < cursor[1] < btn_y + btn_h:
        cor_btn = (0, 150, 0)  # Cor muda ao passar o mouse (feedback)
        if click:
            return True  # Botão clicado!

    # Desenha o botão
    cv2.rectangle(img, (btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h), cor_btn, cv2.FILLED)
    cv2.putText(img, "CONTINUAR", (btn_x + 35, btn_y + 55), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    return False

def inicializar(modo):
    img_list = []
    path = "ImagesPNG"
    files = os.listdir(path)

    if modo == 1:
        # MODO TESTE
        for x, nome in enumerate(files):
            imgType = 'png' if 'png' in nome else 'jpg'
            img_list.append(DragImg(f'{path}/{nome}', [100 + x * 200, 400], [100 + x * 200, 50], imgType, scale=0.5))

    elif modo == 2:
        # MODO JOGO
        escolhidos = random.sample(files, 2)
        for x, nome in enumerate(escolhidos):
            imgType = 'png' if 'png' in nome else 'jpg'

            # Criamos um objeto temporário para saber o tamanho da imagem (size)
            temp_obj = DragImg(f'{path}/{nome}', [0, 0], [0, 0], imgType, scale=0.5)
            h, w = temp_obj.size

            # --- VALIDAÇÃO DO ALVO (Target) ---
            tentativas = 0
            while tentativas < 50:  # Limite de tentativas para não travar o PC
                pos_alvo = [random.randint(100, 1000), random.randint(50, 250)]
                if not checar_overlap(pos_alvo, (w, h), img_list):
                    temp_obj.posTarget = pos_alvo
                    break
                tentativas += 1

            # --- VALIDAÇÃO DA POSIÇÃO INICIAL (Origin) ---
            tentativas = 0
            while tentativas < 50:
                pos_inicial = [random.randint(100, 1000), random.randint(400, 600)]
                # Aqui você pode checar contra as posições iniciais já definidas
                if not any(
                        not (pos_inicial[0] + w < obj.posOrigin[0] or pos_inicial[0] > obj.posOrigin[0] + obj.size[1] or \
                             pos_inicial[1] + h < obj.posOrigin[1] or pos_inicial[1] > obj.posOrigin[1] + obj.size[0])
                        for obj in img_list):
                    temp_obj.posOrigin = pos_inicial
                    break
                tentativas += 1

            img_list.append(temp_obj)

    return img_list


def checar_overlap(new_pos, size, existing_list):
    nx, ny = new_pos
    nw, nh = size
    for imgObj in existing_list:
        ex, ey = imgObj.posTarget  # Ou posOrigin, dependendo do que quer validar
        ew, eh = imgObj.size

        # Lógica de intersecção de retângulos
        if not (nx + nw < ex or nx > ex + ew or ny + nh < ey or ny > ey + eh):
            return True  # Há sobreposição
    return False


listImg = inicializar(MODO)
selectedImg = None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    cursor = [0, 0]
    clicou = False

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8][0:2]
        p1 = lmList[8][0:2]
        p2 = lmList[12][0:2]
        length, info, img = detector.findDistance(p1, p2, img)

        if length < 60:
            clicou = True

            # Lógica de arraste (só funciona se NÃO estiver na tela de vitória)
            if not vitoria:
                if selectedImg is None:
                    for imgObj in listImg:
                        ox, oy = imgObj.posOrigin
                        h, w = imgObj.size
                        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
                            if not imgObj.isMatched:
                                selectedImg = imgObj
                                break
                if selectedImg:
                    selectedImg.update(cursor)
        else:
            selectedImg = None

    # --- Lógica de Jogo ---
    contador_encaixes = 0
    if not vitoria:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            tx, ty = imgObject.posTarget

            # Desenha alvos e imagens
            cv2.rectangle(img, (tx, ty), (tx + w, ty + h), imgObject.color, 2)
            if imgObject.imgType == 'png':
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
                # Desenha uma borda fina na imagem do objeto para identificar a cor correspondente (TEMPORARIO)
                cv2.rectangle(img, (ox, oy), (ox + w, oy + h), imgObject.color, 2)
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

            if imgObject.isMatched:
                contador_encaixes += 1

        if contador_encaixes == len(listImg) and len(listImg) > 0:
            vitoria = True

    # --- Lógica de Vitória ---
    if vitoria:
        if tela_vitoria(img, cursor, clicou):
            # Reset do jogo ao clicar em continuar
            listImg = inicializar(MODO)
            vitoria = False

    cv2.imshow('Video', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




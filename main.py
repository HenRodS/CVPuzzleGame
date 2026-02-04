import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import Interface
from ManagerJogo import inicializar
from Render import renderizar_jogo
from clickDetection import processar_hand_input

# --- Configurações Iniciais ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

estado = "menu"

detector = HandDetector(detectionCon=0.65)
MODO = 2
vitoria = False  # Controla se a tela de parabéns deve aparecer


listImg = inicializar(MODO)
selectedImg = None
flagFase = True

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, cursor, clicou, selectedImg = processar_hand_input(
        detector=detector,
        img=img,
        listImg=listImg,
        selectedImg=selectedImg,
        vitoria=vitoria
    )

    # MÁQUINA DE ESTADOS
    if estado == "menu":
        estado = Interface.tela_menu(img, cursor, clicou)
        if estado == "sair": break

    elif estado == "fases":
        estado, fase = Interface.tela_selecao_fases(img, cursor, clicou)

    elif estado == "opcoes":
        cvzone.putTextRect(img, "EM BREVE...", (500, 350))
        if Interface.desenhar_botao(img, "VOLTAR", (500, 500, 200, 60), cursor, clicou):
            estado = "menu"

    elif estado == "jogando":
        if flagFase:
            listImg = inicializar(MODO, fase)
            flagFase = False

        # --- Lógica de Jogo ---
        contador_encaixes = 0
        if not vitoria:
            img, contador_encaixes = renderizar_jogo(img, listImg)

            if contador_encaixes == len(listImg) and len(listImg) > 0:
                vitoria = True

        # --- Lógica de Vitória ---
        if vitoria:
            if Interface.tela_vitoria(img, cursor, clicou):
                # Reset do jogo ao clicar em continuar
                listImg = inicializar(MODO)
                vitoria = False
                flagFase = True
                selectedImg = None
                estado = "fases" # volta ao inicio
        pass


    cv2.imshow('Video', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import Interface
from ManagerJogo import ManagerJogo
from Render import renderizar_jogo
from clickDetection import processar_hand_input

# --- Configurações Iniciais ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.65)

game = ManagerJogo(modo=2)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, cursor, clicou, game.selectedImg = processar_hand_input(
        detector, img, game.listImg, game.selectedImg, game.vitoria
    )

    # MÁQUINA DE ESTADOS
    if game.estado == "menu":
        game.estado = Interface.tela_menu(img, cursor, clicou)
        if game.estado == "sair": break

    elif game.estado == "fases":
        novo_estado, game.fase_atual = Interface.tela_selecao_fases(img, cursor, clicou)
        game.estado = novo_estado

    elif game.estado == "opcoes":
        cvzone.putTextRect(img, "EM BREVE...", (500, 350))
        if Interface.desenhar_botao(img, "VOLTAR", (500, 500, 200, 60), cursor, clicou):
            game.estado = "menu"

    elif game.estado == "jogando":
        if game.flagFase:
            game.iniciar_fase(game.fase_atual)

        # --- Lógica de Jogo ---
        if not game.vitoria:
            img, encaixes = renderizar_jogo(img, game.listImg)
            if encaixes == len(game.listImg) and len(game.listImg) > 0:
                game.vitoria = True

        # --- Lógica de Vitória ---
        if game.vitoria:
            if Interface.tela_vitoria(img, cursor, clicou):
                # Reset do jogo ao clicar em continuar
                game.reset_geral()
        pass


    cv2.imshow('Video', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
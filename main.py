import pygame

pygame.init()

import numpy
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import Interface
from ManagerJogo import ManagerJogo
from Render import renderizar_jogo
from clickDetection import processar_hand_input

# --- COnfigurações Pygame ---
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("CV Puzzle Game - Pygame Edition")
clock = pygame.time.Clock()

# --- Configurações OpenCV e CVZone ---
cap = cv2.VideoCapture(0)
cap.set(3, largura)
cap.set(4, altura)
detector = HandDetector(detectionCon=0.65)

# --- Variaveis de estado ---
estado = "menu"
MODO = 2
vitoria = False
rodando = True
listImg = inicializar()
selectedImg = None

while rodando:
    # Eventos Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            
    # captura OpenCV
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)

    # Processando mãos
    hands, img = detector.findHands(img, flipType=False) # draw=False para desabilitar o desenho da mão

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
                        if imgObj.rect.collidepoint(cursor):
                            if not imgObj.isMatched:
                                selectedImg = imgObj
                                break
                if selectedImg:
                    selectedImg.update(cursor)
        else:
            selectedImg = None

    # Conversão OpenCV (BGR) -> Pygame (RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pygame = pygame.surfarray.make_surface(numpy.transpose(img_rgb, (1,0,2)))

    # Renderização do fundo (imagem da camera)
    tela.blit(img_pygame, (0,0))

    # Máquina de Estados
    if estado == "menu":
        estado = Interface.tela_menu_pygame(tela, largura, cursor, clicou)
        if estado == "sair": break

    elif estado == "fases":
        print("ping 1")
        estado, num_pecas = Interface.tela_fases_pygame(tela, largura, cursor, clicou)

        if num_pecas is not None:
            listImg = inicializar(num_pecas)
            estado = "jogando"

        # --- Lógica de Jogo ---
        contador_encaixes = 0
        if not vitoria:
            contador_encaixes = renderizar_jogo(tela, listImg)

            if contador_encaixes == len(listImg) and len(listImg) > 0:
                vitoria = True

        # --- Lógica de Vitória ---
        if vitoria:
            if Interface.tela_vitoria_pygame(tela, largura, cursor, clicou):
                listImg = inicializar()
                vitoria = False
                estado = "fases"

    pygame.display.update()
    clock.tick(60) # Limita a 60 FPS

cap.release()
pygame.quit()
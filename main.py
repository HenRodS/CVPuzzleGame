import pygame

pygame.init()

import numpy
import cv2
import Interface
from game_manager import generate_basic_level
from Render import renderizar_jogo
from hand_controller import hand_processor

# --- COnfigurações Pygame ---
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("CV Puzzle Game - Pygame Edition")
clock = pygame.time.Clock()

# --- Configurações OpenCV e CVZone ---
cap = cv2.VideoCapture(0)
cap.set(3, largura)
cap.set(4, altura)

# --- Variaveis de estado ---
estado = "menu"
MODO = 2
vitoria = False
rodando = True
listPiece = generate_basic_level()
selectedPiece = None

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
    cursor, clicou, selectedPiece, img = hand_processor(
        img,
        vitoria,
        listPiece,
        selectedPiece
    )

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
        estado, num_pecas = Interface.tela_fases_pygame(tela, largura, cursor, clicou)

        if num_pecas is not None:
            listPiece = generate_basic_level(num_pecas)
            estado = "jogando"

    elif estado == "jogando":
        # --- Lógica de Jogo ---
        contador_encaixes = 0
        if not vitoria:
            contador_encaixes = renderizar_jogo(tela, listPiece)

            if contador_encaixes == len(listPiece) and len(listPiece) > 0:
                vitoria = True

        # --- Lógica de Vitória ---
        if vitoria:
            if Interface.tela_vitoria_pygame(tela, largura, cursor, clicou):
                listPiece = generate_basic_level()
                vitoria = False
                estado = "fases"

    pygame.display.update()
    clock.tick(60) # Limita a 60 FPS

cap.release()
pygame.quit()
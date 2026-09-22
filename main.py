import pygame

pygame.init()

import numpy
import cv2
from ui import level_select, main_menu, victory_screen, defeat_screen
from ui.timer_bar import TimerBar
from systems.level_generator import generate_basic_level
from systems.game_manager import check_victory
from systems.render import draw_game
from systems.hand_controller import hand_processor
from levels.level_1 import Level1
from levels.level_2 import Level2

# --- COnfigurações gerais ---
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
vitoria = False
derrota = False
fase_atual = 1
timer = TimerBar(largura_tela=largura)
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
        vitoria or derrota,
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
        # chama a tela principal e atualiza o estado conforme a escolha
        estado = main_menu.tela_menu_pygame(tela, largura, cursor, clicou)
        if estado == "sair":
            break

    elif estado == "fases":
        estado, fase_num = level_select.tela_fases_pygame(tela, largura, cursor, clicou)
        # --- Escolha das Fases ---
        if fase_num == 1:
            fase_atual = 1
            listPiece = Level1().load()
            timer.iniciar(Level1.tempo)
            vitoria = False
            derrota = False
            estado = "jogando"

        if fase_num == 2:
            fase_atual = 2
            listPiece = Level2().load()
            timer.iniciar(Level2.tempo)
            vitoria = False
            derrota = False
            estado = "jogando"

    elif estado == "jogando":
        # --- Lógica de Jogo ---
        contador_encaixes = 0
        if not vitoria and not derrota:
            draw_game(tela, listPiece)
            timer.atualizar()
            timer.desenhar(tela)

            if timer.esta_esgotado():
                derrota = True

            if check_victory(listPiece):
                vitoria = True
                timer.pausar()

        # --- Lógica de Vitória ---
        if vitoria:
            if victory_screen.tela_vitoria_pygame(tela, largura, cursor, clicou):
                listPiece = generate_basic_level()
                vitoria = False
                estado = "fases"

        # --- Lógica de Derrota (Tempo Esgotado) ---
        if derrota:
            acao = defeat_screen.tela_derrota_pygame(tela, largura, cursor, clicou)
            if acao == "reiniciar":
                if fase_atual == 1:
                    listPiece = Level1().load()
                    timer.iniciar(Level1.tempo)
                elif fase_atual == 2:
                    listPiece = Level2().load()
                    timer.iniciar(Level2.tempo)
                derrota = False
                vitoria = False
            elif acao == "fases":
                listPiece = generate_basic_level()
                derrota = False
                vitoria = False
                estado = "fases"
                

    pygame.display.update()
    clock.tick(60) # Limita a 60 FPS

cap.release()
pygame.quit()
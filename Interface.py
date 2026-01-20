import cv2
import cvzone


def desenhar_botao(img, texto, pos, cursor, click, cor=(50, 50, 50)):
    x, y, w, h = pos
    selecionado = x < cursor[0] < x + w and y < cursor[1] < y + h

    # Efeito de hover (muda a cor se o dedo estiver em cima)
    cor_final = (0, 200, 0) if selecionado else cor

    cv2.rectangle(img, (x, y), (x + w, y + h), cor_final, cv2.FILLED)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    cv2.putText(img, texto, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    return selecionado and click


def tela_menu(img, cursor, click):
    cvzone.putTextRect(img, "MENU PRINCIPAL", (400, 100), scale=3, thickness=3)

    btn_fases = desenhar_botao(img, "FASES", (500, 200, 250, 60), cursor, click)
    btn_opcoes = desenhar_botao(img, "OPCOES", (500, 300, 250, 60), cursor, click)
    btn_sair = desenhar_botao(img, "SAIR", (500, 400, 250, 60), cursor, click)

    if btn_fases: return "fases"
    if btn_opcoes: return "opcoes"
    if btn_sair: return "sair"
    return "menu"


def tela_selecao_fases(img, cursor, click):
    cvzone.putTextRect(img, "SELECIONE A FASE", (400, 100), scale=3, thickness=3)

    btn_fase1 = desenhar_botao(img, "FASE 1", (200, 250, 200, 60), cursor, click)
    btn_voltar = desenhar_botao(img, "VOLTAR", (500, 600, 200, 60), cursor, click)

    if btn_fase1: return "jogando"
    if btn_voltar: return "menu"
    return "fases"

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
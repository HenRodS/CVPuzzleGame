from cvzone.HandTrackingModule import HandDetector
import cv2

# --- Configurações ---
# maxHands=2 permite rastrear simultaneamente as mãos esquerda e direita
detector = HandDetector(detectionCon=0.65, maxHands=2)

def hand_processor(img, vitoria, listPiece, selectedPiece, usa_maos=False):
    # flipType=True garante que 'Right' corresponda à mão direita física e 'Left' à mão esquerda na imagem espelhada
    hands, img = detector.findHands(img, flipType=True)

    cursor = [0, 0]
    clicou = False
    detected_hands = set()

    # Se selectedPiece foi resetado externamente (ex: tela de derrota ou reinício), libera as peças
    if selectedPiece is None:
        for piece in listPiece:
            if hasattr(piece, 'dragged_by'):
                piece.dragged_by = None

    if hands:
        # Posição padrão do cursor (usada nos menus e botões da UI)
        cursor = hands[0]['lmList'][8][0:2]

        for hand in hands:
            hand_type = hand['type']  # 'Left' ou 'Right'
            detected_hands.add(hand_type)
            lmList = hand['lmList']
            h_cursor = lmList[8][0:2]

            # Distância entre indicador (8) e médio (12) para detecção de gesto de pinça/clique
            length, _, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
            hand_clicou = (length < 60)

            # Prioriza o cursor da mão que estiver interagindo/clicando para menus
            if hand_clicou:
                clicou = True
                cursor = h_cursor

            # Feedback visual das mãos no feed da câmera
            if usa_maos:
                # Flag TRUE: Ao invés de círculo no dedo com ESQ/DIR, a bounding box da mão
                # é colorida em vermelho para Mão Esquerda e azul para Mão Direita.
                # OpenCV usa formato BGR: Vermelho = (0, 0, 255), Azul = (255, 0, 0)
                cor_bbox = (0, 0, 255) if hand_type == "Left" else (255, 0, 0)

                if 'bbox' in hand:
                    x, y, w, h = hand['bbox']
                    x1 = max(0, x - 20)
                    y1 = max(0, y - 20)
                    x2 = min(img.shape[1], x + w + 20)
                    y2 = min(img.shape[0], y + h + 20)

                    # Bounding box colorida (mais espessa ao clicar)
                    espessura = 4 if hand_clicou else 2
                    cv2.rectangle(img, (x1, y1), (x2, y2), cor_bbox, espessura)

            # Se usa_maos for False: design padrão da mão, sem nenhum indicador de direita/esquerda

            # Lógica de seleção e arraste de peças durante o jogo
            if not vitoria:
                if hand_clicou:
                    # 1. Verifica se esta mão já está segurando alguma peça
                    peca_atual = None
                    for piece in listPiece:
                        if getattr(piece, 'dragged_by', None) == hand_type:
                            peca_atual = piece
                            break

                    # 2. Se não está segurando, tenta pegar uma peça sob o cursor
                    if peca_atual is None:
                        for piece in listPiece:
                            if piece.rect.collidepoint(h_cursor):
                                if not piece.isMatched and getattr(piece, 'dragged_by', None) is None:
                                    # Valida se a mão tem permissão para mover esta peça
                                    if piece.can_be_moved_by(hand_type):
                                        piece.dragged_by = hand_type
                                        peca_atual = piece
                                        break

                    # 3. Atualiza a posição da peça sendo arrastada
                    if peca_atual:
                        peca_atual.update(h_cursor)
                else:
                    # Solta qualquer peça que estava sendo segurada por esta mão
                    for piece in listPiece:
                        if getattr(piece, 'dragged_by', None) == hand_type:
                            piece.dragged_by = None

    # Solta peças se a mão correspondente saiu do campo de visão da câmera
    for piece in listPiece:
        if getattr(piece, 'dragged_by', None) and piece.dragged_by not in detected_hands:
            piece.dragged_by = None

    # Atualiza selectedPiece para manter compatibilidade com main.py
    selectedPiece = next((p for p in listPiece if getattr(p, 'dragged_by', None) is not None), None)

    return cursor, clicou, selectedPiece, img

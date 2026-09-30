from cvzone.HandTrackingModule import HandDetector
import cv2

# --- Configurações ---
# maxHands=2 permite rastrear simultaneamente as mãos esquerda e direita
detector = HandDetector(detectionCon=0.65, maxHands=2)

def hand_processor(img, vitoria, listPiece, selectedPiece):
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

            # Indicador visual no feed da câmera para feedback imediato do usuário
            # BGR: Vermelho (0, 0, 255) para Mão Esquerda, Azul (255, 120, 0) para Mão Direita
            cor_mao = (0, 0, 255) if hand_type == "Left" else (255, 120, 0)
            nome_mao = "ESQ" if hand_type == "Left" else "DIR"
            cv2.circle(img, (h_cursor[0], h_cursor[1]), 10, cor_mao, -1 if hand_clicou else 2)
            cv2.putText(img, nome_mao, (h_cursor[0] - 16, h_cursor[1] - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor_mao, 2)

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
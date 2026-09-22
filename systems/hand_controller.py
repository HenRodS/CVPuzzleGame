from cvzone.HandTrackingModule import HandDetector

# --- Configurações ---
detector = HandDetector(detectionCon=0.65)

def hand_processor(img, vitoria, listPiece, selectedPiece):
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
                if selectedPiece is None:
                    for piece in listPiece:
                        if piece.rect.collidepoint(cursor):
                            if not piece.isMatched:
                                selectedPiece = piece
                                break
                if selectedPiece:
                    selectedPiece.update(cursor)
        else:
            selectedPiece = None
    
    return cursor, clicou, selectedPiece, img
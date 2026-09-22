def check_victory(pieces):

    matched = 0

    for piece in pieces:

        if piece.isMatched:
            matched += 1

    return matched == len(pieces)
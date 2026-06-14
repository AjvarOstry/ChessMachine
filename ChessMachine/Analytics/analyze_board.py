# analizuje stan planszy
#wypluwa informacje, które mogą się przydać w paru miejscach
# dlatego lepiej to robić raz na ruch

import chess

def analyze_board(board):

    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    total_count = 0
    type_counts = [[], []]
    type_values = [1, 3, 3, 5, 9, 0]
    white_values = 0
    black_values = 0
    # króla nie liczymy do punktów, no bo musi być na planszy no XD

    for i, piece_type in enumerate(piece_types):
        white_count = len(board.pieces(piece_type, chess.WHITE))
        black_count = len(board.pieces(piece_type, chess.BLACK))

        type_counts[0].append(white_count)
        type_counts[1].append(black_count)

        white_values += white_count * type_values[i]
        black_values += black_count * type_values[i]

    total_count = sum(type_counts[0]) + sum(type_counts[1])

    return white_values, black_values, total_count

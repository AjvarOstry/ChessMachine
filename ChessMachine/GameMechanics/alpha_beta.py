import math

import chess

from Analytics.evaluate import evaluate

INF = math.inf

def alpha_beta(board, depth, alpha, beta, isMax):

    # do evaluate zrobię może numbą (biblioteka do kompilacji jit)
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        return evaluate(board)

    if isMax:

        value = -INF

        for move in board.legal_moves:

            board.push(move)

            value = max(
                value,
                alpha_beta(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )
            )

            board.pop()

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:

        value = INF

        for move in board.legal_moves:

            board.push(move)

            value = min(
                value,
                alpha_beta(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )
            )

            board.pop()

            beta = min(beta, value)

            if alpha >= beta:
                break

        return value

def get_best_moves(board, depth):

    results = []

    for move in board.legal_moves:

        board.push(move)

        score = alpha_beta(
            board,
            depth - 1,
            -INF,
            INF,
            False
        )

        board.pop()

        results.append((move, score))

    results.sort(
        key=lambda x: x[1],
        reverse=(board.turn == chess.WHITE)
    )

    return results
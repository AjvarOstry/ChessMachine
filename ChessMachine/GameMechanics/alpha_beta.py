import math
import time

import chess

from Analytics.evaluate import evaluate

INF = math.inf


def alpha_beta(board, depth, alpha, beta, isMax, deadline=None):

    if deadline is not None and time.time() > deadline:
        return evaluate(board)

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
                    False,
                    deadline
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
                    True,
                    deadline
                )
            )

            board.pop()

            beta = min(beta, value)

            if alpha >= beta:
                break

        return value

def get_best_moves(board, depth, k_max, deadline=None):

    legal_moves = list(board.legal_moves)

    if len(legal_moves) <= k_max:
        return [(move, 0) for move in legal_moves]

    results = []

    for move in legal_moves:

        board.push(move)

        score = alpha_beta(
            board,
            depth - 1,
            -INF,
            INF,
            board.turn == chess.WHITE,
            deadline
        )

        board.pop()

        results.append((move, score))

    results.sort(
        key=lambda x: x[1],
        reverse=(board.turn == chess.WHITE)
    )

    return results[:k_max]
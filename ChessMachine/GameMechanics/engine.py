import random
import threading
import time

from Analytics.TimeManager import TimeManager
from GameMechanics.alpha_beta import get_best_moves
from GameMechanics.open_game import open_game


def engine(board, time_for_round):

    opening_move = open_game(board, "../z_project_data/openings.bin")
    if opening_move is not None:
        return opening_move

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    if len(legal_moves) == 1:
        return legal_moves[0]

    start = time.time()
    soft_deadline = start + time_for_round * 0.95
    hard_deadline = start + time_for_round

    best_move = legal_moves[0]
    depth = 1

    while time.time() < soft_deadline:

        results = get_best_moves(board, depth, 1, hard_deadline)

        if results and time.time() < hard_deadline:
            best_move = results[0][0]
        else:
            break

        depth += 1

    return best_move



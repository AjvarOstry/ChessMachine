import random
import threading

from Analytics.TimeManager import TimeManager
from GameMechanics.alpha_beta import get_best_moves
from GameMechanics.open_game import open_game


def engine(board):

    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None

    best_move = random.choice(legal_moves)

    time_for_round = TimeManager.give_me_time(
        # TODO
    )

    opening_move = open_game(board, "../z_project_data/openings.bin")

    if opening_move is not None:
        return opening_move

    def find_best_move(board):

        nonlocal best_move

        top_moves = get_best_moves(
            board,
            depth=3,
            k_max=10
        )

        if not top_moves:
            return

        best_move = top_moves[0][0]

        # sekcja z modelem

    worker = threading.Thread(
        target=find_best_move,
        daemon=True
    )

    worker.start()

    worker.join(timeout=time_for_round)

    return best_move



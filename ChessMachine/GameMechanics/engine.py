import random
import threading
import time

from Analytics.TimeManager import TimeManager
from GameMechanics.alpha_beta import get_best_moves
from GameMechanics.open_game import open_game

from Evaluation.evaluation import evaluate

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
    depth = 3

    while time.time() < soft_deadline:

        results = get_best_moves(board, depth, 1, hard_deadline)

        if results and time.time() < hard_deadline:
            best_move = results[0][0]

            if board.turn == 1:
                best_value = -1000
            else:
                best_value = 1000

            best_index = 0
            for i in range(results):
                for j in results[i]:
                    board.push(results[i][j])
                value = evaluate(results[i])
                for j in reversed(range(results[i])):
                    board.pop(results[i][j])

                if board.turn == 1:
                    if value > best_value:
                        best_value = value
                        best_index = i

                if board.turn == 0:
                    if value < best_value:
                        best_value = value
                        best_index = i

            best_move = results[best_index][0]

        else:
            break

        depth += 1

    return best_move



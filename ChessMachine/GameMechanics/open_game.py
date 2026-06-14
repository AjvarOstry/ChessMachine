# losujemy otwarcie albo dobieramy kontrę

import chess
import chess.polyglot
import random

def open_game(board, path):

    with chess.polyglot.open_reader(path) as reader:
        entries = list(reader.find_all(board))
        if entries:
            max_weight = max(e.weight for e in entries)
            best = [e for e in entries if e.weight == max_weight]
            move = random.choice(best).move
            return move

        return None


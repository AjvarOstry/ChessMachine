# Notes
# lista komend:
# https://official-stockfish.github.io/docs/stockfish-wiki/UCI-&-Commands.html

import sys
import chess

machine_name = "Chess Machine 1.0"
author = "team NULL"

def uci_command_loop():

    # tu trzeba jakiegoś boarda dać

    while True:
        got_command = input().strip()

        # quit the program ASAP
        if got_command == "quit":
            break

        # engine, identify yourself
        elif got_command == "uci":
            print(f"id name {machine_name}")
            print(f"id author {author}")

            # tu sobie można opcje dorzucić
            # jak jakieś będą
            # print(f"option name <opcje>")

            print("uciok")

        elif got_command == "isready":
            print("readyok")

        elif got_command == "ucinewgame":
            game_board = chess.Board()
            pass

        # uci wypisuje nam stan planszy
        # w postaci wszystkich dotychczasowych ruchów
        elif got_command.startswith("position"):
            # parsowanie pozycji
            pass

        elif got_command.startswith("go"):
            #liczymy ruchy
            print(f"info <jakieś debug info bota>") # tak se możemy logi wypluwać
            print("bestmove <ruch>")
            pass

        # musi być, bo się cute zawiesi
        sys.stdout.flush()

# dlaczego robimy to od nowa za każdym razem zamiast pamiętać planszę?
# podobno taki jest protokół, więc tak się robi.
# ale jak ktoś isę uprze to możemy zmieni
def parse_position(got_command, board):
    command_parts = got_command.split()
    part_id = 1 # bo zero to position

    board.reset()

    if part_id < len(command_parts) and command_parts[part_id] == "moves":
        for move in command_parts[part_id+1:]:
            board.push_uci(move)

    return board


# Notes
# lista komend:
# https://official-stockfish.github.io/docs/stockfish-wiki/UCI-&-Commands.html

import sys
from GameMechanics import open_game

import chess

machine_name = "Chess Machine 1.0"
author = "team NULL"
ruch = None

def uci_command_loop():

    game_board = chess.Board()

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
            game_board = parse_position(got_command, game_board)
            pass

        elif got_command.startswith("go"):
            #liczymy ruchy
            best_move = None

            mv = open_game(game_board)
            if mv is not None:
                best_move = mv.uci()
            else:
                pass # tu będzie nasz silnik

            print(f"info <jakieś debug info bota>") # tak se możemy logi wypluwać
            print(f"bestmove {best_move}")
            pass

        # musi być, bo się cute zawiesi
        sys.stdout.flush()

# dlaczego robimy to od nowa za każdym razem zamiast pamiętać planszę?
# podobno taki jest protokół, więc tak się robi.
# ale jak ktoś isę uprze to możemy zmieni
def parse_position(got_command, board):
    def parse_position(got_command, board):
        command_parts = got_command.split()
        board.reset()
        if "moves" in command_parts:
            moves_index = command_parts.index("moves")
            for move in command_parts[moves_index + 1:]:
                board.push_uci(move)
        return board


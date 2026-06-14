# Notes
# lista komend:
# https://official-stockfish.github.io/docs/stockfish-wiki/UCI-&-Commands.html

import sys
from GameMechanics import open_game
from Analytics.TimeManager import TimeManager

import chess

from GameMechanics.engine import engine

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
            time_manager = None
            pass

        # uci wypisuje nam stan planszy
        # w postaci wszystkich dotychczasowych ruchów
        elif got_command.startswith("position"):
            game_board = parse_position(got_command, game_board)
            pass

        elif got_command.startswith("go"):

            wtime, btime, winc, binc, movestogo = parse_go(got_command)

            if time_manager is None:
                if game_board.turn == chess.WHITE :
                    is_white = True
                else:
                    is_white = False

                time_manager = TimeManager(is_white, 540000, 0)

            if is_white:
                my_time = wtime
                enemy_time = btime
            else:
                my_time = btime
                enemy_time = wtime

            our_time = time_manager.schedlue_time(my_time, enemy_time, game_board, (game_board.ply - 10))

            best_move = engine(game_board, our_time)

            print(f"bestmove {best_move}")
            pass

        # musi być, bo się cute zawiesi
        sys.stdout.flush()

# dlaczego robimy to od nowa za każdym razem zamiast pamiętać planszę?
# podobno taki jest protokół, więc tak się robi.
# ale jak ktoś isę uprze to możemy zmieni
def parse_position(got_command, board):
    command_parts = got_command.split()
    if "startpos" in command_parts:
        board.reset()
    elif "fen" in command_parts:
        fen_index = command_parts.index("fen")
        fen = " ".join(command_parts[fen_index + 1 : fen_index + 7])
        board.set_fen(fen)
    
    if "moves" in command_parts:
        moves_index = command_parts.index("moves")
        for move in command_parts[moves_index + 1:]:
            board.push_uci(move)
    return board

def parse_go(got_command):
    command_parts = got_command.split()

    wtime = 0
    btime = 0
    winc = -1
    binc = -1
    movestogo = -1


    if "wtime" in command_parts:
        wtime_index = command_parts.index("wtime")
        wtime = command_parts[wtime_index + 1]

    if "btime" in command_parts:
        btime_index = command_parts.index("btime")
        btime = command_parts[btime_index + 1]

    if "winc" in command_parts:
        winc_index = command_parts.index("winc")
        winc = command_parts[winc_index + 1]

    if "binc" in command_parts:
        binc_index = command_parts.index("binc")
        binc = command_parts[binc_index + 1]

    if "movestogo" in command_parts:
        movestogo_index = command_parts.index("movestogo")
        movestogo = command_parts[movestogo_index + 1]

    return wtime, btime, winc, binc, movestogo
    # wtime - czas dla białego
    # btime - czas dla czarnego
    # winc/binc - wzrost czasu dodatkowo
    # movestogo - zbędne
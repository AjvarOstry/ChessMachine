import chess
import time

from GameMechanics.FinishHim import FinishHim
from GameMechanics.alpha_beta import get_best_moves
from GameMechanics.open_game import open_game

from UCI.uci_command_loop import uci_command_loop

from Evaluation.evaluation import initModel

def main():

    uci_command_loop()

if __name__ == "__main__":
    initModel()
    main()
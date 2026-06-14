# tablice końcówek Sygyzy 5-men

import chess

class FinishHim:

    def __init__(self, cat_path):
        self.cat_path = cat_path


    def get_move(self, board):

        if(len(board.piece_map()) > 4):
            return None

        else:

            top_move = None
            top_DTZ = None

            for move in board.legal_moves:
                board.push(move)

                try:
                    WDL = self.tablebase.get_wdl(board)
                    DTZ = self.tablebase.get_dtz(board)

                    # to jest ruch z perspektywy przeciwnika,
                    #sprawdziłem. Żebym tego nie overthinkował znowu
                    if WDL == -2 and DTZ is not None:

                        if top_DTZ is None or abs(DTZ) > abs(top_DTZ):
                            top_DTZ = DTZ
                            top_move = move

                except:
                    pass

                board.pop()

        return top_move



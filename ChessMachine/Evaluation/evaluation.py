import torch
import chess
import torch.nn as nn

MODEL_FILE = "chess_model.pth"

INPUT_SIZE = 915

piece_map = {
    "P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5,
    "p": 6, "n": 7, "b": 8, "r": 9, "q": 10, "k": 11
}

piece_values = {
    "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0,
    "p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0
}

max_counts = torch.tensor([
    8, 2, 2, 2, 1, 1,
    8, 2, 2, 2, 1, 1
    ], dtype=torch.float32)

model = None

def initModel():
    global model

    model = ChessNet()

    model.load_state_dict(torch.load(MODEL_FILE, map_location=torch.device("cpu")))

    model.eval()


def evaluate(board):
    x = torch.tensor(getInputData(board), dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
            value = model(x).item()

    return value * 1000.0

def getInputData(board):
    x = torch.zeros(INPUT_SIZE, dtype=torch.float32)

    # pieces
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            idx = piece_map[piece.symbol()] * 64 + sq
            x[idx] = 1.0

    # game state
    offset = 768

    x[offset] = float(board.turn)
    x[offset + 1] = float(board.has_kingside_castling_rights(chess.WHITE))
    x[offset + 2] = float(board.has_queenside_castling_rights(chess.WHITE))
    x[offset + 3] = float(board.has_kingside_castling_rights(chess.BLACK))
    x[offset + 4] = float(board.has_queenside_castling_rights(chess.BLACK))

    # attack maps
    white_attack_offset = 773
    black_attack_offset = 837

    white_attack = 0
    black_attack = 0

    for sq in board.pieces(chess.PAWN, chess.WHITE):
        white_attack |= chess.BB_PAWN_ATTACKS[chess.WHITE][sq]
    for sq in board.pieces(chess.KNIGHT, chess.WHITE):
        white_attack |= chess.BB_KNIGHT_ATTACKS[sq]
    for sq in board.pieces(chess.KING, chess.WHITE):
        white_attack |= chess.BB_KING_ATTACKS[sq]
    for sq in board.pieces(chess.BISHOP, chess.WHITE):
        white_attack |= int(board.attacks(sq))
    for sq in board.pieces(chess.ROOK, chess.WHITE):
        white_attack |= int(board.attacks(sq))
    for sq in board.pieces(chess.QUEEN, chess.WHITE):
        white_attack |= int(board.attacks(sq))

    for sq in board.pieces(chess.PAWN, chess.BLACK):
        black_attack |= chess.BB_PAWN_ATTACKS[chess.BLACK][sq]
    for sq in board.pieces(chess.KNIGHT, chess.BLACK):
        black_attack |= chess.BB_KNIGHT_ATTACKS[sq]
    for sq in board.pieces(chess.KING, chess.BLACK):
        black_attack |= chess.BB_KING_ATTACKS[sq]
    for sq in board.pieces(chess.BISHOP, chess.BLACK):
        black_attack |= int(board.attacks(sq))
    for sq in board.pieces(chess.ROOK, chess.BLACK):
        black_attack |= int(board.attacks(sq))
    for sq in board.pieces(chess.QUEEN, chess.BLACK):
        black_attack |= int(board.attacks(sq))

    for sq in range(64):
        x[white_attack_offset + sq] = 1 if (white_attack & chess.BB_SQUARES[sq]) else 0
        x[black_attack_offset + sq] = 1 if (black_attack & chess.BB_SQUARES[sq]) else 0

    # piece counts + material
    count_offset = 901
    counts = torch.zeros(12, dtype=torch.float32)

    material_white = 0.0
    material_black = 0.0

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if not piece:
            continue

        symbol = piece.symbol()
        counts[piece_map[symbol]] += 1

        if piece.color == chess.WHITE:
            material_white += piece_values[symbol]
        else:
            material_black += piece_values[symbol]

    x[count_offset:count_offset + 12] = counts

    x[913] = material_white
    x[914] = material_black

    #ODKOMENTOWAC DO NOWYCH WAG
    # x[901:913] /= max_counts
    # x[913] /= 39.0
    # x[914] /= 39.0

    return x

class ChessNet(nn.Module):

    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(INPUT_SIZE, 1024),
            nn.ReLU(),
            nn.Dropout(0.1),

            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.1),

            nn.Linear(512, 256),
            nn.ReLU(),

            nn.Linear(256, 1)
        )

    def forward(self, x):
        return self.net(x)
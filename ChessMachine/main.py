import chess
import time

from GameMechanics.alpha_beta import get_best_moves


def benchmark_game(depth=3, k_max=5, max_moves=40):
    """
    Rozgrywa partię silnik vs silnik (samego ze sobą),
    wybierając zawsze najlepszy ruch z get_best_moves.
    Mierzy czas na ruch.
    """
    board = chess.Board()

    move_times = []

    for move_num in range(max_moves):

        if board.is_game_over():
            print(f"Gra zakończona po {move_num} ruchach: {board.result()}")
            break

        start = time.time()
        best_moves = get_best_moves(board, depth, k_max)
        elapsed = time.time() - start

        move_times.append(elapsed)

        best_move = best_moves[0][0]
        board.push(best_move)

        print(f"Ruch {move_num + 1:3d}: {best_move.uci():6s}  "
              f"czas = {elapsed:.3f}s")

    else:
        print(f"\nOsiągnięto limit {max_moves} ruchów (gra niezakończona)")

    print()
    print(f"Liczba ruchów: {len(move_times)}")
    print(f"Średni czas:   {sum(move_times) / len(move_times):.3f}s")
    print(f"Min/Max:       {min(move_times):.3f}s / {max(move_times):.3f}s")
    print(f"Suma czasu:    {sum(move_times):.3f}s")


if __name__ == "__main__":
    benchmark_game(depth=5, k_max=5, max_moves=100)
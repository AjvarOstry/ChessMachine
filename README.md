# ChessMachine
a chess playing engine created for KINo AI chess competition.
*competition repo: https://github.com/kinoai/chess_engine_competition*

**category:** Open

## Team
**name:** "NULL"
**Members:**
- Marcin Cieślak 254735
- Wojciech Iszczak 254765
- Piotr Marciniak 254810

## Technologies

Python 3.13

**Libraries:**
- chess 1.11.2
- numpy 2.4.4
- PyTorch 

Machine is communicating through the UCI protocol. 
Available from a docker container created by `./Dockerfile`


## Docker cheatsheet

**budowa:** `docker build --no-cache -t chess-engine -f ścieżka/do/Dockerfile .`
**uruchamianie:** `docker run -i chess-engine`


## Konwersacje z SI

- Polyglot + python.chess: https://claude.ai/share/4f43d8a0-55e5-4195-9558-701e7579ca0c
- Syzygy + python.chess:   https://claude.ai/share/3f65562d-3b81-49b6-8e4b-ac96271d9fc8

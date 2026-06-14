# =============================================================================
# Chess Engine Container Template — CUDA + cutechess-cli adapter
# Base image: CUDA 12 devel (swap tag to match your driver)
#
# Template modified for NULL team chess engine
# =============================================================================
FROM nvidia/cuda:12.3.1-devel-ubuntu22.04
ARG DEBIAN_FRONTEND=noninteractive

# ---------------------------------------------------------------------------
# System dependencies
# Python 3.13
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        software-properties-common \
        git \
        ca-certificates \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
        python3.13 \
        python3.13-dev \
        python3.13-venv \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Python libraries
# ---------------------------------------------------------------------------
RUN python3.13 -m ensurepip

RUN python3.13 -m pip install --no-cache-dir \
        chess==1.11.2 \
        numpy==2.4.4

RUN python3.13 -m pip install --no-cache-dir \
        torch --index-url https://download.pytorch.org/whl/cu121
# ---------------------------------------------------------------------------
# Build Chess Machine by NULL team
# ---------------------------------------------------------------------------
WORKDIR /opt/engines

RUN git clone --depth 1 https://github.com/AjvarOstry/ChessMachine.git ChessMachine


HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD echo "uci" | timeout 5 python3.13 /opt/engines/ChessMachine/ChessMachine/main.py | grep -q "uciok"

ENTRYPOINT ["python3.13", "/opt/engines/ChessMachine/ChessMachine/main.py"]

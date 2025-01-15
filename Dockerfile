FROM ghcr.io/astral-sh/uv:python3.10-bookworm AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Build sub-dependencies
COPY packages/ packages/
RUN cd packages/bright-ws && uv build --package bright-ws

# Copy and install application dependencies with frozen lock
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev
RUN uv pip install /app/packages/bright-ws/dist/bright_ws-*.whl

FROM python:3.10-bookworm AS runner

RUN apt update -y && apt upgrade -y
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && mkdir -m 0755 -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify Docker installation
RUN docker --version
WORKDIR /app

# Copy packages and application
COPY --from=builder /app/.venv .venv
COPY src/ src/

# Set path to venv to allow uvicorn command to be resolved
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "src/donationbox/app.py"]

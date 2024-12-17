FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy pyproject.toml and lockfile for package installation
COPY pyproject.toml uv.lock ./

# Install with frozen lock
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.13-bookworm AS runner

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

CMD ["python", "src/app.py"]

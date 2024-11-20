FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy pyproject.toml and lockfile for package installation
COPY pyproject.toml uv.lock ./

# Install with frozen lock
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.13-bookworm AS runner

WORKDIR /app

# Copy packages and application
COPY --from=builder /app/.venv .venv
COPY src/ src/

# Set path to venv to allow uvicorn command to be resolved
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

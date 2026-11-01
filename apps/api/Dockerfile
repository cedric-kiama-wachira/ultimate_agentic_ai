FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy only the dependency files first for better caching:

COPY pyproject.toml uv.lock ./

# Copy package files and source

COPY apps/api ./apps/api

# Enable bytecode compilation and Python optimization

ENV UV_COMPILE_BYTECODE=1

# Install dependencies includeing the workspace packages :

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package api

# Enable bytecode compilation and Python optimization 

ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the path to use the virtual environment:

ENV PATH="/app/.venv/bin:$PATH" \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV PYTHONPATH="/app/apps/api/src:$PYTHONPATH"

# Create a group plus a non root user and relevant directories with proper permissions:

RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app 


# Switch to non root user:
    
USER app

# Expose the port for the Streamlit app:

EXPOSE 8000

WORKDIR /app/apps/api/src

# Command to run the  FastAPI application server:

CMD [ "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
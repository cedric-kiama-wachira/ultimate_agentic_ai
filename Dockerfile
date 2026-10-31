FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation and Python optimization

ENV UV_COMPILE_BYTECODE=1
ENV PYTHONOPTIMIZE=1
ENV UV_LINK_MODE=copy 

# Set the Python path to include the src directory for imports:

ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Copy only the dependency files first for better caching:

COPY pyproject.toml uv.lock ./

# Install the required dependencies:

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy the application code:

COPY src ./src/

# Set the path to use the virtual environment:

ENV PATH="/app/.venv/bin:$PATH" \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Create a group plus a non root user and relevant directories with proper permissions:

RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app && \
    mkdir -p /home/app && \
    chown -R app:app /home/app && \
    mkdir -p /home/app/.streamlit && \
    mkdir -p /home/app/.streamlit/data && \
    mkdir -p /home/app/.streamlit/cache && \
    chown -R app:app /home/app/.streamlit 

# Set home directory for the user:

    ENV HOME=/home/app

# Switch to non root user:
    
    USER app

# Expose the port for the Streamlit app:

    EXPOSE 8501

# Command to run the Streamlit app:

    CMD [ "uv", "run", "streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
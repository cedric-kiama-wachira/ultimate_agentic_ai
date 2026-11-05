FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy only the dependency files first for better caching:

COPY pyproject.toml uv.lock ./

# Copy the application code:

COPY apps/chatbot_ui ./apps/chatbot_ui

# Enable bytecode compilation and Python optimization

ENV UV_COMPILE_BYTECODE=1 

# Install dependencies including the workspace packages:

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package chatbot_ui

# Enable bytecode compilation and Python optimization.
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the path to use the virtual environment:

ENV PATH="/app/.venv/bin:$PATH" \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV PYTHONPATH="/app/apps/chatbot_ui/src:$PYTHONPATH"

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

WORKDIR /app/apps/chatbot_ui/src

# Command to run the Streamlit app:

CMD [ "streamlit", "run", "chatbot_ui/app.py", "--server.address=0.0.0.0"]
# Combined Backend + Frontend Dockerfile
# Stage 1: Build frontend
FROM node:24-alpine AS frontend-builder

WORKDIR /frontend

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy frontend package files
COPY frontend/package.json frontend/pnpm-lock.yaml frontend/pnpm-workspace.yaml ./

# Install frontend dependencies
RUN pnpm install --frozen-lockfile

# Copy frontend source
COPY frontend ./

# Build static frontend
RUN pnpm run build

# Stage 2: Backend with static files
FROM python:3.14-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy backend dependency files
COPY backend/pyproject.toml ./

# Install backend dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy backend application code
COPY backend ./

# Copy built frontend static files to backend/static
COPY --from=frontend-builder /frontend/build ./static

# Expose port
EXPOSE 43434

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "43434"]
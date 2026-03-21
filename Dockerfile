FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files needed by the MCP server.
COPY mcp_server.py .

# Run the MCP server over stdio.
CMD ["python", "mcp_server.py"]

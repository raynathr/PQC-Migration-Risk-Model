FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY examples/ ./examples/
COPY tests/ ./tests/
COPY data/ ./data/

# Create results directory
RUN mkdir -p results

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "main.py"]

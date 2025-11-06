FROM python:3.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# Copy API-specific requirements first for better caching
COPY api/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API application code
COPY api/. .

# Ensure models directory exists even if no pretrained files are provided
RUN mkdir -p ./models

# Copy additional assets from the parent repository
COPY data ./data
COPY sample_data ./sample_data
COPY demo.py ./demo.py
COPY extract_measurements.py ./extract_measurements.py
COPY functions.py ./functions.py
COPY inference.py ./inference.py
COPY networks.py ./networks.py
COPY opendr_mock.py ./opendr_mock.py
COPY utils.py ./utils.py
COPY src ./src
COPY commands ./commands

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


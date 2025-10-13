# Use a slim Python base image
FROM python:3.11-slim

# Install antiword
RUN apt-get update && \
    apt-get install -y antiword && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]


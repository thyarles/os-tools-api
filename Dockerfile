# Use a slim Python base image
FROM python:3.11-slim

# Install antiword
RUN apt-get update && \
    apt-get install -y antiword ghostscript lynx unrtf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /

# Copy application files
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "app.main"]


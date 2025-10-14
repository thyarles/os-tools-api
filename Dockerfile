# Use a slim Python base image
FROM python:3.13-slim

# Install tools
RUN apt-get update && \
    apt-get install -y antiword lynx ghostscript unrtf && \
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


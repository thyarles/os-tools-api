# Use a slim Python base image
FROM python:3.13-slim

# Install tools
RUN apt-get update \
    && apt-get install -y \
       antiword \
       lynx \
       ghostscript \
       unrtf \
       odt2txt \
       docx2txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy application files
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

# Expose the port
EXPOSE 5000

# Set path
ENV PYTHONPATH=/

# Run the application
CMD ["python", "-m", "app.main"]


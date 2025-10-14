# Use a slim Python base image
FROM python:3.13-alpine

# Install tools
RUN apk update && \
    apk add --no-cache antiword ghostscript lynx unrtf

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


# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script
COPY scrape.py .

# Create automation directory
RUN mkdir -p /app/automation

# Set environment variable for the base directory
ENV BASE_DIR=/app/automation

# Command to run the script
CMD ["python", "scrape.py"] 
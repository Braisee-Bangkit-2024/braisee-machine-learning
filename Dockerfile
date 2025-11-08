# Use Python 3.9 slim image
FROM python:3.9-slim
  
# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY . .

# Expose the port used by the app
EXPOSE 8080
# Command to run the application
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]

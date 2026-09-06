# Use Python 3.11 on a minimal Debian-based image
FROM python:3.11-slim

# Prevent Python from creating .pyc files
# and ensure Python output appears immediately in container logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file first
# This allows Docker to cache the dependency installation layer
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app.py .

# Document the port used by the FastAPI application
EXPOSE 8000

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8585
EXPOSE 8080

# Start a simple HTTP server that serves static files from /app
CMD ["python", "-m", "http.server", "8080"]

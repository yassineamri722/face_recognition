# Use the official Python 3.8 slim image
FROM python:3.8-slim

# Install dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install required Python packages from requirements.txt
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Set the environment variable for Flask app to the correct path
ENV FLASK_APP=src/app.py

# Expose the port the app will run on
EXPOSE 5000

# Use Gunicorn to run the Flask app from the src directory
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]

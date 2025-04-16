FROM python:3.8-slim

# Install dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install required Python packages
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy the application code
COPY . /app/

# Run the application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

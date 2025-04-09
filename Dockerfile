# Use official Python 3.8 Alpine image as a base
FROM python:3.8-alpine

# Set working directory inside the container
WORKDIR /app

# Copy everything from the current folder into the container
COPY . /app 
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by Flask (adjust if needed)
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]

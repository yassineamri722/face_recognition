# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install any dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by your application (if relevant)
EXPOSE 5000

# Run the application with python app.py (instead of flask run)
CMD ["python", "app.py"]

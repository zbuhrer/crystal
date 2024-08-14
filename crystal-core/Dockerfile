# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./crystal-core /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5005 available to the world outside this container
EXPOSE 5005

# Run core-app.py when the container launches
CMD ["python", "core-app.py"]
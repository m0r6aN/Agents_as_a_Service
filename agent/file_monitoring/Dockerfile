# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8003

# Define environment variable
# ENV NAME World
# If your app needs to connect to a database, you might use something like this:
# ENV DATABASE_URL=postgresql://user:password@db_host:5432/mydatabase

# Run app.py when the container launches
CMD ["python", "file_monitor.py"]
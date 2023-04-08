# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /

# Copy the requirements file into the container at /app
COPY requirements.txt /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /

# Expose port 8000 for the Django app to run on
EXPOSE 8000

# Start the Celery worker and the Django app using supervisord
CMD ["/usr/bin/supervisord", "-c", "/supervisord.conf"]

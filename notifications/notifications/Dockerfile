# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV development
RUN apt-get update
RUN apt install -y graphviz nano
# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt /code/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . /code/

# Expose the port on which the Django server will run (change it if needed)
EXPOSE 8000

# Set up the entrypoint command

CMD ["sh", "-c", "python manage.py migrate && python manage.py migrate api && python manage.py runserver 0.0.0.0:8000"]
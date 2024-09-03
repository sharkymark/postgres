# Python image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# get utilities in the container
RUN apt-get update && apt-get install -y procps ssh git net-tools htop sudo

# Install pip dependencies
# RUN pip install --no-cache-dir --upgrade pip && pip install pandas jupyterlab ipykernel
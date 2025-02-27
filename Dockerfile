# Use official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy project files to the container
COPY . /app/

# Install uv
RUN pip install --upgrade pip
RUN pip install uv

# Install project dependencies using uv
RUN uv sync

# Expose Django port
EXPOSE 8000

# Start the Django application using Gunicorn
CMD ["gunicorn", "HydroponicsSystem.wsgi:application", "--bind", "0.0.0.0:8000"]

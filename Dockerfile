# Use the official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root
# Copy the rest of the application code into the container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run the application using gunicorn
CMD ["poetry", "run", "gunicorn", "HydroponicsSystem.wsgi:application", "--bind", "0.0.0.0:8000"]

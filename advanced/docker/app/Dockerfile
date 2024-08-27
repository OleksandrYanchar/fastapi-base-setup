FROM python:3.10

WORKDIR /app

RUN apt update && apt -qy upgrade

ADD pyproject.toml /app

# Upgrade pip and install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of your application code to the working directory
COPY . /app/

# Set the PYTHONPATH environment variable
ENV PYTHONPATH="/app"

# Set the final working directory in the container
WORKDIR /app/
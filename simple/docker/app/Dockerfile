FROM python:3.10

WORKDIR /app

RUN apt update && apt -qy upgrade

# Copy the entire requirements directory
COPY requirements /app/requirements
# Install dependencies from dev.txt
RUN pip install -r requirements/dev.txt

# Copy the rest of your application
COPY . /app/

ENV PYTHONPATH="/app"

WORKDIR /app/
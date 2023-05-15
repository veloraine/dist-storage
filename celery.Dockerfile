# Base image
FROM python:3.9

ARG URL_0
ARG URL_1
ARG URL_2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV URL_0 $URL_0
ENV URL_1 $URL_1
ENV URL_2 $URL_2

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . /app

CMD ["celery", "purge"]

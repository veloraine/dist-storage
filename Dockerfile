# Base image
FROM python:3.9

ARG URL_0
ARG URL_1
ARG URL_2
ARG URL_3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV URL_0 $URL_0
ENV URL_1 $URL_1
ENV URL_2 $URL_2
ENV URL_3 $URL_3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
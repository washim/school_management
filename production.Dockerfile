FROM python:latest
RUN useradd ec2-user
EXPOSE 8000
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=school_management.settings_production \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install "gunicorn==20.0.4"
COPY requirements.txt /
RUN pip install -r /requirements.txt
WORKDIR /app
RUN chown ec2-user:ec2-user /app
COPY --chown=ec2-user:ec2-user . .
USER ec2-user
RUN python manage.py collectstatic --noinput --clear --no-post-process
#CMD gunicorn school_management.wsgi:application --certfile=server.crt --keyfile=server.key
CMD gunicorn school_management.wsgi:application --workers=4 --timeout 1200 --keep-alive 1200
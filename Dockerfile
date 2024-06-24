FROM python:3.11-bullseye as base

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends python3-gdal &&  \
    rm -rf /var/lib/apt/lists/* && \
    # Create a user
    addgroup --system random_user && adduser --system --group random_user && \
    mkdir /staticfiles

FROM base as development

RUN pip install --disable-pip-version-check --no-cache-dir -U pip poetry

COPY ./poetry.lock ./pyproject.toml /
RUN poetry export --without-hashes -o requirements.txt

# Make wheels in wheels/ directory
RUN mkdir /wheels && \
    pip wheel --disable-pip-version-check --no-cache-dir -r requirements.txt -w /wheels

FROM base as production

COPY --from=development /wheels /wheels
COPY ./deployment/configurations/gunicorn.conf.py /gunicorn.conf.py
COPY ./deployment/entrypoints/entrypoint-dashboard.sh /entrypoint-dashboard
COPY ./deployment/entrypoints/entrypoint-celery-worker.sh /entrypoint-celery-worker
COPY ./deployment/entrypoints/entrypoint-celery-flower.sh /entrypoint-celery-flower
RUN chmod +x /entrypoint*

RUN pip install --disable-pip-version-check --no-cache-dir -U /wheels/* && \
    rm -rf /wheels && \
    rm -rf /root/.cache/pip \
    rm -rf /var/cache/apk/*

COPY ./open_data_spain /app
RUN chown -R random_user:random_user /app /staticfiles

WORKDIR /app
ENV STATIC_ROOT=/staticfiles

RUN DJANGO_SETTINGS_MODULE=ods.settings python manage.py collectstatic --noinput

#USER random_user
ENTRYPOINT ["/entrypoint-web"]

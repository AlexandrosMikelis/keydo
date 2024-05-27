ARG PYTHON_VERSION=3.9-alpine3.13

FROM python:${PYTHON_VERSION} as python
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apk update && \
    apk add --no-cache \
        # dependencies for building Python packages
        build-base \
        # psycopg2 dependencies
        postgresql-dev

COPY app/requirements .
# COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apk update && \
    apk add --no-cache \
        # psycopg2 dependencies
        postgresql-dev \
        # Translations dependencies
        gettext \
    && rm -rf /var/cache/apk/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

COPY app/compose/production/django/entrypoint /entrypoint 
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY app/compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY app/compose/local/faust/start /start-faust
RUN sed -i 's/\r$//g' /start-faust
RUN chmod +x /start-faust

# copy application code to WORKDIR
COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]

# EXPOSE 8000

# ARG DEV=false
# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     apk add --update --no-cache postgresql-client && \
#     apk add --update --no-cache --virtual .tmp-build-deps \
#         build-base postgresql-dev musl-dev && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp && \
#     apk del .tmp-build-deps && \
#     adduser \
#         --disabled-password \
#         --no-create-home \
#         django-user

# COPY ./entrypoint /entrypoint
# RUN sed -i 's/\r$//g' /entrypoint
# RUN chmod +x /entrypoint

# COPY ./start /start-faust
# RUN sed -i 's/\r$//g' /start-faust
# RUN chmod +x /start-faust

# ENV PATH="/py/bin:$PATH"

# USER django-user



FROM python:3.12

RUN mkdir -p /app
WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install --no-cache-dir poetry python-multipart gunicorn uvicorn

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

EXPOSE 80

ENTRYPOINT ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80", "api:app", "--log-level", "info", "--error-logfile", "-"]
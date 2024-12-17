FROM python:3.12

RUN mkdir -p /app
WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install --no-cache-dir poetry python-multipart gunicorn uvicorn black isort

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

EXPOSE 80

ENTRYPOINT ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80", "api:app", "--error-logfile", "-"]
#ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "trace", "--use-colors"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
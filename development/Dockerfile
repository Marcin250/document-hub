FROM python:3.12

RUN mkdir -p /app
WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install --no-cache-dir poetry python-multipart uvicorn black pylint

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

EXPOSE 80

ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "trace", "--use-colors", "--reload"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
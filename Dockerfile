FROM python:3.8-slim

RUN pip install poetry
COPY . /.
RUN poetry install --no-dev


ENTRYPOINT ["/entrypoint.sh"]

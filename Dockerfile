FROM python:3.8-alpine

RUN pip install poetry
COPY . /.
RUN poetry install --no-dev


ENTRYPOINT ["/entrypoint.sh"]

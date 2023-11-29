FROM python:3.11-slim

RUN pip install -U pip poetry
COPY . /.
RUN poetry config virtualenvs.create false
RUN poetry install


ENTRYPOINT ["/entrypoint.sh"]

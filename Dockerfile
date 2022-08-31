FROM python:3.10-slim

RUN pip install -U pip poetry
COPY . /.
RUN poetry config virtualenvs.create false
RUN poetry install


ENTRYPOINT ["/entrypoint.sh"]

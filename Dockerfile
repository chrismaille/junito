FROM python:3.8-slim

RUN pip install poetry
COPY . /.
RUN poetry config virtualenvs.create false
RUN poetry install


ENTRYPOINT ["/entrypoint.sh"]

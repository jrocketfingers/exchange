FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml /app/
RUN poetry install
COPY . /app/

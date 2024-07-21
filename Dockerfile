

ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /code

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

# CMD [ "uvicorn","src.main:app","--host","0.0.0.0","--port","80","--reload" ]
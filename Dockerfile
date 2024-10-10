FROM python:3.12-slim as base

RUN mkdir /src
COPY ./src /src

COPY ./requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM base AS development

RUN pip install --editable /src

WORKDIR /src

CMD [ "uvicorn", "export.entrypoints.app:app", "--host", "0.0.0.0", "--reload" ]



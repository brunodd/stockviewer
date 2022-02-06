FROM python:3.9


RUN python -m pip install poetry


WORKDIR /code/
COPY poetry.lock pyproject.toml /code/
COPY stockviewer/ /code/stockviewer

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY app.py /code/

VOLUME /data/
ENV DATA_VOLUME=/data/

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:server"]
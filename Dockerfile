FROM condaforge/miniforge3

EXPOSE 8080

WORKDIR /code/

RUN conda install yfinance addict seaborn plotly dash gunicorn
COPY stockviewer.yml app.py /code/
COPY data/ /code/data/
COPY stockviewer/ /code/stockviewer/

ENV DATA_VOLUME=/code/data/

CMD python -m app

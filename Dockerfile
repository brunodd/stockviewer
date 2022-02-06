FROM python:3.9

WORKDIR /code/
COPY dist/stockviewer-0.1.0-py3-none-any.whl /code/
COPY app.py /code/app.py
RUN pip install /code/stockviewer-0.1.0-py3-none-any.whl

EXPOSE 8050
EXPOSE 80
EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:server"]
#ENTRYPOINT ["bash"]
#ENTRYPOINT ["python -m"]
#CMD ["app"]
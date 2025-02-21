FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11


COPY ./requirements/requirements.txt /app
COPY ./app /app/app

RUN pip install -r /app/requirements.txt

EXPOSE 80
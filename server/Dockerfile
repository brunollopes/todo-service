FROM python:latest AS build

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .
# EXPOSE 5000
#CMD gunicorn --bind 0.0.0.0:5000 wsgi 
CMD [ "uvicorn",  "app.app:app", "--host", "0.0.0.0", "--port", "5000"]
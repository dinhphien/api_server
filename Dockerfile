FROM python:3.6-alpine3.10
ENV FLASK_APP "api/application/main.py"
WORKDIR /api

COPY __init__.py  /api/__init__.py

#install dependencies:
COPY requirements.txt /api/
RUN pip3 install -r requirements.txt

#copy all the files to the container
COPY application  api/application

EXPOSE 5000


CMD flask run --host=0.0.0.0
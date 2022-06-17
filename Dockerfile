FROM python:3.10.5

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirement.txt /app/

RUN pip install -r /app/requirement.txt

COPY . /app/

#ENV POSTGRES_NAME=postgres
#ENV POSTGRES_USER=postgres
#ENV POSTGRES_PASSWORD=root
#ENV DB_HOST=db
#ENV DB_PORT=5432

#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN python manage.py runserver
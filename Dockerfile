from python:3.8

COPY ./ app/

WORKDIR app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
FROM python

COPY requirements.txt /app/

WORKDIR /app
RUN pip3 install -r requirements.txt

COPY czech_working_month/ /app

EXPOSE 5000

CMD FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000

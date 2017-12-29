#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import date
import logging

from flask import Flask, render_template

from .czech_working_month import CzechWorkingMonth


app = Flask(__name__)


@app.route('/')
def index():
    today = date.today()

    year_months = [(today.month-1, today.year) if today.month > 1 else (12, today.year-1),
                   (today.month, today.year),
                   (today.month + 1, today.year) if today.month < 12 else (1, today.year + 1)]

    return render_template('index.html',
                           year_months=year_months)


@app.route('/detail/<int:month>/<int:year>')
def detail(month, year):
    cwm = CzechWorkingMonth(day=1, month=month, year=year, part_time_ratio=0.6)

    return render_template('detail.html',
                           cwm=cwm)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    app.run(host='0.0.0.0', debug=True)

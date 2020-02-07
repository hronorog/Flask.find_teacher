# -*- coding: utf8 -*-
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def main():
    pass


@app.route('/goals/<goal>/')
def goals():
    pass


@app.route('/profile/<id_teacher>/')
def idtech():
    pass


@app.route('/request/')
def t_request():
    pass


@app.route('/request_done/')
def request_done():
    pass


@app.route('/booking/<id_teacher>/<time_week>/<time>/')
def bron():
    pass


@app.route('/booking_done/')
def bron_done():
    pass


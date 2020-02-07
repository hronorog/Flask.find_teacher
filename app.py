# -*- coding: utf8 -*-
from flask import Flask, render_template
from data import *
import json
from random import shuffle


# дни недели
week = {'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота',
        'sun': 'Воскресенье'
        }

# иконки целей
goal_icon = {"travel": "⛱",
             "study": "🏫",
             "work": "🏢",
             "relocate": "🚜"}

# список учителей в JSON
tea = teachers
tea = json.dumps(tea, ensure_ascii=False)
tea = json.loads(tea)


app = Flask(__name__)


@app.route('/')
def main():
    # рандомный список 6 учителей
    teach = tea
    shuffle(teach)
    teach = teach[:6]
    return render_template("index.html",
                           goals=goals,
                           goal_icon=goal_icon,
                           teachers=teach)


@app.route('/all_teachers/')
def all_teachers():
    return render_template('all_teachers.html', teachers=tea)


@app.route('/profile/<id_teacher>/')
def id_teach(id_teacher):
    for teacher in tea:
        if teacher['id'] == int(id_teacher):
            id_t = teacher
    # список целей
    lst = []
    for goal in id_t["goals"]:
        lst.append(goals[goal])
    return render_template("profile.html",
                           lst=lst,
                           teacher=id_t,
                           week=week)


@app.route('/goals/<goal>/')
def to_goals(goal):
    lst = []
    for teacher in tea:
        if goal in teacher["goals"]:
            lst.append(teacher)

    # иконка
    icon = goal_icon[goal]
    return render_template("goal.html",
                           icon=icon,
                           goal=goal,
                           goals=goals,
                           lst=lst)


@app.route('/request/')
def t_request():
    return render_template("request.html")


@app.route('/request_done/')
def request_done():
    return render_template("request_done.html")


@app.route('/booking/<id_teacher>/<time_week>/<time>/')
def bron(id_teacher, time_week, time):
    return render_template("booking.html")


@app.route('/booking_done/')
def bron_done():
    return render_template("booking_done.html")


@app.errorhandler(404)
@app.errorhandler(500)
def not_found(e):
    return "Такой страницы нет"


if __name__ == "__main__":
    app.run('0.0.0.0', 8000)

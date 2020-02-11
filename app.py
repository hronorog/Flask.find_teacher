# -*- coding: utf8 -*-
from flask import Flask, render_template, request
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


@app.route('/booking/<id_teacher>/<day_week>/<time>/')
def bron(id_teacher, day_week, time):
    return render_template("booking.html",
                           day=day_week,
                           teacher=tea[int(id_teacher)],
                           time=time,
                           week=week)


@app.route('/booking_done/', methods=['POST'])
def bron_done():
    teacherId = request.form.get('clientTeacher')
    teacherDay = request.form.get('clientWeekday')
    teacherTime = request.form.get('clientTime')
    clientName = request.form.get('clientName')
    clientPhone = request.form.get('clientPhone')

    # подготовка json-строки
    stroka = {"teacher":
                  {'ID': teacherId,
                   "day": teacherDay,
                   "time": teacherTime
                   },
              "client":
                  {"name": clientName,
                   "phone": clientPhone
                   }
              }

    with open('booking.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(stroka, sort_keys=True, indent=2, ensure_ascii=False))
    return render_template("booking_done.html",
                           teacherDay=teacherDay,
                           teacherTime=teacherTime,
                           clientName=clientName,
                           clientPhone=clientPhone)


@app.route('/request/')
def t_request():
    return render_template("request.html")


@app.route('/request_done/', methods=['POST'])
def request_done():
    goal = request.form.get('goal')
    time = request.form.get('time')
    clientName = request.form.get('clientName')
    clientPhone = request.form.get('clientPhone')

    stroka = {
        'goal': goal,
        'time': time,
        'clientName': clientName,
        'clientPhone': clientPhone
    }
    with open('request.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(stroka, sort_keys=True, indent=2, ensure_ascii=False))

    goal = goals[goal]
    return render_template("request_done.html",
                           goal=goal,
                           time=time,
                           clientName=clientName,
                           clientPhone=clientPhone)


@app.errorhandler(404)
@app.errorhandler(500)
def not_found(e):
    return "Такой страницы нет"


if __name__ == "__main__":
    app.run('0.0.0.0', 8000)

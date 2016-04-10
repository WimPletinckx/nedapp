from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import ExerciseConfigForm,AnswerForm,ExerciseForm

import random

list= [ {"woord":"a1","woordverklaring":"b1","woordincontext":"c1"}
      , {"woord":"a2","woordverklaring":"b2","woordincontext":"c2"}
      , {"woord":"a3","woordverklaring":"b3","woordincontext":"c3"}
      , {"woord":"a4","woordverklaring":"b4","woordincontext":"c4"}
      , {"woord":"a5","woordverklaring":"b5","woordincontext":"c5"}
      , {"woord":"a6","woordverklaring":"b6","woordincontext":"c6"}
      , {"woord":"a7","woordverklaring":"b7","woordincontext":"c7"}
]

@main.route('/', methods=['GET', 'POST'])
def index():
    form = ExerciseConfigForm()
    form.startIndex.choices=[]
    form.endIndex.choices=[]
    for i in range(len(list)):
        form.startIndex.choices.append((i, list[i]["woord"]))
        form.endIndex.choices.append((i, list[i]["woord"]))
    '''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    '''

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['level'] = form.level.data
        session['startIndex'] = form.startIndex.data
        session['endIndex'] = form.endIndex.data
        session['numberOfExercises'] = form.numberOfExercises.data
        session['score']=-1
        session['exerciseStarted']=0
        session['answers']=[]
        return redirect(url_for('.exercise'))

    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

@main.route('/exercise', methods=['GET', 'POST'])
def exercise():
    form = ExerciseForm()
    exercises = []

    if not session.get('exerciseStarted',False):
        answerdict = {}
        level = session.get("level")
        for i in range(session.get('numberOfExercises')):
            i = random.randrange(session.get("startIndex"),session.get("endIndex")+1)
            if level == 0 :
                question = list[i]["woord"]
                answerdict[question]= list[i]["woordverklaring"]
            elif level == 1 :
                question = list[i]["woordverklaring"]
                answerdict[question]= list[i]["woord"]
            else :
                question = list[i]["woordincontext"]
                answerdict[question]= list[i]["woord"]
            exercises.append(question)
        session['answerdict']=answerdict
        session['exercises']=exercises
        session['exerciseStarted']=1
    else :
        print "started"
        exercises = session['exercises']

    if request.method == 'POST':
        if request.form['action'] == 'Bereken score':
            print form.answers
            session['answers']=[]
            score = 0
            print len(form.answers.entries)
            for i in range(len(form.answers.entries)):
                print i
                answer = form.answers.entries[i].data['answer']
                session['answers'].append(answer)
                if answer.strip() == session['answerdict'][exercises[i]]:
                    score += 1
                else :
                    print "doesn't match with %s"%session['answerdict'][exercises[i]]

            session['score'] = score
            return redirect(url_for('.exercise'))
        elif request.form['action'] == 'Do Something Else':
            pass # do something else
        else:

            pass # unknown
    
    for i in range(session.get('numberOfExercises')):
        answerform = AnswerForm()
        if session['answers'] :
            answerform.answer=session['answers'][i]
        else :
            answerform.answer=""
        form.answers.append_entry(answerform)
    


    return render_template('exercise.html',
                           exerciseform=form, exercises=exercises, level=session.get('level'), score=session.get('score',-1))

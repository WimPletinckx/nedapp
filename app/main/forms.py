from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, IntegerField, FieldList, FormField	
from wtforms.validators import Required
from wtforms.widgets import TableWidget


class ExerciseConfigForm(Form):
    name = StringField('Wat is jouw naam?', validators=[Required()])
    level = SelectField('Moeilijkheidsgraad', choices=[(0, 'Woord -> Uitleg'), (1, 'Uitleg -> Woord'), (2, 'Zin -> Woord')],coerce=int)
    startIndex = SelectField('Startwoord',coerce=int)
    endIndex = SelectField('Eindwoord',coerce=int)
    numberOfExercises = IntegerField('Aantal oefeningen', validators=[Required()])
    submit = SubmitField('Start oefeningen')

class AnswerForm(Form):
    answer = StringField('')

class ExerciseForm(Form):
	answers = FieldList(FormField(AnswerForm))

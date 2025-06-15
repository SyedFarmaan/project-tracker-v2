
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired,Length

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")

class ProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Add Project")

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

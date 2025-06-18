
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo

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

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

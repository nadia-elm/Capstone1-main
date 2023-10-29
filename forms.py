from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,validators
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
  username = StringField('Username', validators=[Length(min=4, max=25),DataRequired()])
  email = StringField('Email ', validators= [Email(),DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Register')

class UserLoginForm(FlaskForm):

  username = StringField('Username', validators= [DataRequired()])
  password = PasswordField('Password', validators= [DataRequired()])
  submit = SubmitField('Login')





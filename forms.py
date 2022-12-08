from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Registrar")
    
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título Slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Crear Post')
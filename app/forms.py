from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange



class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password =  PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class IncomeForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired(), Length(max=200)])
    amount = DecimalField('Valor', validators=[DataRequired(), NumberRange(min=0.01)])
    date = DateField('Data', validators=[DataRequired()])
    category_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar')

class ExpenseForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired(), Length(max=200)])
    amount = DecimalField('Valor', validators=[DataRequired(), NumberRange(min=0.01)])
    date = DateField('Data', validators=[DataRequired()])
    category_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar')
class CategoryForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    type = SelectField('Tipo', choices=[('income', 'Receita'), ('expense', 'Despesa')], validators=[DataRequired()])
    color = StringField('Color (hex)', validators=[DataRequired()])
    submit = SubmitField('Registrar')

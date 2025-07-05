from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user
from app import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    email_exists = User.query.filter_by(email=form.email.data).first()
    username_exists = User.query.filter_by(username=form.username.data).first()

    if form.validate_on_submit():
        if email_exists:
            flash('Email já cadastrado.', 'danger')
            return redirect(url_for('auth.register'))
        if username_exists:
            flash('Usuário já cadastrado.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))




